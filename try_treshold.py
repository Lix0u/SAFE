from matplotlib.pylab import f
import numpy as np
from SAFE.improved_SAFE import SAFE
from argparse import ArgumentParser
from SAFE.find_function.manage_db.db_manager import JsonManager

if __name__ == "__main__":
    parser = ArgumentParser(description="Safe Embedder")
    parser.add_argument(
        "-m", "--model", dest="model", required=True, help="Model to use for embedding"
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

    tresholds = [0.98, 0.95, 0.93, 0.9, 0.87, 0.85]

    args = parser.parse_args()

    ######################################
    
    functions_found = [[] for _ in range(len(tresholds) + 1)]
    safe = SAFE(args.model)
    db_manager = JsonManager(args.db)
    for name in db_manager.get_all_names():
        similarity_safe, function_address_safe = safe.check_executable(
            db_manager.get(name), args.executable
        )
        found = False
        for i, treshold in enumerate(tresholds):
            if similarity_safe[0][0] > treshold:
                found = True
                functions_found[i].append((name,hex(function_address_safe), similarity_safe[0][0]))
                break
        if not found:
            functions_found[-1].append((name,hex(function_address_safe), similarity_safe[0][0]))
    for i, treshold in enumerate(tresholds):
        print(f"Functions found with treshold {treshold} : {functions_found[i]}")
