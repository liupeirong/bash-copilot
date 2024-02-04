import os

from config import PromptConfig


def count_tokens_approx(messages: list):
    count = 0
    for m in messages:
        count += len(m['content'])
    return count


class PromptFile:
    current_context_file = ''
    system_prompt_file = ''
    examples_file = ''
    token_count = 0
    meta_messages = []
    user_messages = []
    config:PromptConfig

    def __init__(self, config: PromptConfig):
        self.current_context_file = os.path.join(os.path.dirname(__file__), '..', 'current_context.txt')
        self.system_prompt_file = os.path.join(os.path.dirname(__file__), '..', 'context', 'system_prompt.txt')
        self.examples_file = os.path.join(os.path.dirname(__file__), '..', 'context', 'examples.txt')
        self.config = config
    
    def init_context(self):
        self.meta_messages = []
        with open(self.system_prompt_file, 'r') as f:
            lines = f.readlines()
            self.meta_messages.append({'role': 'system', 'content': lines.join('\n')})
        with open(self.examples_file, 'r') as f:
            line = f.readline()
            if line.startswith('#'):
                self.meta_messages.append({'role': 'user', 'content': line})
            elif line.trim() != '':
                self.meta_messages.append({'role': 'assistant', 'content': line})
        self.token_count = count_tokens_approx(self.meta_messages)

        self.user_messages = []
        with open(self.current_context_file, 'r+') as f:
            line = f.readline()
            if line.startswith('#'):
                self.user_messages.append({'role': 'user', 'content': line})
            elif line.trim() != '':
                self.user_messages.append({'role': 'assistant', 'content': line})
        self.token_count += count_tokens_approx(self.user_messages)

    def append_input_to_context(self, input):
        msg = {'role': 'user', 'content': input}
        input_tokens_count = count_tokens_approx([msg])
        if self.token_count + input_tokens_count > self.config.max_tokens:
            # delete first 2 lines of prompt context file
            self.token_count -= count_tokens_approx(self.user_messages[:2])
            self.user_messages = self.user_messages[2:]
            with open(self.current_context_file, 'w') as f:
                for m in self.user_messages:
                    f.write(f'{m["content"]}\n')

        self.token_count += input_tokens_count
        self.user_messages.append(msg)
        with open(self.current_context_file, 'a') as f:
            f.write(f'{msg["content"]}\n')
        return self.meta_messages + self.user_messages
    
    def append_output_to_context(self, llm_output):
        msg = {'role': 'assistant', 'content': llm_output}
        self.user_messages.append(msg)
        self.token_count += count_tokens_approx([msg])
        with open(self.current_context_file, 'a') as f:
            f.write(f'{msg["content"]}\n')
        
    def clear_last_interaction(self):
        m = self.user_messages.pop()
        # could be a user/assistant pair
        if m['role'] == 'assistant':
            self.token_count -= count_tokens_approx([m])
            m2 = self.user_messages.pop()
            assert m2['role'] == 'user'
            self.token_count -= count_tokens_approx([m2])
        # or could be just user
        elif m['role'] == 'user':
            self.token_count -= count_tokens_approx([m])
        with open(self.current_context_file, 'w') as f:
            for m in self.user_messages:
                f.write(f'{m["content"]}\n')

