#!/usr/bin/env bash
#
# Populate all QRCards site projects in Vikunja
#
# Usage: ./populate-all-sites.sh

set -e

POPULATE_SCRIPT="/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src/populate_vikunja.py"
VENV_PYTHON="/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src/venv/bin/python"
SITES_DIR="/home/ivanadmin/spawn-solutions/applications/qrcards-sites"

echo "📦 Populating QRCards Sites in Vikunja..."
echo ""

# Array of site YAML files
SITES=(
    "ivantohelpyou.yaml"
    "model-citizen-developer.yaml"
    "convention-city-seattle.yaml"
    "inverse-fractional.yaml"
    "taelyen.yaml"
)

for site in "${SITES[@]}"; do
    echo "➡️  Creating project from $site..."
    $VENV_PYTHON "$POPULATE_SCRIPT" --verbose "$SITES_DIR/$site"
    echo ""
done

echo "✅ All 5 QRCards site projects created!"
echo ""
echo "🌐 View in Vikunja: https://app.vikunja.cloud"
echo ""
echo "📝 Next steps:"
echo "   1. Open Vikunja and review the 5 new projects"
echo "   2. Complete the 'GTD Capture' task in each project"
echo "   3. Add specific tasks based on each site's needs"
