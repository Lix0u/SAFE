import os
import numpy as np
from argparse import ArgumentParser
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from find_function.improved_SAFE import SAFE
import json
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-f', '--folder', help='Folder containing the sample of binaries', required=True)
    arg_parser.add_argument('-b', '--binary', help='Binary containing the function for which the threshold is to be found', required=True)
    arg_parser.add_argument('-a', '--address', help='Address of the function for which the threshold is to be found', required=True)
    arg_parser.add_argument('-o', '--output', help='Output file', required=True)
    args = arg_parser.parse_args()
    
    folder = args.folder
    #check if the folder exists
    if not os.path.exists(folder):
        print('Folder does not exist')
        exit(1)
    binary = args.binary
    #check if the binary exists
    if not os.path.exists(os.path.join(folder, binary)):
        print('Binary does not exist')
        exit(1)
    address = int(args.address,16)
    output = args.output
    
    safe = SAFE("data/safe.pb")
    thresholds = {1: [], 0.98: [], 0.95: [], 0.93: [], 0.90: []}
    embedding = safe.embedd_function(os.path.join(folder, binary), address)
    for file in os.listdir(folder):
        print("Processing file: " + file)
        embeddings = safe.get_embeddings(os.path.join(folder, file))
        for emb in embeddings.keys():
            sim = cosine_similarity(np.array(embedding), np.array(embeddings[emb]['embedding']))
            for threshold in thresholds.keys():
                if sim >= threshold:
                    thresholds[threshold].append(file + ':' + hex(embeddings[emb]['address']))
                    break
        json.dump(thresholds, open(output, 'w'), indent=4)
    for threshold in thresholds.keys():
        print("Threshold " + str(threshold) + " has " + str(len(thresholds[threshold])) + " matches")
    
    
    