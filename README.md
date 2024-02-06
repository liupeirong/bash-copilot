
# Introduction

This is a command line tool that lets you type in natural language and generates bash commands which you can decide to run.
It's inspired by [the Codex Cli sample](https://github.com/microsoft/Codex-CLI/tree/main) and has been refactored
 from deprecated Codex models to GPT models with chat completion APIs.

## How to set it up?

You only need to set it up once.

### Install Python and OpenAI

1. Clone this repo to your machine, to a folder <REPO_ROOT>. All files mentioned below are relative to this root.
1. Set the environment variables `OPENAI_API_URL` and `OPENAI_API_KEY` to point to your Azure OpenAI Service.
1. Edit `config.ini` to configure your Azure OpenAI deployment and model.
1. Install Python 3.8+.
1. Install Python modules by running `pip install -r requirements.txt`. This copilot has dependency on `openai` only.

### Configure bash

1. Set the environment variable `BASH_COPILOT_PATH` in `scripts/bash_setup.sh` to your <REPO_ROOT>.
1. Adjust the `#!` path for bash in the first line of all `.sh` files in the `scripts` folder.
1. Adjust the `#!` path for python in the first line of `src/main.py`.
1. Run `scripts/bash_setup.sh`, then open a new bash console.

## How to run?

In a bash console, type in `#` followed by your question in natural language in one line. Hit `Ctrl + G` when you are done.

If there's no error, Azure OpenAI will generate a bash command. If you like the command, hit enter to run it.
 Otherwise hit `Ctrl + C` to quit.

### Memory

User/AI Q&A history is stored in `current_context.txt`. When this copilot starts, it will load this history as its memory.

* If the total number of tokens is beyond the specified max number of tokens, earlier history will be deleted.
* You can run the commands `# show context`, `# clear last context`, or `# clear context` to interact with this memory.

## How to customize for your use case?

1. You can customize system prompt in `contexts/system_prompt.txt`.
1. You can customize few-shot examples in `contexts/examples.txt`.
