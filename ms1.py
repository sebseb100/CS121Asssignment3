import os 
import json 
from bs4 import BeautifulSoup
import re 

json_file = '/DEV'


def build_inverted_index():
    inverted_index = {}

    for cur, subdir, files in os.walk(json_file):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(cur,file),'r') as fizzy:
                    data = json.load(fizzy)

                s = BeautifulSoup(json_data['html'], 'html.parser')
                text = soup.get_text()

                tokens = re.findall(r"[a-zA-Z0-9]+", stringer.lower())
                undup_tokens = set(tokens)
                for token in undup_tokens:
                    if token not in inverted_index.keys():
                        inverted_index[token] = []
                    inverted_index[token].append({'doc_id': file, "tf-dif": tokens.count(token)})
    return inverted_index

def write_report(inverted_dic):
    with open('report.txt', 'w') as f:
        f.write("Inverted Index\n\n")
        for term, posts in inverted_dic.items():
            f.write(f'Term: {term}\nDocuments:\n')
            for post in posts:
                f.write(f' - {posting["doc-id"]}: tf={posting["tf-dif"]}\n')
            f.write('\n')