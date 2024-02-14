from argparse import ArgumentParser
from sklearn.metrics.pairwise import cosine_similarity
import os

path = os.getcwd()
print(path)

import sys
sys.path.append(path)

from safe import SAFE

if __name__ == '__main__':

    parser = ArgumentParser()

    parser.add_argument("-m", "--model",   help="Safe trained model to generate function embeddings")
    parser.add_argument("-i", "--input",   help="Input executable that contains the function to embedd")
    parser.add_argument("-a", "--address", help="Hexadecimal address of the function to embedd")

    args = parser.parse_args()

    address = int(args.address, 16)
    safe = SAFE(args.model)
    embedding1 = safe.embedd_function(args.input, address)
    embedding2 = safe.embedd_function(args.input, address)
    print(embedding1[0])
    print(embedding2[0])
    sim=cosine_similarity(embedding1,embedding2)
    print(sim)
