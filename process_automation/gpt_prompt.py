import os


class Prompt:

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def get_assistant_role(self):
        with open(os.path.join(self.BASE_DIR, 'prompts', 'assistant_role.txt'), 'r') as f:
            return f'{f.read()}'

    def prompt_for_explanation(self, question):
        with open(os.path.join(self.BASE_DIR, 'prompts', 'generate_explanation.txt'), 'r') as f:
            return f'{f.read()}\n{question}'

    def prompt_for_replication(self, question):
        with open(os.path.join(self.BASE_DIR, 'prompts', 'replicate_question.txt'), 'r') as f:
            return f'{f.read()}\n{question}'


if __name__ == "__main__":
    prompt = Prompt()
    print('Testing...')

