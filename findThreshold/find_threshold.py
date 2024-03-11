import os
import numpy as np
from argparse import ArgumentParser

from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

from find_function.improved_SAFE import SAFE
import json
from sklearn.metrics.pairwise import cosine_similarity

#TODO : fix path

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-f","--folder", help="Folder containing the executables", required=True)
    arg_parser.add_argument("-n", "--name", dest="name", required=False, help="Name of the db file", default="data.json")
    args = arg_parser.parse_args()
    safe = SAFE("data/safe.pb") #TODO check this path
    if os.path.exists('data/'+args.name): #TODO check this path
        with open('data/'+args.name, 'r') as f: #TODO check this path
            data = json.load(f)
    else:
        data = {}
    first_file = True
    folders = args.folder.split(',')
    for folder in folders:
        for file in os.listdir(args.folder):
            print ("Processing file: " + file)
            if first_file:
                first_file = False
                embeddings = safe.get_embeddings(args.folder + "/" + file)
                thresh = {1:[], 0.98:[], 0.95:[], 0.93:[], 0.90:[]}
                for embedding in embeddings.keys():
                    embeddings[embedding].update(thresh)
                    embeddings[embedding]['embedding'] = embeddings[embedding]['embedding']
                    data[embedding] = embeddings[embedding]
            else:
                embeddings = safe.get_embeddings(args.folder + "/" + file)
                for embedding in embeddings.keys():
                    for d in data.keys():
                        sim = cosine_similarity(np.array(embeddings[embedding]['embedding']), np.array(data[d]['embedding']))
                        for threshold in thresh.keys():
                            if sim >= threshold:
                                data[d][threshold].append(file+':'+hex(embeddings[embedding]['address']))
                json.dump(data, open(args.name, 'w'), indent=4) #TODO check this path

    #remove all the functions that are too small and have too many matches
    n_files = len(os.listdir(args.folder))
    keys = list(data.keys())
    for d in keys:
        if len(data[d][1]) > n_files:
            del data[d]