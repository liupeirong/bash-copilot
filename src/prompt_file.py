import os

from config import PromptConfig


def count_tokens_approx(messages: list):
    count = 0
    for m in messages:
        count += len(m["content"])
    return count


class PromptFile:
    current_context_file = ""
    system_prompt_file = ""
    examples_file = ""
    token_count = 0
    meta_messages = []
    user_messages = []
    config: PromptConfig

    def __init__(self, config: PromptConfig):
        self.current_context_file = os.path.join(
            os.path.dirname(__file__), "..", "current_context.txt"
        )
        self.system_prompt_file = os.path.join(
            os.path.dirname(__file__), "..", "contexts", "system_prompt.txt"
        )
        self.examples_file = os.path.join(
            os.path.dirname(__file__), "..", "contexts", "examples.txt"
        )
        self.config = config

    def init_meta_context(self):
        self.meta_messages = []
        with open(self.system_prompt_file, "r") as f:
            lines = f.readlines()
            self.meta_messages.append({"role": "system", "content": "".join(lines)})
        with open(self.examples_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                if line.startswith("#"):
                    self.meta_messages.append({"role": "user", "content": line})
                elif line.strip() != "":
                    self.meta_messages.append({"role": "assistant", "content": line})
        self.token_count = count_tokens_approx(self.meta_messages)

    def clear_user_context(self):
        self.user_messages = []
        if os.path.exists(self.current_context_file):
            with open(self.current_context_file, "w") as f:
                pass

    def init_user_context(self):
        self.user_messages = []
        if os.path.exists(self.current_context_file):
            with open(self.current_context_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.rstrip()
                    if line.startswith("#"):
                        self.user_messages.append({"role": "user", "content": line})
                    elif line.strip() != "":
                        self.user_messages.append({"role": "assistant", "content": line})
            self.token_count += count_tokens_approx(self.user_messages)
        else:
            with open(self.current_context_file, "w") as f:
                pass

    def clear_context(self):
        self.clear_user_context()
        self.init_meta_context()

    def init_context(self):
        self.init_meta_context()
        self.init_user_context()

    def get_all_messages(self) -> list:
        return self.meta_messages + self.user_messages

    def append_interaction_to_context(self, input, output):
        in_msg = {"role": "user", "content": input}
        input_tokens_count = count_tokens_approx([in_msg])
        if self.token_count + input_tokens_count > self.config.max_tokens:
            # delete first 2 lines of prompt context file
            self.token_count -= count_tokens_approx(self.user_messages[:2])
            self.user_messages = self.user_messages[2:]
            with open(self.current_context_file, "w") as f:
                for m in self.user_messages:
                    f.write(f'{m["content"]}\n')

        self.token_count += input_tokens_count
        self.user_messages.append(in_msg)
        with open(self.current_context_file, "a") as f:
            f.write(f'{in_msg["content"]}\n')

        out_msg = {"role": "assistant", "content": output}
        self.user_messages.append(out_msg)
        self.token_count += count_tokens_approx([out_msg])
        with open(self.current_context_file, "a") as f:
            f.write(f'{out_msg["content"]}\n')

    def clear_last_interaction(self):
        if len(self.user_messages) == 0:
            return
        
        m = self.user_messages.pop()
        # could be a user/assistant pair
        if m["role"] == "assistant":
            self.token_count -= count_tokens_approx([m])
            m2 = self.user_messages.pop()
            assert m2["role"] == "user"
            self.token_count -= count_tokens_approx([m2])
        # or could be just the user
        elif m["role"] == "user":
            self.token_count -= count_tokens_approx([m])
        with open(self.current_context_file, "w") as f:
            for m in self.user_messages:
                f.write(f'{m["content"]}\n')
