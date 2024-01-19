# SAFE TEAM
# Copyright (C) 2019  Luca Massarelli, Giuseppe Antonio Di Luna, Fabio Petroni, Leonardo Querzoni, Roberto Baldoni

from sklearn.metrics.pairwise import cosine_similarity
from asm_embedding.FunctionAnalyzerRadare import RadareFunctionAnalyzer
from argparse import ArgumentParser
from asm_embedding.FunctionNormalizer import FunctionNormalizer
from asm_embedding.InstructionsConverter import InstructionsConverter
from neural_network.SAFEEmbedder import SAFEEmbedder
from utils import utils

class SAFE:

    def __init__(self, model):
        self.converter = InstructionsConverter("data/i2v/word2id.json")
        self.normalizer = FunctionNormalizer(max_instruction=150)
        self.embedder = SAFEEmbedder(model)
        self.embedder.loadmodel()
        self.embedder.get_tensor()

    """
        returns the embedding vector
    """
    def embedd_function(self, filename, address):
        analyzer = RadareFunctionAnalyzer(filename, use_symbol=False, depth=0) 
        functions = analyzer.analyze()
        instructions_list = None
        for function in functions:
            if functions[function]['address'] == address:
                instructions_list = functions[function]['filtered_instructions']
                break
        if instructions_list is None:
            print("Function not found")
            return None
        converted_instructions = self.converter.convert_to_ids(instructions_list)
        instructions, length = self.normalizer.normalize_functions([converted_instructions])
        embedding = self.embedder.embedd(instructions, length)
        return embedding

    def check_executable(self, function_embedding, executable):
        max_similarity = 0
        address = 0
        analyzer = RadareFunctionAnalyzer(executable, use_symbol=False, depth=0) 
        functions = analyzer.analyze()
        print(functions)
        instructions_list = None
        for function in functions:
            print("address: ", hex(functions[function]['address']))
            instructions_list = functions[function]['filtered_instructions']
            converted_instructions = self.converter.convert_to_ids(instructions_list)
            instructions, length = self.normalizer.normalize_functions([converted_instructions])
            embedding = self.embedder.embedd(instructions, length)
            sim = cosine_similarity(embedding, function_embedding)   
            print(sim)
            if sim > max_similarity:
                max_similarity = sim
                address = functions[function]['address']     
        if instructions_list is None:
            print("Function not found")
            return None
        
        return max_similarity, address

if __name__ == '__main__':

    utils.print_safe()

    parser = ArgumentParser(description="Safe Embedder")

    parser.add_argument("-m", "--model",   help="Safe trained model to generate function embeddings")
    parser.add_argument("-e", "--executable",   help="Executable to compare the function embedding")
    parser.add_argument("-f", "--function",   help="executable function that contains the function to embedd and compare to the other executable")
    parser.add_argument("-a", "--address", help="Hexadecimal address of the function to embedd")

    args = parser.parse_args()

    address = int(args.address, 16)
    safe = SAFE(args.model)
    embedding = safe.embedd_function(args.function, address)
    similarity, function_address = safe.check_executable(embedding, args.executable)
    #print(embedding[0])
    print(similarity)
    print(hex(function_address))
