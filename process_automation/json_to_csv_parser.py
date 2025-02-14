import csv
import os


class Parser:

    def __init__(self):
        pass

    def parse_into_csv(self, questions, filename, base_dir):

        headers = ["S. No",	"Question",	"Option A", "Option B", "Option C", "Option D", "Option E", "Explanation", "Key", "SUB TOPIC"]
        rows = []
        sr_no = 0
        for question in questions:
            sr_no += 1
            row = [
                sr_no,
                question.get('question'),
                question.get('options')[0],
                question.get('options')[1],
                question.get('options')[2],
                question.get('options')[3],
                question.get('options')[4] if len(question.get('options'))>4 else "",
                question.get('solution').replace('$$', '$'),
                question.get('answer'),
                f"LOGICAL_{question.get('topic')}",
            ]
            rows.append(row)

        os.makedirs('outputs', exist_ok=True)
        with open(os.path.join(base_dir, 'outputs', f"{filename}"), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(rows)
            print(f"CSV file {os.path.join(os.path.dirname(base_dir), 'outputs', f"{filename}")} generated successfully.")

            print(questions)
