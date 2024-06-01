from operator import sub
import subprocess
folders = ['database_sample/warzone','database_sample/mirai']
files = [
    {'binary':'gonnacry_clang_O1',
     'address':'0x1b40',
     'output':'gonnacry_clang_O1_1b40'},
    {'binary':'gonnacry_gcc_O2',
     'address':'0x1f50',
     'output':'gonnacry_gcc_O2_1f50'},
    {'binary':'gonnacry_gcc_O2',
     'address':'0x18c0',
     'output':'gonnacry_gcc_O2_18c0'},
    {'binary':'gonnacry_clang_O1',
     'address':'0x1370',
     'output':'gonnacry_clang_O1_1370'},
    {'binary':'gonnacry_clang_O2',
     'address':'0x15b0',
     'output':'gonnacry_clang_O2_15b0'},
    {'binary':'gonnacry_clang_O2',
     'address':'0x1e40',
     'output':'gonnacry_clang_O2_1e40'},
    {'binary':'gonnacry_gcc_O2',
     'address':'0x22f0',
     'output':'gonnacry_gcc_O2_22f0'},
    {'binary':'gonnacry_clang_O2',
     'address':'0x1e10',
     'output':'gonnacry_clang_O2_1e10'},
    {'binary':'gonnacry_gcc_O2',
     'address':'0x2450',
     'output':'gonnacry_gcc_O2_2450'},
    {'binary':'gonnacry_gcc_O2',
     'address':'0x1540',
     'output':'gonnacry_gcc_O2_1540'}
]

for folder in folders:
    for file in files:
        family = folder.split('/')[-1]
        binary = file['binary']
        address = file['address']
        output = file['output']
        cmd = f'python3 findThreshold/find_threshold3.py -f {folder} -b database_sample/gonnacry/{binary} -a {address} -o findThreshold/outputs/{output}_{family}.json'
        print(cmd)
        subprocess.run(cmd.split(' '))