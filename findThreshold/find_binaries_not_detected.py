import os
import json
#TODO: fix path

# murmurhash1 = json.load(open("outputs/warzone_murmurhash_threshold3_6e1475.json","r"))
murmurhash1 = json.load(open("findThreshold/output_find_best_signature/0b798bd.json","r"))
found = []
print("number of match : " + str(len(murmurhash1["1"])))
print("number of samples : " + str(len(os.listdir("database_sample/warzone"))))
for n in murmurhash1["1"]:
    found.append(n.split(":")[0])
for file in os.listdir("database_sample/warzone"):
    if file not in found:
        print(file)