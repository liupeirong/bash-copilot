################################################
## *** Bash Copilot plugin function       *** ##
##         loaded by $HOME/.bashcopilotrc     ##
################################################

create_completion()
{
    # Get the text typed until now
    text=${READLINE_LINE}
    # BASH_COPILOT_PATH is defined in $HOME/.bashcopilotrc
    completion=$(echo -n "$text" | $BASH_COPILOT_PATH/src/main.py)
    # Add completion to the current buffer
    READLINE_LINE="${text}${completion}"
    # Put the cursor at the end of the line
    READLINE_POINT=${#READLINE_LINE}
}
