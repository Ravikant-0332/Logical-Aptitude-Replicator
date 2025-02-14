import json
import os
import sys
import csv
import time
import logging
from process_automation.json_to_csv_parser import Parser
from pathlib import  Path
import winsound
from dotenv import load_dotenv
from log_handler import LoggerWriter
from process_automation.replicator import QuestionReplicator


load_dotenv()

API_KEY = os.getenv('KEY')
END_POINT = os.getenv('ENDPOINT')
MODEL_NAME = os.getenv('MODEL_NAME')
API_VERSION = os.getenv('API_VERSION')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.stdout = LoggerWriter(logging.info)
sys.stderr = LoggerWriter(logging.error)


def get_input_files():
    """
    Returns a list of file paths of all input files located in the 'inputs' directory.

    :return: A list containing the file paths of all files in the 'inputs' folder.
    """
    files = []

    folder_path = os.path.join(BASE_DIR, 'inputs')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            files.append(file_path)

    return files

def get_input_jsons(file_path):
    """
    :param file_path: The path to the CSV file that contains question data.
    :return: A list of dictionaries, where each dictionary represents a question with its options, solution, answer, and topic.
    """
    res_json = []

    with open(file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)
        for row in csv_reader:
            res_json.append({
                "question": row[1],
                "options": [row[i] for i in range(2, 7) if len(str(row[i]))>0],
                "solution": row[7],
                "answer": row[header.index(row[8])],
                "topic": row[9].removeprefix('LOGICAL_')
            })

    return res_json


if __name__ == '__main__':
    parser = Parser()
    replicator = QuestionReplicator(API_KEY, END_POINT, MODEL_NAME, API_VERSION)

    for file in get_input_files():
        all_questions = []
        for input_json in get_input_jsons(file):
            all_questions.extend(replicator.replicate(input_json))

        parser.parse_into_csv(all_questions, Path(file).name, BASE_DIR)

    for i in range(3):
        winsound.Beep(1300, 400)
        time.sleep(0.1)


