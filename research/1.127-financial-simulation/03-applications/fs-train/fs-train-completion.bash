#!/bin/bash
# Bash completion for fs-train
# Usage: source this file or add to ~/.bashrc:
#   source /path/to/fs-train-completion.bash

_fs_train_completion() {
    local cur prev scenarios_dir

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Find scenarios directory relative to script location
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    scenarios_dir="$script_dir/scenarios"

    # If completing scenario argument
    if [[ ${COMP_CWORD} -eq 1 ]] || [[ "${prev}" != --* ]]; then
        # Get scenario files
        if [[ -d "$scenarios_dir" ]]; then
            local scenarios=$(cd "$scenarios_dir" && ls *.yaml 2>/dev/null | sed 's/\.yaml$//')
            COMPREPLY=( $(compgen -W "${scenarios}" -- "${cur}") )

            # Also add numbers as shortcuts
            local numbers=$(cd "$scenarios_dir" && ls *.yaml 2>/dev/null | grep -o '^[0-9]\+' | sort -u)
            COMPREPLY+=( $(compgen -W "${numbers}" -- "${cur}") )
        fi
        return 0
    fi

    # Complete flags
    if [[ ${cur} == -* ]]; then
        COMPREPLY=( $(compgen -W "--llm --list --scenarios-dir --help" -- "${cur}") )
        return 0
    fi
}

# Register completion
complete -F _fs_train_completion run-fs-train
complete -F _fs_train_completion fs-train
