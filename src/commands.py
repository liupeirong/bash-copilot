import os

from prompt_file import PromptFile

def get_command_result(input: str, context: PromptFile):
    """
    Checks if the input is a command and if so, executes it
    Currently supported commands:
    - show context
    - clear context
    - clear last context

    Returns: command result or "" if no command matched
    """
    # context file commands
    if input.__contains__("context"):
        # show context <n>
        if input.__contains__("show"):
            print(f"-------------display: {context.current_context_file}:")
            os.system(f"cat {context.current_context_file}")
            print('\n')
            print(f"-------------display: messages in memory:")
            for msg in context.meta_messages + context.user_messages:
                print(f"{msg['role']}: {msg['content']}")
            return "context shown"
        
        # clear last context
        if input.__contains__("clear last"):
            context.clear_last_interaction()
            return "cleared last interaction"
        
        # clear context
        if input.__contains__("clear"):
            context.clear_context()
            return "cleared context"
        
    return ""