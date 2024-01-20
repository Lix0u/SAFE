import imp
from arrow import get
from matplotlib.pylab import f
from numpy import add
from sklearn.metrics.pairwise import cosine_similarity
from asm_embedding.FunctionAnalyzerRadare import RadareFunctionAnalyzer
from argparse import ArgumentParser, BooleanOptionalAction
from asm_embedding.FunctionNormalizer import FunctionNormalizer
from asm_embedding.InstructionsConverter import InstructionsConverter
from neural_network.SAFEEmbedder import SAFEEmbedder
from utils import utils
from db_manager import JsonManager
import sys


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
        instructions_list = None
        embeddings = []
        for function in functions:
            instructions_list = functions[function]["filtered_instructions"]
            converted_instructions = self.converter.convert_to_ids(instructions_list)
            instructions, length = self.normalizer.normalize_functions(
                [converted_instructions]
            )
            embedding = self.embedder.embedd(instructions, length)
            embeddings.append(embedding)
        return embeddings

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


if __name__ == "__main__":
    # utils.print_safe()

    parser = ArgumentParser(description="Safe Embedder")

    parser.add_argument(
        "-m", "--model", dest="model", required=True, help="Model to use for embedding"
    )
    parser.add_argument(
        "-add",
        "--add",
        dest="add",
        action=BooleanOptionalAction,
        help="flag to add a function embedding to the database",
    )
    parser.add_argument(
        "-n",
        "--name",
        dest="name",
        required=False,
        help="Name of the function to add to the database or to compare",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        required=False,
        help="File that contains the function to embedd",
    )
    parser.add_argument(
        "-a",
        "--address",
        dest="address",
        required=False,
        help="Address of the function to embedd",
    )
    parser.add_argument(
        "-db", "--database", dest="db", required=False, help="Database path"
    )
    parser.add_argument(
        "-e",
        "--executable",
        dest="executable",
        required=False,
        help="Executable to analyze",
    )

    args = parser.parse_args()

    safe = SAFE(args.model)

    if args.add is None and args.executable is None:
        parser.error("Either -add or -e is required.")
    file = args.file
    if args.address is not None:
        address = int(args.address, 16)

    if args.db is None:
        db_path = "db.json"
    else:
        db_path = args.db

    db_manager = JsonManager(db_path)

    if args.add is not None:
        if args.file is None or args.address is None:
            parser.error(
                "-f or -a are required when adding a function embedding to the database."
            )
        if args.name in db_manager.get_all_names():
            print(
                "function"
                + args.name
                + " already in the database are you sure you want to overwrite it? (y/n)"
            )
            while True:
                answer = input()
                if answer == "y" or answer == "Y" or answer == "n" or answer == "N":
                    break
                print("please enter y or n")
            if answer != "y" and answer != "Y":
                sys.exit(1)
        embedding = safe.embedd_function(args.file, int(args.address, 16))
        safe.add_embedding_to_db(embedding, args.name, db_manager)
    else:
        if args.executable is None:
            parser.error("-e is required when comparing a function embedding.")
        if args.name is None:
            keys = db_manager.get_all_names()
            max_similarity = 0
            best_address = 0
            for key in keys:
                embedding = db_manager.get(key)
                similarity, function_address = safe.check_executable(
                    embedding, args.executable
                )
                if similarity[0][0] > max_similarity:
                    max_similarity = similarity[0][0]
                    best_address = function_address
            print(max_similarity)
            print(hex(best_address))
        else:
            if (embedding := db_manager.get(args.name)) is None:
                if args.file is None or args.address is None:
                    parser.error(
                        "-f or -a are required when comparing a function embedding if the function is not yet in the database."
                    )
                embedding = safe.embedd_function(file, address)
            similarity, function_address = safe.check_executable(
                embedding, args.executable
            )
            print(similarity[0][0])
            print(hex(function_address))
