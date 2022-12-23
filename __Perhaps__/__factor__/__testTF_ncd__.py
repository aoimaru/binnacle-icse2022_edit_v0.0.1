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
TEST_CASE_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__"
TEST_CASE_TF_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCaseTF__"

def ncd(x,y):
    if x == y:
        return 0
    z_x = len(zlib.compress(bytes(x, "utf8")))
    z_y = len(zlib.compress(bytes(y, "utf8")))
    z_xy = len(zlib.compress(bytes(x + y, "utf8")))    
    return float(z_xy - min(z_x, z_y)) / max(z_x, z_y)


#文字列`X`と`Y`の間のレーベンシュタイン距離を見つける関数。
def dist(X, Y):
    #`m`と`n`は、それぞれ`X`と`Y`の文字の総数です。
    (m, n) = (len(X), len(Y))
 
    # `i`と`j`のすべてのペアについて、 `T[i、j]`はレーベンシュタイン距離を保持します
    # `X`の最初の`i`文字と`Y`の最初の`j`文字の間の#。
    #`T`は`(m + 1)×(n + 1)`の値を保持することに注意してください。
    T = [[0 for x in range(n + 1)] for y in range(m + 1)]
 
    #によって、ソースプレフィックスを空の文字列に変換できます。
    #はすべての文字を削除します
    for i in range(1, m + 1):
        T[i][0] = i                    #(ケース1)
 
    #空のソースプレフィックスからターゲットプレフィックスに到達できます
    # すべての文字を挿入することによる
    for j in range(1, n + 1):
        T[0][j] = j                    #(ケース1)
 
    #はボトムアップ方式でルックアップテーブルを埋めます
    for i in range(1, m + 1):
 
        for j in range(1, n + 1):
            nc = ncd(X[i-1], Y[j-1])
            if nc <= 0.9:           #(ケース2)
                cost = 0                        #(ケース2)
            else:
                cost = 1                        #(ケース3c)
 
            T[i][j] = min(T[i - 1][j] + 1,      #の削除(ケース3b)
                        T[i][j - 1] + 1,        #挿入(ケース3a)
                        T[i - 1][j - 1] + cost) #交換(ケース2 + 3c)
 
    return T[m][n]

def main():
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
    

    total = list()

    for test_case in test_cases:
        print()
        print("test_case:", test_case)
        test_case_path = "{}/{}.json".format(TEST_CASE_TF_PATH, test_case)
        with open(test_case_path, mode="r") as f:
            contents = json.load(f)
        test = contents["test_case"]

        test_sequence = list()
        for tt in test["children"]:
            astCommand = AstCleaner._sort_by_asc(tt)
            test_sequence.append(json.dumps(astCommand))

        edit_distances = list()

        cases = contents["case"]
        for case in tqdm.tqdm(cases):
            case_sequence = list()
            for astCommand in case["content"]["children"]:
                astCommand = AstCleaner._sort_by_asc(astCommand)
                case_sequence.append(json.dumps(astCommand))
            edit_distances.append(
                {
                    "caseId": case["caseId"],
                    "answer": case["answer"],
                    "distance": case["distance"],
                    "ncd_distance": dist(test_sequence, case_sequence)/max(len(test_sequence), len(case_sequence))*1.00
                }
            )

        edit_distances = sorted(edit_distances, key=lambda x:x["ncd_distance"])

        count = 0
        for edit_distance in edit_distances[:10]:
            print("caseId", "ID:{}".format(edit_distance["caseId"]).ljust(7), "ncd_distance:", str(edit_distance["ncd_distance"]).ljust(20), "distance:", str(edit_distance["distance"]).ljust(20))
            if edit_distance["answer"]==1:
                count += 1
        
        print("answer:{}%".format(count/10*100))
        total.append(count/10*100)

    print()
    print("total:{}%".format(sum(total)/len(total)))

            







            


if __name__ == "__main__":
    main()