# coding: utf-8
# Your code here!
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



def getNumRangeMatchChar(S1: str, S2: str, distance=-1):
    L1 = len(S1); L2 = len(S2)
    ignored_distance = False
    
    if distance < 0 : ignored_distance = True
    
    counter = 0
    
    for i in range(L1):
        From = i
        Under = L2
        if not ignored_distance:
            From = 0 if i<distance else i-distance
            Under = int(L2) if i+distance>=L2 else i+distance
        
        for j in range(From, Under):
            # if S1[i]==S2[j]: counter+=1
            if ncd(S1[i], S2[j]) <= 0.1: counter+=1
    return counter

def getRangeMatchChar(S1, S2, distance=-1):
    L1 = len(S1); L2 = len(S2)
    ignored_distance = False
    
    if distance < 0 : ignored_distance = True
    
    ret = ""
    for i in range(L1):
        From = i
        Under = L2
        if not ignored_distance:
            From = 0 if i<distance else i-distance
            Under = L2 if i+distance>=L2 else i+distance
        
        for j in range(From, Under):
            # if S1[i]==S2[j]: ret+=S1[i]
            if ncd(S1[i], S2[j]) <= 0.1: ret+=S1[i]
    
    return ret
    
def getNumTransposition(S1, S2):
    c = 0
    L1 = len(S1); L2 = len(S2)
    for i in range(min(L1, L2)):
        # if S1[i] != S2[i]: c+=1
        if ncd(S1[i], S2[i]) > 0.1: c+=1
    
    return c



def getJaroDistance(S1, S2):
    L1 = len(S1); L2 = len(S2)
    distance = max(L1, L2)
    if distance<=0: return -1
    distance = int(distance/2)-1
    if distance<=0: return -1
    
    match = getNumRangeMatchChar(S1, S2, distance)
    trans = getNumTransposition(getRangeMatchChar(S1, S2, distance), getRangeMatchChar(S1, S2, distance))
    m = float(match)
    t = float(trans/2)
    
    try:
        return (m/L1+m/L2+(m-t)/match)/3
    except Exception as e:
        return 0
    
def getLengthOfCommonPrefix(S1, S2):
    L1 = len(S1); L2 = len(S2)
    c = 0
    for i in range(min(L1, L2)):
        # if (S1[i]==S2[i]):
        if ncd(S1[i], S2[i]) <= 0.1:
            c+=1
        else:
            break
    return c

def getJaroWinklerDistance(S1, S2, scaling=0.1):
    if scaling<0: return -1
    j = getJaroDistance(S1, S2)
    return j+getLengthOfCommonPrefix(S1, S2)*scaling*(1-j)

def main():
    file_paths = JsonFile._get_file_paths(JESSFRAZ_AST_ROOT_PATH)
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
    
    test_case = "dante:0"
    test_case = "taskd:0"
    # test_case = "phpvirtualbox:0"
    # test_case = "prestashop:2"
    # test_case = "kcptun:0"
    # test_case = "webgoat:0"
    # test_case = "webdis:2"
    test_case = "nextcloud:1"
    test_case = "afterthedeadline:1"
    test_case = "mysql-proxy:0"
    test_case = "dante:0"
    # test_case = "webgoat:0"
    # test_case = "glances:0"
    test_obj = {
        "type": "ROOT",
        "children": []
    }

    test_ncd = list()

    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        test_obj["children"].append(astCommand)
        test_ncd.append(json.dumps(astCommand))
    
    # pprint.pprint(test_obj)

    edit_distances = list()

    print("do...")
    for dumped_id, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        # if dumped_id==test_case:
        #     continue
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
                "jw_distance": getJaroWinklerDistance(test_ncd, sample_ncd),
                "simple_distance": simple_distance(PQ_GramWrapper._zhang(test_obj), PQ_GramWrapper._zhang(sample_obj))/max(len(test_obj["children"]), len(sample_obj["children"]))*1.00
            }
        )
        
    edit_distances = sorted(edit_distances, key=lambda x:x["jw_distance"])
    
    output_distances = dict()
    for edit_distance in edit_distances:
        if not edit_distance["jw_distance"] in output_distances:
            output_distances[edit_distance["jw_distance"]] = list()
        output_distances[edit_distance["jw_distance"]].append(edit_distance)
    
    output_distances = sorted(output_distances.items(), key=lambda x:x[0], reverse=True)
    count = 0
    for output_distance in output_distances:
        edit_distances = sorted(output_distance[1], key=lambda x:x["simple_distance"])
        for edit_distance in edit_distances:
            if count >= 10:
                break
            print(edit_distance["dumpedId"].ljust(20), edit_distance["jw_distance"], edit_distance["simple_distance"])
            count += 1
    
if __name__ == "__main__":
    main()