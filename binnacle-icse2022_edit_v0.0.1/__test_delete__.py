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
JESSFRAZ_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/jessfraz"
PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"

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
            if nc <= 0.1:           #(ケース2)
                cost = 0                        #(ケース2)
            else:
                cost = 1                        #(ケース3c)
 
            T[i][j] = min(T[i - 1][j] + 1,      #の削除(ケース3b)
                        T[i][j - 1] + 1,        #挿入(ケース3a)
                        T[i - 1][j - 1] + cost) #交換(ケース2 + 3c)        
 
    return T[m][n]

def main():
    file_paths = JsonFile._get_file_paths(VIMAGICK_AST_ROOT_PATH)
    # file_paths = JsonFile._get_file_paths(JESSFRAZ_AST_ROOT_PATH)
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
    
    test_case = "dante:0"
    # test_case = "taskd:0"
    # test_case = "phpvirtualbox:0"
    # test_case = "prestashop:2"
    # test_case = "webgoat:0"
    # test_case = "webdis:2"
    # test_case = "kcptun:0"
    # test_case = "snort:0"
    # test_case = "vnstat:0"
    # test_case = "mysql-proxy:0"
    # test_case = "kafka-manager:1"
    # test_case = "nextcloud:1"
    test_case = "nextcloud:2"
    # test_case = "mantisbt:2"
    # test_case = "dante:0"
    # test_case = "webgoat:0"
    # test_case = "kafka-manager:1"
    # test_case = "libev-arm:0"
    # test_case = "glances:0"
    test_obj = {
        "type": "ROOT",
        "children": []
    }

    test_ncd = list()

    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case][2:-1]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        test_obj["children"].append(astCommand)
        test_ncd.append(json.dumps(astCommand))
    
    pprint.pprint(test_obj)

    edit_distances = list()
    print("do...")
    for dumped_id, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        if dumped_id==test_case:
            continue
        sample_obj = {
            "type": "ROOT",
            "children": []
        }

        sample_ncd = list()

        for dumped_ast_command in dumped_ast_commands:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            sample_obj["children"].append(astCommand)
            sample_ncd.append(json.dumps(astCommand))

        edit_distances.append(
            {
                "dumpedId": dumped_id,
                "astCommands": sample_obj,
                "ncd_distance": dist(sample_ncd, test_ncd)/max(len(test_ncd), len(sample_ncd))*1.00,
                "simple_distance": simple_distance(PQ_GramWrapper._zhang(test_obj), PQ_GramWrapper._zhang(sample_obj))/max(len(test_obj["children"]), len(sample_obj["children"]))*1.00
            }
        )

    print()
    print("adding dummy...")
    for dummy_id in tqdm.tqdm(range(10)):
        sample_ncd = list()
        for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            astCommand = ASTSeed._random(
                content=astCommand,
                N=0.7,
                R=0.1,
                A=0.1,
                D=0.1,
                dummy=0.05
            )
            sample_obj["children"].append(astCommand)
            sample_ncd.append(json.dumps(astCommand))
        edit_distances.append(
            {
                "dumpedId": test_case+":dummy:{}".format(dummy_id),
                "astCommands": sample_obj,
                "ncd_distance": dist(sample_ncd, test_ncd)/max(len(test_ncd), len(sample_ncd))*1.00,
                "simple_distance": simple_distance(PQ_GramWrapper._zhang(test_obj), PQ_GramWrapper._zhang(sample_obj))/max(len(test_obj["children"]), len(sample_obj["children"]))*1.00
            }
        )

    
    edit_distances = sorted(edit_distances, key=lambda x:x["ncd_distance"])


    output_distances = dict()
    for edit_distance in edit_distances:
        if not edit_distance["ncd_distance"] in output_distances:
            output_distances[edit_distance["ncd_distance"]] = list()
        output_distances[edit_distance["ncd_distance"]].append(edit_distance)
    
    output_distances = sorted(output_distances.items(), key=lambda x:x[0])
    count = 0
    for output_distance in output_distances:
        edit_distances = sorted(output_distance[1], key=lambda x:x["simple_distance"])
        for edit_distance in edit_distances:
            if count >= 15:
                break
            # pprint.pprint(edit_distance["astCommands"])
            print(edit_distance["dumpedId"].ljust(20), edit_distance["ncd_distance"], edit_distance["simple_distance"])
            count += 1
            


if __name__ == "__main__":
    main()