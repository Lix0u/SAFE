import sys
from pathlib import Path

from matplotlib.pylab import f
sys.path.append(str(Path(__file__).resolve().parents[1]))
from find_function.improved_SAFE import SAFE
from find_threshold3 import find_threshold
from argparse import ArgumentParser
import json
from sklearn.metrics.pairwise import cosine_similarity
import psutil


starting_binary = "database_sample/warzone/d565677b0818122a241235109dc8ed5b69983f0fb231dabe683516ff3078cbff.exe"
starting_address = "0x405f10"
folder = "database_sample/warzone"
output_folder = "findThreshold/output_find_best_signature_copy"

def find_best_signature():
    search_stack = [[starting_binary, starting_address]]
    searched_binary = []
    best_signature = ""
    best_signature_count = 0
    while search_stack:
        current_binary, current_address = search_stack.pop(0)
        current_address = int(current_address, 16)
        output_file = output_folder+"/"+current_binary.split("/")[-1][:7]+".json"
        searched_binary.append(current_binary.split("/")[-1])
        threshold = find_threshold(folder, current_binary.split("/")[-1], current_address, output_file, True)
        #get the number of matches over the threshold
        with open(output_file) as f:
            data = json.load(f)
            for t in data:
                if float(t) >= threshold:
                    if len(data[t]) > best_signature_count:
                        best_signature = current_binary
                        best_signature_count = len(data[t])
                    for match in data[t]:
                        if match.split(":")[0] not in searched_binary:
                            search_stack.append([folder+"/"+match.split(":")[0], match.split(":")[1]])
    print(best_signature, best_signature_count)

if __name__ == "__main__":
    find_best_signature()