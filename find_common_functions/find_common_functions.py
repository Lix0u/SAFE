import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1]))
from find_function.improved_SAFE import SAFE
from sklearn.metrics.pairwise import cosine_similarity
import json
import psutil

sys.path.append(str(Path(__file__).parents[1]))

output_file = "find_common_functions/common_functions_warzone_vscode_debug.json"

safe = SAFE("data/safe.pb")

debug = True

folder = "database_sample/warzone_vscode"

def kill_radare_process():
        for proc in psutil.process_iter():
            if proc.name() == "radare2" and proc.ppid() == os.getpid():
                proc.kill()

common_functions = {}
common_functions_no_embedding = {}

files = os.listdir(folder)
files.sort()
files = [os.path.join(folder, file) for file in files]
for file in files:
    print(file)
    embeddings = safe.get_embeddings_instruction_threshold(file, 25)
    kill_radare_process()
    for val in embeddings:
        embedding = embeddings[val]["embedding"]
        address = embeddings[val]["address"]
        found = False
        for func in common_functions:
            if round(cosine_similarity(embedding, common_functions[func]["embedding"])[0][0], 3) >= 1:
                if debug:
                    common_functions[func]["address"].append(file.split('/')[-1]+':'+hex(address))
                    common_functions_no_embedding[func]["address"].append(file.split('/')[-1]+':'+hex(address))
                common_functions[func]["count"] += 1
                common_functions_no_embedding[func]["count"] += 1
                found = True
                break
        if not found:
            if debug:
                common_functions[file.split('/')[-1]+':'+hex(address)] = {"embedding": embedding,"n_instr": embeddings[val]["n_instructions"], "count":1, "address": [file.split('/')[-1]+':'+hex(address)]}
                common_functions_no_embedding[file.split('/')[-1]+':'+hex(address)] = {"n_instr": embeddings[val]["n_instructions"], "count":1, "address": [file.split('/')[-1]+':'+hex(address)]}
            else:
                common_functions[file.split('/')[-1]+':'+hex(address)] = {"embedding": embedding,"n_instr": embeddings[val]["n_instructions"], "count": 1}
                common_functions_no_embedding[file.split('/')[-1]+':'+hex(address)] = {"n_instr": embeddings[val]["n_instructions"], "count": 1}
    json.dump(common_functions_no_embedding, open(output_file, "w"), indent=4)
#sort by count and n_instr
common_functions = dict(sorted(common_functions_no_embedding.items(), key=lambda x: (x[1]["count"], x[1]["n_instr"]), reverse=True))
json.dump(common_functions_no_embedding, open(output_file, "w"), indent=4)