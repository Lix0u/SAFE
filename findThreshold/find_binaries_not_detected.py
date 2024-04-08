import os
import json
#TODO: fix path

# murmurhash1 = json.load(open("outputs/warzone_murmurhash_threshold3_6e1475.json","r"))
#murmurhash1 = json.load(open("findThreshold/output_find_best_signature/0b798bd.json","r"))
rc4_1= json.load(open("findThreshold/outputs/warzone_rc4_d56567.txt","r"))
found = []
print("number of match : " + str(len(rc4_1["0.98"])))
print("number of samples : " + str(len(os.listdir("database_sample/warzone"))))
for n in rc4_1["1"]:
    found.append(n.split(":")[0])
for file in os.listdir("database_sample/warzone"):
    if file not in found:
        print(file)