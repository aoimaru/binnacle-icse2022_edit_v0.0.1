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
import zlib

GOLD_JSON_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/json/gold"
GOLD_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/gold"
GITHUB_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/github"
GOLD_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/gold"
GITHUB_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/github"

VIMAGICK_DATA_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2020_doc2vec_v0.0.1/data/vimagick"
VIMAGICK_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/vimagick"

PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"

def ncd(x,y):
    if x == y:
        return 0
    z_x = len(zlib.compress(bytes(x, "utf8")))
    z_y = len(zlib.compress(bytes(y, "utf8")))
    z_xy = len(zlib.compress(bytes(x + y, "utf8")))    
    return float(z_xy - min(z_x, z_y)) / max(z_x, z_y)

def dist_sub(X, m, Y, n):
 
    #ベースケース：空の文字列(ケース1)
    if m == 0:
        return n
 
    if n == 0:
        return m
 
    # 文字列の最後の文字が一致する場合は#(ケース2)
    # cost = 0 if (X[m - 1] == Y[n - 1]) else 1

    nc = ncd(X[m-1], Y[n-1])
    if nc <= 0.3:
        cost = 0
    else:
        cost = 1
 
    return min(
        dist(X, m - 1, Y, n) + 1,        #の削除(ケース3a))
        dist(X, m, Y, n - 1) + 1,           #挿入(ケース3b))
        dist(X, m - 1, Y, n - 1) + cost
    )

def dist_2(X, m, Y, n):
 
    #ベースケース：空の文字列(ケース1)
    if m == 0:
        return n
 
    if n == 0:
        return m
 
    # 文字列の最後の文字が一致する場合は#(ケース2)
    # cost = 0 if (X[m - 1] == Y[n - 1]) else 1

    nc = ncd(X[m-1], Y[n-1])
    if nc <= 0.3:
        cost = 0
    else:
        cost = 1
 
    return min(
        dist(X, m - 1, Y, n) + 1,        #の削除(ケース3a))
        dist(X, m, Y, n - 1) + 1         #挿入(ケース3b))
        # dist(X, m - 1, Y, n - 1) + cost
    )

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
            nc = ncd(X[m-1], Y[n-1])
            if nc <= 0.3:           #(ケース2)
                cost = 0                        #(ケース2)
            else:
                cost = 1                        #(ケース3c)
 
            T[i][j] = min(T[i - 1][j] + 1,      #の削除(ケース3b)
                        T[i][j - 1] + 1,        #挿入(ケース3a)
                        T[i - 1][j - 1] + cost) #交換(ケース2 + 3c)
 
    return T[m][n]

def main():
    file_paths = JsonFile._get_file_paths(VIMAGICK_AST_ROOT_PATH)
    dumped_ast_commands_per_run_instruction_dictionaly = dict()
    print(" loading *.json ========>>> ")
    for file_path in tqdm.tqdm(file_paths):
        contents = JsonFile._get_contents(file_path)
        for content in contents:
            run_instruction_id = ":".join(content["astCommandId"].split(":")[:-1])
            dumped = json.dumps(content["astCommand"])
            if not run_instruction_id in dumped_ast_commands_per_run_instruction_dictionaly:
                dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id] = list()
            dumped_ast_commands_per_run_instruction_dictionaly[run_instruction_id].append(dumped)

    with open("__testCase__.json", mode="r") as f:
        test_cases = json.load(f)
    
    S_1 = list()
    test_case = "webgoat:0"
    test_case = "zoneminder:0"
    print(test_case)
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        S_1.append(json.dumps(astCommand))

    pprint.pprint(S_1)

    lcs_dict = dict()
    for dumped_id, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        S_2 = list()
        for dumped_ast_command in dumped_ast_commands:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            S_2.append(json.dumps(astCommand))
        lcs_dict[dumped_id] = dist(S_1, S_2)/max(len(S_1), len(S_2))*1.00
    lcs_tuple = sorted(lcs_dict.items(), key=lambda x:x[1])

    for lcs_tp in lcs_tuple[:20]:
        print(lcs_tp)

if __name__ == "__main__":
    main()