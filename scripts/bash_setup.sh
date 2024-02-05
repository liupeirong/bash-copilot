#!/usr/bin/bash

set -e
trap 'exitScript' ERR

help()
{
    cat <<- _EOF_
Help for Bash Copilot setup script

Usage: source bash_setup.sh [optional parameters]

    -d           Print some system information for debugging.
    -h           Print this help content.

To uninstall Bash Copilot use bash_cleanup.sh.
_EOF_
}

configureApp()
{ 
    chmod +x "$BASH_COPILOT_PATH/src/main.py"
}

# Create and load ~/.bashcopilotrc to setup bash 'Ctrl + G' binding
configureBash()
{
    echo "*** Configuring bash [$BASH_COPILOT_PATH] ***"
    echo -n > $BASH_COPILOT_RC_FILE
    echo "export BASH_COPILOT_PATH=\"${BASH_COPILOT_PATH}\"" >> $BASH_COPILOT_RC_FILE
    echo 'source "${BASH_COPILOT_PATH}/scripts/bash_plugin.sh"' >> $BASH_COPILOT_RC_FILE
    echo "bind -x '\"\C-g\":\"create_completion\"'" >> $BASH_COPILOT_RC_FILE
    echo "SOURCED: $SOURCED"
    if [ $SOURCED -eq 1 ]; then
        echo "*** Testing bash settings [$BASH_COPILOT_RC_FILE] ***"
        source "$BASH_COPILOT_RC_FILE"
    fi
}

# Add call to .bashcopilotrc into .bashrc
enableApp()
{
    echo "*** Activating application [$HOME/.bashrc] ***"
    # Check if already installed
    if grep -Fq ".bashcopilotrc" $HOME/.bashrc; then
        return 0
    fi
    echo -e "\n# Initialize Bash Copilot" >> $HOME/.bashrc
    echo 'if [ -f "$HOME/.bashcopilotrc" ]; then' >> $HOME/.bashrc
    echo '    . "$HOME/.bashcopilotrc"' >> $HOME/.bashrc
    echo 'fi' >> $HOME/.bashrc
}

# Print some system details useful to debug the script in case it's not working
systemInfo()
{
    echo "*** system ***"
    uname -smpr
    echo "*** bash interpreter ***"
    echo $BASH_VERSION
    echo "*** python ***"
    if command -v python &> /dev/null; then
        which python
        python --version
    else
        echo "python not found"
    fi
    echo "*** curl ***"
    if command -v curl &> /dev/null; then
        which curl
        curl --version
    else
        echo "curl not found"
    fi
}

# Remove variables and functions from the environment, in case the script was sourced
cleanupEnv()
{
    unset SOURCED
}

# Clean exit for sourced scripts
exitScript()
{
    cleanupEnv
    kill -SIGINT $$
}

# Detect if the script is sourced
(return 0 2>/dev/null) && SOURCED=1 || SOURCED=0

BASH_COPILOT_PATH="$HOME/clouddrive/bash_copilot"
BASH_COPILOT_RC_FILE="$HOME/.bashcopilotrc"

configureApp
configureBash
enableApp
cleanupEnv

echo -e "*** Setup complete! ***\n";

echo "***********************************************"
echo "Open a new Bash terminal, type '#' followed by"
echo "your natural language command and hit Ctrl + G!"
echo "***********************************************"
