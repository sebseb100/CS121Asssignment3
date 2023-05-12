import os 
import json 
from bs4 import BeautifulSoup
import re 
from collections import defaultdict

json_file = os.path.join(os.getcwd(), 'DEV')


def build_inverted_index():
    inverted_index = defaultdict(list)

    for cur, subdir, files in os.walk(json_file):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(cur, file),'r') as fizzy:
                    data = json.load(fizzy)
                soup = BeautifulSoup(data['content'], 'html.parser')
                text = soup.get_text()

                tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
                undup_tokens = set(tokens)
                for token in undup_tokens:
                    inverted_index[token].append({'doc_id': file, "tf-dif": tokens.count(token)})
    with open('inverted_index.json', 'w') as f:
        json.dump(inverted_index, f)
    return inverted_index

def write_report(inverted_dic):
    with open('report.txt', 'w') as f:
        f.write("Inverted Index\n\n")
        for term, posts in inverted_dic.items():
            f.write(f'Term: {term}\nDocuments:\n')
            for post in posts:
                f.write(f' - {post["doc_id"]}: tf={post["tf-dif"]}\n')
            f.write('\n')


if __name__ == "__main__":
    inverted = build_inverted_index()
    write_report(inverted)