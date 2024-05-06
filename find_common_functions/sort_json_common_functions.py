#sort json file by number of instructions and count
import json
from rich import print as rprint
import numpy as np

from matplotlib.pylab import f

file = open("find_common_functions/common_functions_warzone_debug.json", "r")
data = json.load(file)
file.close()

def sort_by_count(data):
    rprint([type(x) for x in data.values()])
    return sorted(data.values(), key=lambda x: x['count'], reverse=True)

def sort_by_instructions(data):
    return sorted(data, key=lambda x: x['n_instr'], reverse=True)

def sort(data):
    d = sort_by_count(data)
    d = sort_by_instructions(d)
    return d

def sort_better(data):
    #sort by count*n_instr
    return sorted(data.values(), key=lambda x: x['count']*np.sqrt(x['n_instr']), reverse=True)

data = sort_better(data)
json.dump(data, open("find_common_functions/common_functions_warzone_debug_sorted2.json", "w"), indent=4)