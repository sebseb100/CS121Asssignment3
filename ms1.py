import os 
import json 
from bs4 import BeautifulSoup
import re 
from collections import defaultdict

json_file = os.path.join(os.getcwd(), 'DEV')

file_counter = 0
index_size = 0

def build_inverted_index():
    global file_counter, index_size

    inverted_index = defaultdict(list)

    for cur, subdir, files in os.walk(json_file):
        for file in files:
            print(file)
            if file.endswith('.json'):
                cur_file_path = os.path.join(cur, file)
                with open(cur_file_path,'r') as f:
                    data = json.load(f)
                soup = BeautifulSoup(data['content'], 'html.parser')
                text = soup.get_text()

                tokens = re.findall(r"[a-zA-Z0-9]+", text.lower())
                undup_tokens = set(tokens)
                for token in undup_tokens:
                    inverted_index[token].append({'doc_id': file, "tf-dif": tokens.count(token)})
                file_counter += 1

                index_size_bytes = os.path.getsize(cur_file_path)
                index_size += (index_size_bytes/1024)

    with open('inverted_index.json', 'w') as f:
        json.dump(inverted_index, f)
    return inverted_index

def write_report(inverted_dic):
    global file_counter, index_size
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



if __name__ == "__main__":
    inverted = build_inverted_index()
    write_report(inverted)