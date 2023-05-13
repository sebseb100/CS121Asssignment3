import os 
import json 
from bs4 import BeautifulSoup
import re 
from collections import defaultdict
from nltk.stem import PorterStemmer

json_file = os.path.join(os.getcwd(), 'DEV')
# json_file = os.path.join(os.getcwd(), 'ANALYST')

file_counter = 0
index_size = 0

def build_inverted_index():
    global file_counter, index_size

    inverted_index = defaultdict(list)

    for cur, subdir, files in os.walk(json_file):
        for file in files:
            print(file)
            file_counter += 1
            if file.endswith('.json'):
                try:
                    cur_file_path = os.path.join(cur, file)
                    with open(cur_file_path,'r') as f:
                        data = json.load(f)
                        soup = BeautifulSoup(data['content'], 'html.parser')
                        text = soup.get_text()


                    tokens = re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower())
                    undup_tokens = set(tokens)
                    for token in undup_tokens:
                        inverted_index[token].append({'doc_id': file, "tf-dif": tokens.count(token)})
                except:
                    print("BAD FILE")

                # index_size_bytes = os.path.getsize(cur_file_path)
                # index_size += (index_size_bytes/1024)
                write_report(inverted_index)
        write_json(inverted_index)

    return inverted_index
def write_json(inverted_dic):
    with open('inverted_index.json', 'w') as f:
            json.dump(inverted_dic, f)


def write_report(inverted_dic):
    global file_counter

    file_path = os.path.join(os.getcwd(), 'inverted_index.json')
    index_size_bytes = os.path.getsize(file_path)
    index_size = (index_size_bytes/1024)
    with open('report.txt', 'w') as f:
        f.write("Inverted Index\n\n")
        # for term, posts in inverted_dic.items():
        #     f.write(f'Term: {term}\nDocuments:\n')
        #     for post in posts:
        #         f.write(f' - {post["doc_id"]}: tf={post["tf-dif"]}\n')
        #     f.write('\n')
        f.write(f'Number of Indexed Documents: {file_counter}\n')
        f.write(f'Number of Unique Tokens: {len(inverted_dic.keys())}\n')
        f.write(f'Total Size (kB): {index_size}\n')



if __name__ == "main":
    inverted = build_inverted_index()
    # write_report(inverted)`