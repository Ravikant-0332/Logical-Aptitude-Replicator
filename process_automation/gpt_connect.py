from openai import AzureOpenAI
from dotenv import load_dotenv
from .gpt_prompt import Prompt

load_dotenv()


class ChatAgent:

    def __init__(self, end_point, key, version):

        self.client = AzureOpenAI(azure_endpoint=end_point, api_key=key, api_version=version)
        self.prompt = Prompt()

    def resolve_query(self, model, prompt):

        messages = [
            {
                "role": "system",
                "content": self.prompt.get_assistant_role(),
            }
        ]

        messages.extend(prompt)

        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
            max_tokens=1000
        )
        return completion.choices[0].message.content

