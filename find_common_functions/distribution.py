# find the distribution of the number of instructions in the functions of the given binary
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))
from asm_embedding.FunctionAnalyzerRadare import RadareFunctionAnalyzer

binary = "database_sample/wabot-christophe/9ca786e161159f6fb7aead62db463e5f2b42c7a3c3f6e1126d9462ca039cca47.exe"

analyzer = RadareFunctionAnalyzer(binary, use_symbol=False, depth=0)
functions = analyzer.analyze()

n_instructions = list(map(lambda x: len(x["filtered_instructions"]), functions.values()))

#create graph
import matplotlib.pyplot as plt
import numpy as np

plt.hist(n_instructions, bins=np.arange(0, max(n_instructions), 1), alpha=0.75)
plt.title("Distribution of the number of instructions in the functions")
plt.xlabel("Number of instructions")
plt.ylabel("Number of functions")

plt.savefig("distribution.png")
plt.clf()


# remove all functions with less than 10 instructions
filtered_functions = list(filter(lambda x: len(x["filtered_instructions"]) > 25, functions.values()))
filtered_n_instructions = list(map(lambda x: len(x["filtered_instructions"]), filtered_functions))
plt.hist(filtered_n_instructions, bins=np.arange(0, max(filtered_n_instructions), 1), alpha=0.75)
plt.title("Distribution of the number of instructions in the functions (filtered)")
plt.xlabel("Number of instructions")
plt.ylabel("Number of functions")

plt.savefig("filtered_distribution.png")

#print the number of functions
print(len(functions))
print(len(filtered_functions))