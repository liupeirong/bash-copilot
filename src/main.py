#!/usr/bin/python
# -*- coding: utf-8 -*-

from openai import AzureOpenAI
import sys

from prompt_file import PromptFile
from config import PromptConfig
from commands import get_command_result


if __name__ == "__main__":
    try:
        config = PromptConfig()
        aoai = AzureOpenAI(api_version=config.openai["api_version"],
                           api_key=config.openai["api_key"],
                           azure_endpoint=config.openai["api_base"])

        prompt_file = PromptFile(config)
        prompt_file.init_context()

        user_input = sys.stdin.read()
        user_input = user_input.rstrip()

        command_result = get_command_result(user_input, prompt_file)
        if (
            command_result != ""
        ):  # executed the command of this app not bash, must restart shell
            print(f"\n# {command_result}, exit shell.")
            sys.exit(0)

        in_msg = {"role": "user", "content": user_input}
        all_messages = prompt_file.get_all_messages()
        all_messages.append(in_msg)
        response = aoai.chat.completions.create(
            model=config.deployment, messages=all_messages, temperature=config.temperature, top_p=1, max_tokens=config.max_tokens, stop="#")
        if response.choices[0].finish_reason == "stop":
            completion_all = response.choices[0].message.content
            print(f"\n{completion_all}")
            prompt_file.append_interaction_to_context(user_input, completion_all)

    except Exception as e:
        print("\n\n# Bash Copilot error: Unexpected exception - " + str(e))
