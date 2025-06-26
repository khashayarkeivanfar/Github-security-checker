import csv
import os

def save_findings(findings, output_file='findings.csv'):
    exists = os.path.exists(output_file)
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['repo_url', 'key_value'])
        if not exists:
            writer.writeheader()
        for item in findings:
            writer.writerow({
                'repo_url': item['repo_url'],
                'key_value': item['key_value']
            })