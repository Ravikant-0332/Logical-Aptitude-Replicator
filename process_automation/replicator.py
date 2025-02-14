import os
import csv
import json
import time

from .gpt_prompt import Prompt
from .gpt_connect import ChatAgent
from .json_to_csv_parser import Parser


class QuestionReplicator:

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, api_key, endpoint, model_name, api_version):
        self.API_KEY = api_key
        self.ENDPOINT = endpoint
        self.MODEL_NAME = model_name
        self.API_VERSION = api_version
        self.PARSER = Parser()
        self.PROMPT = Prompt()

    @classmethod
    def get_sample_data(cls):
        file_path = os.path.join(cls.BASE_DIR, 'sample_data', 'questions.csv')

        questions = {}

        with open(file_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                questions[row[2].lower()] = questions.get(row[2].lower(), [])
                questions[row[2].lower()].append({
                    "question": row[1],
                    "options": [row[2], row[3], row[4], row[5]],
                    "explanation": row[6],
                    "answer": row[header.index(row[7])],
                    "topic": row[8].removeprefix('LOGICAL_')
                })

        return questions

    def replicate(self, question):
        agent = ChatAgent(self.ENDPOINT, self.API_KEY, self.API_VERSION)

        replicated_questions = [question]

        input_for_solution_gen = {
            "base_question": {
            "question": question.get('question', ""),
            "solution": question.get('solution')
            },
            "new_question": "",
            "correct_answer": ""
        }

        replication_prompt = [
            {
                "role": "system",
                "content": self.PROMPT.get_assistant_role(),
            },
            {
                "role": "user",
                "content": f"I want 5 replication of this question, {question}"
            }
        ]

        t = time.time()
        print("Replicating...")
        response = json.loads(agent.resolve_query(self.MODEL_NAME, replication_prompt))
        print(f"Replication finished in {round(time.time()-t, 2)} seconds")

        for replica in response:

            input_for_solution_gen['new_question'] = replica.get('question')
            input_for_solution_gen['correct_answer'] = replica.get('answer')

            solution_gen_prompt = [
                {
                    "role": "system",
                    "content": self.PROMPT.get_assistant_role(),
                },
                {
                    "role": "user",
                    "content": f"Generate solution for the given question, {input_for_solution_gen}"
                }
            ]
            t = time.time()
            print("Writing Solution for the replicated question...")
            solution = agent.resolve_query(self.MODEL_NAME, solution_gen_prompt)
            print(f"Generated Solution in {round(time.time()-t, 2)} seconds")

            replicated_questions.append({
                "question": replica.get('question'),
                "options": replica.get('options'),
                "solution": solution,
                "answer": replica.get('answer'),
                "topic": question.get('topic')
            })

        return replicated_questions


if __name__ == "__main__":
    print(QuestionReplicator.get_sample_data())



