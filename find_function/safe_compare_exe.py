from sklearn.metrics.pairwise import cosine_similarity
from SAFE.asm_embedding.FunctionAnalyzerRadare import RadareFunctionAnalyzer
from argparse import ArgumentParser
from SAFE.asm_embedding.FunctionNormalizer import FunctionNormalizer
from SAFE.asm_embedding.InstructionsConverter import InstructionsConverter
from SAFE.neural_network.SAFEEmbedder import SAFEEmbedder
from SAFE.find_function.manage_db.db_manager import JsonManager
import os

class SAFE:
    def __init__(self, model):
        self.converter = InstructionsConverter("data/i2v/word2id.json") #TODO check this path
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
            if functions[function]["address"] == address:
                instructions_list = functions[function]["filtered_instructions"]
                break
        if instructions_list is None:
            print("Function not found")
            return None
        converted_instructions = self.converter.convert_to_ids(instructions_list)
        instructions, length = self.normalizer.normalize_functions(
            [converted_instructions]
        )
        embedding = self.embedder.embedd(instructions, length)
        return embedding

    def embedd_executable(self, filename):
        analyzer = RadareFunctionAnalyzer(filename, use_symbol=False, depth=0)
        functions = analyzer.analyze()
        embeddings = []
        for function in functions:
            instructions_list = functions[function]["filtered_instructions"]
            converted_instructions = self.converter.convert_to_ids(instructions_list)
            instructions, length = self.normalizer.normalize_functions(
                [converted_instructions]
            )
            embedding = self.embedder.embedd(instructions, length)
            embeddings.append([embedding, functions[function]["address"]])
        return embeddings

    def add_embedding_to_db(self, embbeding, name, file, address):
        e = embbeding.tolist() #TODO : change counter by a list
        self.db.add(name, {"embedding": e, "count_1": 0, "count_98": 0, "count_95": 0, "count_93": 0, "count_90": 0, "file": file, "address": address})

    def load_db(self, path):
        self.db = JsonManager(path)

    def add_embedding_to_db(self, embbeding, name, db_manager):
        db_manager.add(name, embbeding)

    def check_executable(self, function_embedding, executable):
        max_similarity = 0
        address = 0
        analyzer = RadareFunctionAnalyzer(executable, use_symbol=False, depth=0)
        functions = analyzer.analyze()
        instructions_list = None
        for function in functions:
            instructions_list = functions[function]["filtered_instructions"]
            converted_instructions = self.converter.convert_to_ids(instructions_list)
            instructions, length = self.normalizer.normalize_functions(
                [converted_instructions]
            )
            embedding = self.embedder.embedd(instructions, length)
            sim = cosine_similarity(embedding, function_embedding)
            if sim > max_similarity:
                max_similarity = sim
                address = functions[function]["address"]
        if instructions_list is None:
            print("Function not found")
            return None

        return max_similarity, address

if __name__ == '__main__':
    safe = SAFE("data/safe.pb")
    safe.load_db("db_exe.json")
    parser = ArgumentParser()
    parser.add_argument("-f","--folder", help="Folder containing the executables", required=True)

    args = parser.parse_args()

    for file in os.listdir(args.folder):
        print ("Processing file: " + file)
        safe.add_executable_to_db(args.folder + "/" + file)
        safe.db.save()
    print("test")