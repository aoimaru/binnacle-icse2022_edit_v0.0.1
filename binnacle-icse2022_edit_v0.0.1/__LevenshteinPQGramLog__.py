
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

PHASED3_JESSFRAZ_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_3__/jessfraz"
PHASED3_VIMAGICK_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_3__/vimagick"
PHASED3_GOLD_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_3__/gold"

PHASED4_JESSFRAZ_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_4__/jessfraz"
PHASED4_VIMAGICK_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_4__/vimagick"
PHASED4_GOLD_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_4__/gold"

PHASED4_GEM_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_4__/gemUpdateSystemRmRootGem"
PHASED4_NPM_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_4__/__npmCacheCleanAfterInstall__"




def ncd(x,y):
    if x == y:
        return 0
    z_x = len(zlib.compress(bytes(x, "utf8")))
    z_y = len(zlib.compress(bytes(y, "utf8")))
    z_xy = len(zlib.compress(bytes(x + y, "utf8")))    
    return float(z_xy - min(z_x, z_y)) / max(z_x, z_y)

def __Levenshtein__(X, Y):
    (m, n) = (len(X), len(Y))

    T = [[0 for x in range(n + 1)] for y in range(m + 1)]

    for i in range(1, m + 1):
        T[i][0] = i

    for j in range(1, n + 1):
        T[0][j] = j

    where = list()
    Logs = list()
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pq = PQ_GramWrapper._get_pq_edit_distance(X[i-1], Y[j-1], 5, 2)
            if pq <= 0.9:
                cost = 0
                where.append(str(j))
            else:
                cost = 1

            Insert = T[i - 1][j] + 1
            Delete = T[i][j - 1] + 1
            Replace = T[i - 1][j - 1] + cost

            Min = min(Insert, Delete, Replace)
            Log = list()
            for Key, Value in {"Insert": Insert, "Delete": Delete, "Replace": Replace}.items():
                if Value==Min:
                    Log.append(Key)
                if cost==0:
                    if "Replace" in Log:
                        Log = ["Replace"]
                column = " or ".join(Log)+" cost:{}".format(Min)
            Logs.append(column)

 
            T[i][j] = min(Insert, Delete, Replace)
    return T[m][n], where, T, Logs



def __Phased__(test_case: str):
    file_paths = JsonFile._get_file_paths(PHASED4_JESSFRAZ_PATH)
    # file_paths = JsonFile._get_file_paths(PHASED4_VIMAGICK_PATH)
    # file_paths = JsonFile._get_file_paths(PHASED4_GOLD_PATH)

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


    test_obj = {
        "type": "ROOT",
        "children": []
    }
    test_ncd = list()
    
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        test_obj["children"].append(astCommand)
        test_ncd.append(astCommand)

    # file_path = PHASED4_GEM_PATH+"/"+test_case+".json"
    # # file_path = PHASED4_NPM_PATH+"/"+test_case+".json"
    # contents = JsonFile._get_contents(file_path)
    # for content in contents:
    #     astCommand = AstCleaner._sort_by_asc(content["astCommand"])
    #     test_obj["children"].append(astCommand)
    #     test_ncd.append(astCommand)
    
    
    # test_ncd.pop(1)
    # test_ncd.pop(-1)

    for tn in test_ncd:
        print(json.dumps(tn))
    

    # file_paths = JsonFile._get_file_paths(PHASED4_JESSFRAZ_PATH)
    file_paths = JsonFile._get_file_paths(PHASED4_GOLD_PATH)
    # file_paths = JsonFile._get_file_paths(PHASED4_VIMAGICK_PATH)

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

    sample_obj = {
        "type": "ROOT",
        "children": []
    }
    sample_ncd = list()

    sample_case = "6e482708d3cafd1b0361e981702a95b023033688:1"
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[sample_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        sample_obj["children"].append(astCommand)
        sample_ncd.append(astCommand)
    
    ncd, where, T, Logs = __Levenshtein__(test_ncd, sample_ncd)
    ncd = ncd/max(len(test_ncd), len(sample_ncd))*1.00

    print(ncd)
    for tn in sample_ncd:
        print(json.dumps(tn))
    print()

    for t in T:
        print(t)
    
    for Log in Logs:
        print(Log)
    for wh in where:
        print(wh)

    sample_obj = {
        "type": "ROOT",
        "children": []
    }
    sample_ncd = list()

    sample_case = "616a77b53720814ade5121f2a348a446c355edf2:1"
    # sample_case = "f41b7df15ec0f174eace4b87954b705fed7c9b37:6"
    # sample_case = "6e482708d3cafd1b0361e981702a95b023033688:1"
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[sample_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        sample_obj["children"].append(astCommand)
        sample_ncd.append(astCommand)
    
    ncd, where, T, Logs = __Levenshtein__(test_ncd, sample_ncd)
    ncd = ncd/max(len(test_ncd), len(sample_ncd))*1.00

    print(ncd)
    for tn in sample_ncd:
        print(json.dumps(tn))
    print()

    for t in T:
        print(t)
    
    for Log in Logs:
        print(Log)
    
    for wh in where:
        print(wh)





def main():
    test_case = "privoxy:1"
    # test_case = "openssh:1"
    test_case = "mariadb:1"
    test_case = "mysql-proxy:1"
    # test_case = "vsftpd:1"
    # test_case = "privoxy:1"
    # test_case = "mediagoblin:1"
    # test_case = "kafka-manager:6"
    # test_case = "tabula:5"


    # test_case = "afterthedeadline:4"



    # test_case = "100644861884e21cc1e1aa878b21042b810f04f4:5"
    
    # __Phased_3__(test_case)
    # print()
    # test_case = "gemUpdateSystemRmRootGem:0"
    # test_case = "npmCacheCleanAfterInstall:0"
    # __Phased_4__(test_case)
    __Phased__(test_case)

if __name__ == "__main__":
    main()