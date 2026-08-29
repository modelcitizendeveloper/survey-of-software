#!/usr/bin/env bash
#
# run-droplet.sh — run this harness on a STANDARD x86 machine and destroy it after.
#
# WHY THIS EXISTS. The first four cells of RESULTS.md were measured on aarch64, under WSL2,
# on a laptop. That is not a standard machine, and the conclusion it supported — "16-32x sits
# at the bottom of Astral's claimed 10-100x range" — is a comparison against numbers that were
# themselves measured on x86. Comparing an ARM measurement to an x86 claim and reporting where
# it "sits in the range" is not a comparison at all.
#
# So: same harness, same pinned corpus, same pinned tools, on a stated cloud instance that
# anyone can rent for pennies. The instance type goes in RESULTS.md next to the numbers,
# because "standard hardware" means nothing unless you say which.
#
# It also tests something the laptop cannot: that the PUBLISHED container actually builds and
# runs on a fresh machine that has never seen this project. That is the claim the workshop
# download page makes on the reader's behalf.
#
# Lifecycle:  create -> wait ssh -> install docker -> ship harness -> build -> run -> collect
#             -> DESTROY (trap, fires on any exit path)
#
# Secrets come from ~/gt/scripts/mutation-sweep/.env, the same file the mutation sweep uses:
# DIGITALOCEAN_ACCESS_TOKEN, DO_SSH_KEY_NAME, SSH_KEY_FILE.
#
# Usage:  ./run-droplet.sh [--size SLUG] [--region SLUG] [--scales "1 12"] [--reps N]
#                          [--keep] [--dry-run]
set -euo pipefail

note() { echo -e "\033[36m>\033[0m $*"; }
die()  { echo "error: $*" >&2; exit 1; }

# Source the secrets BEFORE computing defaults. The first version read DO_REGION from the
# shell and sourced .env thirty lines later, so the .env's own region was silently ignored —
# it only worked because the fallback happened to match.
ENVF="$HOME/gt/scripts/mutation-sweep/.env"
[[ -f "$ENVF" ]] || die "no .env at $ENVF"
set -a; . "$ENVF"; set +a
: "${DIGITALOCEAN_ACCESS_TOKEN:?}" "${DO_SSH_KEY_NAME:?}" "${SSH_KEY_FILE:?}"

# 8 vCPU x86, so ARCHITECTURE is the only variable that moved against the 8-core ARM box.
# s5-* is not offered in every region — it lives in atl1/mem1/mkc1/ric1, not tor1, and DO
# rejects the mismatch with a 422 rather than picking somewhere for you.
SIZE="${DO_FMT_SIZE:-s5-8vcpu-16gb-30gb}"
REGION="${DO_FMT_REGION:-atl1}"
IMAGE="ubuntu-24-04-x64"
SCALES="${SCALES:-1 12}"
REPS="${REPS:-9}"
KEEP=0 DRYRUN=0
NAME="sos-fmt-bench-$$"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --size)   SIZE="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --scales) SCALES="$2"; shift 2 ;;
    --reps)   REPS="$2"; shift 2 ;;
    --keep)   KEEP=1; shift ;;
    --dry-run) DRYRUN=1; shift ;;
    -h|--help) sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

DO=(doctl --access-token "$DIGITALOCEAN_ACCESS_TOKEN")
command -v doctl >/dev/null || die "doctl not on PATH"

HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HERE/out"

if [[ $DRYRUN -eq 1 ]]; then
  note "DRY RUN — would create $NAME ($SIZE, $IMAGE, $REGION), run scales '$SCALES' at $REPS reps, then destroy"
  exit 0
fi

# TEARDOWN FIRST, before anything can be created. A benchmark droplet that outlives the
# benchmark bills forever, and the failure is silent — it just keeps costing money.
DROPLET_ID=""
teardown() {
  local rc=$?
  if [[ -n "$DROPLET_ID" && $KEEP -eq 0 ]]; then
    note "destroying droplet $DROPLET_ID"
    "${DO[@]}" compute droplet delete "$DROPLET_ID" --force >/dev/null 2>&1 \
      && note "destroyed" \
      || echo "WARNING: could not destroy droplet $DROPLET_ID — CHECK YOUR ACCOUNT" >&2
  elif [[ -n "$DROPLET_ID" ]]; then
    note "--keep: droplet $DROPLET_ID left running. Destroy it yourself."
  fi
  exit $rc
}
trap teardown EXIT INT TERM

KEY_ID="$("${DO[@]}" compute ssh-key list --format Name,ID --no-header \
          | awk -v n="$DO_SSH_KEY_NAME" '$0 ~ n {print $NF}' | head -1)"
[[ -n "$KEY_ID" ]] || die "ssh key '$DO_SSH_KEY_NAME' not found on the account"

note "creating $NAME ($SIZE, $IMAGE, $REGION)"
DROPLET_ID="$("${DO[@]}" compute droplet create "$NAME" \
  --size "$SIZE" --image "$IMAGE" --region "$REGION" --ssh-keys "$KEY_ID" \
  --wait --format ID --no-header)"
[[ -n "$DROPLET_ID" ]] || die "droplet create returned no id"
IP="$("${DO[@]}" compute droplet get "$DROPLET_ID" --format PublicIPv4 --no-header)"
note "droplet $DROPLET_ID at $IP"

# `-n` and the keepalives are not decoration. On the first real run the benchmark FINISHED,
# wrote both result files, and the ssh session never returned — so the script sat wedged
# holding an idle droplet that billed until a human noticed it flat on the CPU graph. The
# remote `timeout` did its job; the hang was in ssh itself, waiting on a channel docker had
# left open. `-n` detaches stdin, ServerAlive* makes a dead peer fatal instead of eternal,
# and every call below is additionally wrapped in a LOCAL timeout.
#
# THE RULE THIS COST US: the teardown trap only fires when the script reaches an exit. A trap
# cannot rescue a process that never returns, so every remote call needs its own local clock.
SSH=(ssh -n -i "$SSH_KEY_FILE" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null
     -o ConnectTimeout=10 -o LogLevel=ERROR -o ServerAliveInterval=15 -o ServerAliveCountMax=4
     "root@$IP")

note "waiting for ssh"
for i in $(seq 1 60); do
  "${SSH[@]}" true 2>/dev/null && break
  [[ $i -eq 60 ]] && die "ssh never came up"
  sleep 5
done

note "recording what this machine actually is"
"${SSH[@]}" 'echo "  $(uname -m) | $(nproc) cores | $(grep -m1 "model name" /proc/cpuinfo | cut -d: -f2- | xargs) | $(free -g | awk "/Mem:/{print \$2}")GB"'

# cloud-init still holds the dpkg lock for a minute or two after ssh comes up, so an
# immediate apt-get fails. The first version also sent apt's output to /dev/null, so the
# failure surfaced later as the useless "Unit docker.service not found" — never silence the
# step you are about to depend on.
note "waiting for cloud-init to release the package lock"
"${SSH[@]}" 'cloud-init status --wait >/dev/null 2>&1 || true' || true

note "installing docker"
timeout 900 "${SSH[@]}" 'set -e
  export DEBIAN_FRONTEND=noninteractive
  for i in $(seq 1 10); do
    if apt-get update -qq && apt-get install -y -qq docker.io rsync; then break; fi
    echo "  apt attempt $i failed (lock held?), retrying in 15s" >&2
    [ $i -eq 10 ] && { echo "apt never succeeded" >&2; exit 1; }
    sleep 15
  done
  systemctl enable --now docker
  docker --version' || die "docker install failed"

note "shipping the harness"
rsync -az --delete -e "ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR" \
  --exclude node_tools --exclude __pycache__ --exclude out \
  "$HERE/" "root@$IP:/root/harness/"

note "building the container (this also proves the PUBLISHED harness builds on a clean machine)"
timeout 1800 "${SSH[@]}" 'cd /root/harness && docker build -q -t sos-fmt-bench:1.253 . >/dev/null' \
  || die "container build failed on a clean machine — that is a real finding, not a blip"

for s in $SCALES; do
  note "running scale x$s at $REPS reps"
  timeout 4200 "${SSH[@]}" "cd /root/harness && mkdir -p out && REPS=$REPS SCALE=$s timeout 3600 \
      docker run --rm -e REPS -e SCALE -v /root/harness/out:/out sos-fmt-bench:1.253 >/dev/null" \
    || echo "WARNING: scale x$s did not complete or ssh hung after it did" >&2
done

note "collecting results"
rsync -az -e "ssh -i $SSH_KEY_FILE -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR" \
  "root@$IP:/root/harness/out/" "$HERE/out/"

# The instance type is part of the method. A result that says "measured on x86" without
# saying WHICH x86 is the same underspecified claim this harness exists to correct.
for f in "$HERE"/out/results-container-x86_64-*.json; do
  [[ -e "$f" ]] || continue
  python3 - "$f" "$SIZE" "$REGION" "$IMAGE" <<'PY'
import json, sys
p, size, region, image = sys.argv[1:5]
d = json.load(open(p))
d["machine"]["instance"] = {"provider": "digitalocean", "size": size,
                            "region": region, "image": image}
json.dump(d, open(p, "w"), indent=2)
print(f"  stamped {p.split('/')[-1]} with instance {size}")
PY
done

note "done — results in $HERE/out/"
ls -la "$HERE/out/" | grep x86_64 || echo "  (no x86 results collected — check the warnings above)"
