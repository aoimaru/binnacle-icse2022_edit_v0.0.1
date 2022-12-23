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

GOLD_JSON_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/json/gold"
GOLD_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/gold"
GITHUB_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/github"
GOLD_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/gold"
GITHUB_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/github"

VIMAGICK_DATA_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2020_doc2vec_v0.0.1/data/vimagick"
VIMAGICK_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/vimagick"

PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def lcs(s1, s2, n, m):
    if n == 0 or m == 0:
        return 0
    cos = cos_sim(s1[n-1], s2[m-1])
    if cos >= 0.8:
        return 1+lcs(s1, s2, n-1, m-1)
    else:
        return max(lcs(s1, s2, n, m-1), lcs(s1, s2, n-1, m))

# @lru_cache(maxsize=4096)
def ld(s, t):
    if not s: 
        return len(t)
    if not t: 
        return len(s)
    cos = cos_sim(s[0], t[0])
    if cos >= 0.95: 
        return ld(s[1:], t[1:])
    l1 = ld(s, t[1:])
    l2 = ld(s[1:], t)
    l3 = ld(s[1:], t[1:])
    return 1 + min(l1, l2, l3)

# @lru_cache(maxsize=4096)
def dist(X, m, Y, n):
 
    #ベースケース：空の文字列(ケース1)
    if m == 0:
        return n
 
    if n == 0:
        return m
 
    # 文字列の最後の文字が一致する場合は#(ケース2)
    # cost = 0 if (X[m - 1] == Y[n - 1]) else 1

    cos = cos_sim(X[m-1], Y[n-1])
    if cos >= 0.8:
        cost = 0
    else:
        cost = 1
 
    return min(
        dist(X, m - 1, Y, n) + 1,        #の削除(ケース3a))
        dist(X, m, Y, n - 1) + 1,           #挿入(ケース3b))
        dist(X, m - 1, Y, n - 1) + cost
    )
        
def main():
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
    
    model_path = "{}/root-pvdm.model".format(GITHUB_MODEL_ROOT_PATH)
    d2v_model = D2V_ROOT._load_model(model_path)


    S_1 = list()
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly["openconnect:0"]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        pprint.pprint(astCommand)
        astCommandSequence = Root._get(astCommand)
        astCommandVector = d2v_model.infer_vector(astCommandSequence, epochs=30)
        S_1.append(astCommandVector)
    
    S_1 = list()
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly["webgoat:0"]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        pprint.pprint(astCommand)
        astCommandSequence = Root._get(astCommand)
        astCommandVector = d2v_model.infer_vector(astCommandSequence, epochs=30)
        S_1.append(astCommandVector)
    
    lcs_dict = dict()
    count = 0
    for dumped_id, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        S_2 = list()
        for dumped_ast_command in dumped_ast_commands:
            astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
            astCommandSequence = Root._get(astCommand)
            astCommandVector = d2v_model.infer_vector(astCommandSequence, epochs=30)
            S_2.append(astCommandVector)
            
        # lcs_dict[dumped_id] = dist(S_1, len(S_1), S_2, len(S_2))
        lcs_dict[dumped_id] = dist(S_1, len(S_1), S_2, len(S_2))/max(len(S_1), len(S_2))*1.00
    
    lcs_tuple = sorted(lcs_dict.items(), key=lambda x:x[1])

    for lcs_tp in lcs_tuple[:10]:
        print(lcs_tp)
        



if __name__ == "__main__":
    main()