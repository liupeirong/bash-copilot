#!/usr/bin/env bash

uninstall()
{
    # Remove key binding (works only for sourced script calls)
    if [ $SOURCED -eq 1 ]; then
        bind -r "\C-g"
    fi

    echo "Bash Copilot has been removed."
}

# Detect if the script is sourced
(return 0 2>/dev/null) && SOURCED=1 || SOURCED=0
echo "SOURCED: $SOURCED"

uninstall

unset SOURCED
