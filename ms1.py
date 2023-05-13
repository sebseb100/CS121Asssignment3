#The following contain imports os: allows for interaction with operating system, for our case interacting with the file system.
#json: allows us to read and handle json files, decode them, load them in as data we can work with like strings.
#BeautifulSoup: Provides a way to extract data from HTML documents, used for web scraping traditionally. 
#re: Regex, regular expressions, can be used to search manipulate, replace, filter, manipulate strings. (Text from our html data)
#defaultdict: if you try and access a key that does not exist it will automatically create the key and assign it a default value
#PoterStemmer: from a Natural Language Processing Library, PorterStemmer used for keyword extraction, text normalization, reduces words to base form
import os 
import json 
from bs4 import BeautifulSoup
import re 
from collections import defaultdict
from nltk.stem import PorterStemmer

#Creates a file path by joining the current directory "os.getcwd()" and 'DEV' the name of the file of JSONs we're working with
json_file = os.path.join(os.getcwd(), 'DEV')

#Initialize variables to keep track of the number of files and size of index for report purposes 
file_counter = 0
index_size = 0

#Method used to build the inverted index
def build_inverted_index():

    #establish variables as global variables within the given scope of the method 
    global file_counter, index_size

    #initialize an ivnverted index variable that is a defaultdict with lists as values 
    inverted_index = defaultdict(list)

    #1)os.walk() used to iterate over all the files in the directory specified by the json_file
    #The method returns a tuple containing the current directory, a list of subdirectories, and a list of files in the current directory.
    
    #2)Iterating over the list of files returned, we pring the file, and then increment the file_counter 
    
    #3)If the file ends with '.json' then we try to obtain the current file bath using os.path.join as described previously
    
    #4)We open that file for reading purposes and store it as a temporary variable within the context manager f
    
    #5)We then use our json.load() method will load our json contents into a dictionairy, then extract its 'content' (text
    # that is actually on the html page rather than other descriptors) using the BeautifulSoup library object, we store this in 'text'
    
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

    #6) Now that we've obtained the text we use the REGEX Library to extract all tokens from our lowercased 'text' string variable
    # the criteria is all alphanumeric sequences with a length of 3 or greater
    
    #7) We store the unique tokens by calling set() on tokens that removes all duplicates 
    
    #8) We then loop through each of the unique tokens and, using our defaultdict we append token counts to our token (a key)
    # with relevance to the file name, if token isn't a key, not to worry, this is a default dictionairy, it'll create one
    
    #9) If all that was described in steps 4-8 doesn't work, then we simply catch the exception and print "BAD FILE"

    #10)We use our write_report method and hand it the the inverted_index dictionairy for processing within that method
    
    #11)We return the inverted_index dict
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

#Method takes a argument inverted_dic, opens a file called 'inverted_index.json' in writing mode 'w', now that the json is 
#available to be written into as f we take the inverted_dic dictionairy and dumps/writes it into the file f, thereby 
#converting the dictionairy to a json string 
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

#As soon as the program runs we call the build_inverted_index function that works with our DEV file and writes its 
# processed data into the report
if __name__ == "main":
    inverted = build_inverted_index()
    # write_report(inverted)`