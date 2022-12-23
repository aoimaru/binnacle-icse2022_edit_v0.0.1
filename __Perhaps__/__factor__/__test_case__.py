
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
import glob
import os

GOLD_JSON_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/json/gold"
GOLD_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/gold"
GITHUB_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/github"
GOLD_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/gold"
GITHUB_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/github"

VIMAGICK_DATA_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2020_doc2vec_v0.0.1/data/vimagick"
VIMAGICK_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/vimagick"

PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"

TEST_CASE_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_lstm_v0.0.3/__testCase__"
TEST_CASE_TF_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_lstm_v0.0.3/__testCaseTF__"


def create_test_case():
    file_paths = JsonFile._get_file_paths(VIMAGICK_AST_ROOT_PATH)
    dumped_ast_commands = list()
    dumped_ast_commands_per_run_instruction_dictionaly = dict()

    print("loading contents...")
    for file_path in tqdm.tqdm(file_paths):
        contents = JsonFile._get_contents(file_path)
        for content in contents:
            run_instruction_id = ":".join(content["astCommandId"].split(":")[:-1])
            dumped = json.dumps(content["astCommand"])
            dumped_ast_commands.append(dumped)
            if not run_instruction_id in dumped_ast_commands_per_run_instruction_dictionaly:
                dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id] = list()
            dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id].append(dumped)
    print()

    with open("__testCase__.json", mode="r") as f:
        test_cases = json.load(f)
    
    print("creating test_case...")
    for test_case in tqdm.tqdm(test_cases):
        test_case_path = "{}/{}.json".format(TEST_CASE_PATH, test_case)
        test_obj = {
            "type": "ROOT",
            "children": []
        }
        for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            test_obj["children"].append(astCommand)

        created = list()
        for _ in range(10):
            created.append(ASTSeed._random(test_obj))
        
        writed = {
            "test_case": test_obj,
            "created_case": created
        }

        with open(test_case_path, mode="w") as f:
            json.dump(writed, f, indent=4)

def create_test_case_2():
    for file_path in glob.glob("{}/**/*.json".format(TEST_CASE_PATH), recursive=True):
        name = os.path.basename(file_path); 
        name = name.replace(".json", "")
        test_case_path = "{}/{}.json".format(TEST_CASE_TF_PATH, name)
        with open(file_path, mode="r") as f:
            contents = json.load(f)
        test_case = contents["test_case"]

        cases = list()
        caseId = 0
        for created in contents["created_case"]:
            distance = simple_distance(PQ_GramWrapper._zhang(test_case), PQ_GramWrapper._zhang(created))/max(len(test_case["children"]), len(created["children"]))*1.00
            cases.append(
                {
                    "caseId": caseId,
                    "answer": 1,
                    "distance": distance,
                    "content": created
                }
            )
            caseId += 1
        results = list()
        print()
        print("creating test_case... <path:{}>".format(test_case_path))
        for file_path in tqdm.tqdm(glob.glob("{}/**/*.json".format(TEST_CASE_PATH), recursive=True)):
            with open(file_path, mode="r") as f:
                contents = json.load(f)
            for created in contents["created_case"]:
                distance = simple_distance(PQ_GramWrapper._zhang(test_case), PQ_GramWrapper._zhang(created))/max(len(test_case["children"]), len(created["children"]))*1.00
                results.append(
                    {
                        "caseId": caseId,
                        "answer": 0,
                        "distance": distance,
                        "content": created,
                    }
                )
                caseId += 1
        results = sorted(results, key=lambda x:x["distance"], reverse=True)
        for result in results[:50]:
            cases.append(result)
    
        tight = {
            "test_case": test_case,
            "case": cases
        }

        with open(test_case_path, mode="w") as f:
            json.dump(tight, f, indent=4)

def main():
    create_test_case_2()


if __name__ == "__main__":
    main()