#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openai
import sys

from prompt_file import PromptFile
from config import PromptConfig
from commands import get_command_result


if __name__ == '__main__':
    try:
        config = PromptConfig()
        openai.api_base = config.openai['api_base']
        openai.api_key = config.openai['api_key']
        openai.api_type = config.openai['api_type']
        openai.api_version = config.openai['api_version']

        prompt_file = PromptFile(config)
        prompt_file.init_context()

        user_input = sys.stdin.read()

        command_result = get_command_result(user_input, prompt_file)
        if command_result != "":  # executed the command of this app not bash, must restart shell
            print("Command completed, exit shell.")
            sys.exit(0)

        query = prompt_file.append_input_to_context(user_input)
        # TODO: change this to chatcompletion API
        response = openai.Completion.create(
            engine=config.deployment, prompt=query, temperature=config.temperature, top_p=1, max_tokens=config.max_tokens, stop="#")
        completion_all = response['choices'][0]['text']
        print(completion_all)

        if completion_all != "" or len(completion_all) > 0:
            prompt_file.append_output_to_context(completion_all)
        
    except FileNotFoundError:
        print('\n\n# Bash Copilot error: Prompt file not found, try again')
    except openai.error.RateLimitError:
        print('\n\n# Bash Copilot error: Rate limit exceeded, try later')
    except openai.error.APIConnectionError:
        print('\n\n# Bash Copilot error: API connection error, are you connected to the internet?')
    except openai.error.InvalidRequestError as e:
        print('\n\n# Bash Copilot error: Invalid request - ' + str(e))
    except Exception as e:
        print('\n\n# Bash Copilot error: Unexpected exception - ' + str(e))
