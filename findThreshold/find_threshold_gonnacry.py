import os
import numpy as np
from argparse import ArgumentParser
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from find_function.improved_SAFE import SAFE
import json
from sklearn.metrics.pairwise import cosine_similarity
import psutil


def kill_radare_process():
    for proc in psutil.process_iter():
        if proc.name() == "radare2" and proc.ppid() == os.getpid():
            proc.kill()

def find_threshold(folder, binary, address, output, debug, minThreshold):
    safe = SAFE("data/safe.pb") 
    thresholds = {}
    minThreshold = float(minThreshold)
    if debug:
        # thresholds = {1: [], 0.98: [], 0.95: [], 0.93: [], 0.90: [],0.89:[],0.88:[]}
        for i in reversed(np.arange(minThreshold, 1.0, 0.01)):
            thresholds[round(i,2)] = []
    else:
        for i in reversed(np.arange(minThreshold, 1.0, 0.01)):
            thresholds[round(i,2)] = 0

    embedding = safe.embed_function( binary, address)
    if embedding is None:
        print("Function not found")
        exit(1)
    files = list(os.listdir(folder))
    files.sort()
    max_sim = 0
    for file in files:
        if file == binary:
            continue
        print("Processing file: " + file)
        best_sim = 0
        best_emb = None
        embeddings = safe.get_embeddings(os.path.join(folder, file))
        kill_radare_process()
        for emb in embeddings.keys():
            sim = cosine_similarity(np.array(embedding), np.array(embeddings[emb]['embedding']))
            if sim > max_sim:
                max_sim = sim
            if sim > best_sim:
                best_sim = sim
                best_emb = emb
        for threshold in thresholds.keys():
            if round(best_sim[0][0],3) >= threshold:
                if debug:
                    thresholds[threshold].append(file + ':' + hex(embeddings[best_emb]['address']))
                else:
                    thresholds[threshold] += 1
                break
        json.dump(thresholds, open(output, 'w'), indent=4)
    thresholds["max"] = max_sim[0][0]
    json.dump(thresholds, open(output, 'w'), indent=4)
    print ("Max similarity: " + str(max_sim))
    if debug:
        for threshold in thresholds.keys():
            print("Threshold " + str(threshold) + " has " + str(len(thresholds[threshold])) + " matches")
    max_thresh_found = False
    thresh = list(thresholds.keys())
    thresh.sort(reverse=True) # so that we can see where we are in the folder
    for threshold in thresh:
        if debug:
            count = len(thresholds[threshold])
        else:
            count = thresholds[threshold]
        if count > 0:
            if not max_thresh_found:
                final_threshold = threshold
                max_thresh_found = True
            else:
                break
        else:
            final_threshold = threshold
    print("Final threshold: " + str(final_threshold))
    return final_threshold

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-f', '--folder', help='Folder containing the sample of binaries', required=True)
    arg_parser.add_argument('-b', '--binary', help='Binary containing the function for which the threshold is to be found', required=True)
    arg_parser.add_argument('-a', '--address', help='Address of the function for which the threshold is to be found', required=True)
    arg_parser.add_argument('-o', '--output', help='Output file', required=True)
    arg_parser.add_argument('-t', '--minThreshold', help='Minimum threshold', required=False, default=0.88)
    arg_parser.add_argument('--debug', help='Debug mode', action='store_true')
    args = arg_parser.parse_args()
    
    folder = args.folder
    #check if the folder exists
    if not os.path.exists(folder):
        print('Folder does not exist')
        exit(1)
    binary = args.binary
    #check if the binary exists
    if not os.path.exists(binary):
        print('Binary does not exist')
        exit(1)
    address = int(args.address,16)
    output = args.output
    
    find_threshold(folder, binary, address, output, args.debug, args.minThreshold)