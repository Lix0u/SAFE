from SAFE.find_function.improved_SAFE import SAFE
from argparse import ArgumentParser
from SAFE.find_function.manage_db.db_manager import JsonManager
from SAFE.asm_embedding.FunctionAnalyzerRadare import RadareFunctionAnalyzer

# bytes ffor the pattern matching
murmurhash = b"\x55\x8b\xec\x53\x8b\xda\x8b\xc3\x99\x83\xe2\x03\x56\x57\x8d\x3c\x02\x8b\x55\x08\xc1\xff\x02\x8d\x34\xb9\xf7\xdf\x74\x23\x69\x04\xbe\x51\x2d\x9e\xcc\xc1\xc0\x0f\x69\xc0\x93\x35\x87\x1b\x33\xc2\xc1\xc0\x0d\x6b\xd0\x05\x81\xea\x9c\x94\xab\x19\x83\xc7\x01\x75\xdd\x8b\xc3\x33\xc9\x83\xe0\x03\x83\xe8\x01\x74\x1a\x83\xe8\x01\x74\x0c\x83\xe8\x01\x75\x26\x0f\xb6\x4e\x02\xc1\xe1\x10\x0f\xb6\x46\x01\xc1\xe0\x08\x33\xc8\x0f\xb6\x06\x33\xc1\x69\xc0\x51\x2d\x9e\xcc\xc1\xc0\x0f\x69\xc0\x93\x35\x87\x1b\x33\xd0\x33\xd3\x8b\xc2\xc1\xe8\x10\x33\xc2\x69\xc8\x6b\xca\xeb\x85\x5f\x5e\x5b\x8b\xc1\xc1\xe8\x0d\x33\xc1\x69\xc0\x35\xae\xb2\xc2\x8b\xc8\xc1\xe9\x10\x33\xc8\x8b\x45\x0c\x89\x08\x5d"
murmurhash2 = b"\x55\x8b\xec\x83\xec\x2c\x8b\x45\x08\x89\x45\xe0\x8b\x45\x0c\x99\x83\xe2\x03\x03\xc2\xc1\xf8\x02\x89\x45\xec\x8b\x45\x10\x89\x45\xf8\xc7\x45\xd8\x51\x2d\x9e\xcc\xc7\x45\xd4\x93\x35\x87\x1b\x8b\x45\xec\x8b\x4d\xe0\x8d\x04\x81\x89\x45\xdc\x8b\x45\xec\xf7\xd8\x89\x45\xf0\xeb\x07\x8b\x45\xf0\x40\x89\x45\xf0\x83\x7d\xf0\x00\x74\x59\xff\x75\xf0\xff\x75\xdc\xe8\x59\x2d\xfe\xff\x59\x59\x89\x45\xf4\x69\x45\xf4\x51\x2d\x9e\xcc\x89\x45\xf4\x6a\x0f\xff\x75\xf4\xe8\x1e\x2d\xfe\xff\x59\x59\x89\x45\xf4\x69\x45\xf4\x93\x35\x87\x1b\x89\x45\xf4\x8b\x45\xf8\x33\x45\xf4\x89\x45\xf8\x6a\x0d\xff\x75\xf8\xe8\xfc\x2c\xfe\xff\x59\x59\x89\x45\xf8\x6b\x45\xf8\x05\x2d\x9c\x94\xab\x19\x89\x45\xf8\xeb\x9a\x8b\x45\xec\x8b\x4d\xe0\x8d\x04\x81\x89\x45\xe4\x83\x65\xfc\x00\x8b\x45\x0c\x83\xe0\x03\x89\x45\xe8\x83\x7d\xe8\x01\x74\x39\x83\x7d\xe8\x02\x74\x1d\x83\x7d\xe8\x03\x74\x02\xeb\x6a\x33\xc0\x40\xd1\xe0\x8b\x4d\xe4\x0f\xb6\x04\x01\xc1\xe0\x10\x33\x45\xfc\x89\x45\xfc\x33\xc0\x40\xc1\xe0\x00\x8b\x4d\xe4\x0f\xb6\x04\x01\xc1\xe0\x08\x33\x45\xfc\x89\x45\xfc\x33\xc0\x40\x6b\xc0\x00\x8b\x4d\xe4\x0f\xb6\x04\x01\x33\x45\xfc\x89\x45\xfc\x69\x45\xfc\x51\x2d\x9e\xcc\x89\x45\xfc\x6a\x0f\xff\x75\xfc\xe8\x6a\x2c\xfe\xff\x59\x59\x89\x45\xfc\x69\x45\xfc\x93\x35\x87\x1b\x89\x45\xfc\x8b\x45\xf8\x33\x45\xfc\x89\x45\xf8\x8b\x45\xf8\x33\x45\x0c\x89\x45\xf8\xff\x75\xf8\xe8\x71\x2c\xfe\xff\x59\x89\x45\xf8\x8b\x45\x14\x8b\x4d\xf8\x89\x08\xc9"
findstart = b"\x55\x8b\xec\x83\xec\x14\xc6\x45\xff\x00\xc7\x45\xf4\x90\x1d\x42\x00\xc6\x45\xf8\x4d\xc6\x45\xf9\x5a\xc6\x45\xfa\x90\xc6\x45\xfb\x00\x83\x65\xf0\x00\x0f\xb6\x45\xff\x85\xc0\x75\x42\x6a\x04\xff\x75\xf4\x8d\x45\xf8\x50\xe8\x12\xf5\xfd\xff\x83\xc4\x0c\x89\x45\xec\x83\x7d\xec\x00\x75\x0b\xc6\x45\xff\x01\x8b\x45\xf4\xeb\x21\xeb\x07\x8b\x45\xf4\x48\x89\x45\xf4\x8b\x45\xf0\x40\x89\x45\xf0\x81\x7d\xf0\xe8\x03\x00\x00\x75\x04\x83\x65\xf0\x00\xeb\xb6\x33\xc0\xc9"
findstart2 = b"\x55\x8b\xec\x51\xb9\x0e\x5c\x41\x00\xc7\x45\xfc\x4d\x5a\x90\x00\x8d\x45\xfc\x8b\x00\x3b\x01\x74\x03\x49\xeb\xf4\x8b\xc1\xc9"
findstart3 = b"\x55\x8b\xec\x51\x53\x56\xbe\x23\x33\x41\x00\xc7\x45\xfc\x4d\x5a\x90\x00\x33\xdb\x6a\x04\x8d\x45\xfc\x56\x50\xe8\xbd\xdc\xfe\xff\x83\xc4\x0c\x85\xc0\x74\x13\x33\xc9\x8d\x43\x01\x4e\x81\xfb\xe7\x03\x00\x00\x0f\x45\xc8\x8b\xd9\xeb\xda\x8b\xc6\x5e\x5b\xc9"
findstart4 = b"\x55\x8b\xec\x51\x53\x56\xbe\xa2\x1c\x41\x00\xc7\x45\xfc\x4d\x5a\x90\x00\x33\xdb\x6a\x04\x8d\x45\xfc\x56\x50\xe8\x3e\xf3\xfe\xff\x83\xc4\x0c\x85\xc0\x74\x13\x33\xc9\x8d\x43\x01\x4e\x81\xfb\xe7\x03\x00\x00\x0f\x45\xc8\x8b\xd9\xeb\xda\x8b\xc6\x5e\x5b\xc9"
findstart5 = b"\x55\x8b\xec\x51\xb9\xe5\x17\x42\x00\xc7\x45\xfc\x4d\x5a\x90\x00\x8d\x45\xfc\x8b\x00\x3b\x01\x74\x03\x49\xeb\xf4\x8b\xc1\xc9"


def save_address(name, address):
    if name not in db_manager.get_all_names():
        db_manager.add(name, address)
    db_manager.save()


if __name__ == "__main__":
    parser = ArgumentParser(description="Safe Embedder")
    parser.add_argument(
        "-m", "--model", dest="model", required=True, help="Model to use for embedding"
    )
    parser.add_argument(
        "-n",
        "--name",
        dest="name",
        required=True,
        help="Name of the function to add to the database or to compare",
    )
    parser.add_argument(
        "-db", "--database", dest="db", required=True, help="Database path"
    )
    parser.add_argument(
        "-e",
        "--executable",
        dest="executable",
        required=True,
        help="Executable to analyze",
    )

    args = parser.parse_args()
    ######################################
    #################SAFE#################
    ######################################

    safe = SAFE(args.model)
    db_manager = JsonManager(args.db)
    if (embedding := db_manager.get(args.name)) is None:
        # add a case where we check the executable against all the db?
        print(f"Function {args.name} not found in the database")
        exit(1)
    else:
        similarity_safe, function_address_safe = safe.check_executable(
            embedding, args.executable
        )

    print(
        f"Similarity SAFE : {similarity_safe[0][0]}, {args.name}, {hex(function_address_safe)}"
    )

    ######################################
    ##########PATTERN MATCHING############
    ######################################

    # open the db to store the functions and their addresses
    db_name = "db_addresses.json"
    db_manager = JsonManager(db_name)

    analyzer = RadareFunctionAnalyzer(args.executable, use_symbol=False, depth=0)
    functions = analyzer.find_functions_boudaries()
    for function in functions:
        min_bound = function["minbound"]
        max_bound = function["maxbound"] - 1
        # get the bytes of the function in hex
        function_bytes = analyzer.r2.cmdj(f"pxj {max_bound - min_bound} @ {min_bound}")
        b = bytes(function_bytes)
        if args.name == "warzone_0x411bf8":  # function corresponding to murmurhash
            if murmurhash == b:
                save_address(
                    args.executable.split("/")[-1] + "_murmurhash", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, murmurhash")
                break
            if murmurhash2 == b:
                save_address(
                    args.executable.split("/")[-1] + "_murmurhash", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, murmurhash2")
                break
        elif args.name == "warzone_0x411ca2":  # function corresponding to findstart
            if findstart == b:
                save_address(
                    args.executable.split("/")[-1] + "_findstart", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, findstart")
                break
            if findstart2 == b:
                save_address(
                    args.executable.split("/")[-1] + "_findstart", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, findstart2")
                break
            if findstart3 == b:
                save_address(
                    args.executable.split("/")[-1] + "_findstart", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, findstart3")
                break
            if findstart4 == b:
                save_address(
                    args.executable.split("/")[-1] + "_findstart", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, findstart4")
                break
            if findstart5 == b:
                save_address(
                    args.executable.split("/")[-1] + "_findstart", hex(min_bound)
                )
                print(f"Similarity pattern matching : 1.0, findstart5")
                break
        else:
            print(f"no pattern matching for {args.name}")
            break