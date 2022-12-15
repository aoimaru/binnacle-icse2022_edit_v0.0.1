import pickle
import pprint
import json
import numpy as np

from libs.files import *
from libs.d2v import *
from pqgrams_wrapper import *
from libs.contents import *
from libs.algorithms import *

import tqdm
from functools import lru_cache
import zlib
import random

from zss import simple_distance

GOLD_JSON_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/json/gold"
GOLD_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/gold"
GITHUB_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/github"
GOLD_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/gold"
GITHUB_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/github"

VIMAGICK_DATA_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2020_doc2vec_v0.0.1/data/vimagick"
VIMAGICK_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/vimagick"

PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"


def sampling_random_testCase():
    file_paths = JsonFile._get_file_paths(VIMAGICK_AST_ROOT_PATH)
    dumped_ast_commands = list()
    dumped_ast_commands_per_run_instruction_dictionaly = dict()
    print(" loading *.json ========>>> ")
    for file_path in tqdm.tqdm(file_paths):
        contents = JsonFile._get_contents(file_path)
        for content in contents:
            run_instruction_id = ":".join(content["astCommandId"].split(":")[:-1])
            dumped = json.dumps(content["astCommand"])
            dumped_ast_commands.append(dumped)
            if not run_instruction_id in dumped_ast_commands_per_run_instruction_dictionaly:
                dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id] = list()
            dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id].append(dumped)
    
    run_instruction_ids = [run_instruction_id for run_instruction_id in random.sample(dumped_ast_commands_per_run_instruction_dictionaly.keys(), 50)]
    
    with open("__testCase__.json", mode="w") as f:
        json.dump(run_instruction_ids, f, indent=4)


def check_sample_testCase():
    file_paths = JsonFile._get_file_paths(VIMAGICK_AST_ROOT_PATH)
    dumped_ast_commands = list()
    dumped_ast_commands_per_run_instruction_dictionaly = dict()
    print(" loading *.json ========>>> ")
    for file_path in tqdm.tqdm(file_paths):
        contents = JsonFile._get_contents(file_path)
        for content in contents:
            run_instruction_id = ":".join(content["astCommandId"].split(":")[:-1])
            dumped = json.dumps(content["astCommand"])
            dumped_ast_commands.append(dumped)
            if not run_instruction_id in dumped_ast_commands_per_run_instruction_dictionaly:
                dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id] = list()
            dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id].append(dumped)

    with open("__testCase__.json", mode="r") as f:
        test_cases = json.load(f)
    
    for dumped_id, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        if not dumped_id in test_cases:
            continue
        for dumped_ast_command in dumped_ast_commands:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            # pprint.pprint(astCommand)
    
    for item in dumped_ast_commands_per_run_instruction_dictionaly[test_cases[0]]:
        print(items)
    
def supply():
    file_paths = JsonFile._get_file_paths(VIMAGICK_AST_ROOT_PATH)
    dumped_ast_commands = list()
    dumped_ast_commands_per_run_instruction_dictionaly = dict()
    print(" loading *.json ========>>> ")
    for file_path in tqdm.tqdm(file_paths):
        contents = JsonFile._get_contents(file_path)
        for content in contents:
            run_instruction_id = ":".join(content["astCommandId"].split(":")[:-1])
            dumped = json.dumps(content["astCommand"])
            dumped_ast_commands.append(dumped)
            if not run_instruction_id in dumped_ast_commands_per_run_instruction_dictionaly:
                dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id] = list()
            dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id].append(dumped)

    with open("__testCase__.json", mode="r") as f:
        test_cases = json.load(f)
    
    S_1 = {
        "type": "ROOT",
        "children": []
    }

    test_case = test_cases[40]
    print(test_case)
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        S_1["children"].append(astCommand)
    
    pprint.pprint(S_1)

    tree_edit_distances = list()

    for dumped_id, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        if dumped_id==test_case:
            continue
        S_2 = {
            "type": "ROOT",
            "children": []
        }
        for dumped_ast_command in dumped_ast_commands:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            S_2["children"].append(astCommand)

        tree_edit_distances.append(
            {
                "dumpedId": dumped_id,
                "astCommands": S_2,
                "distance": simple_distance(PQ_GramWrapper._zhang(S_1), PQ_GramWrapper._zhang(S_2))/max(len(S_1["children"]), len(S_2["children"]))*1.00
            }
        )
    
    tree_edit_distances = sorted(tree_edit_distances, key=lambda x:x["distance"])

    for tree_edit_distance in tree_edit_distances:
        print(tree_edit_distance["dumpedId"].zfill(20), tree_edit_distance["distance"])
    






def main():
    # check_sample_testCase()
    supply()

if __name__ == "__main__":
    main()