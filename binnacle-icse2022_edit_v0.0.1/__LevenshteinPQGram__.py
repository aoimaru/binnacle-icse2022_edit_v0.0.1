
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
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pq = PQ_GramWrapper._get_pq_edit_distance(X[i-1], Y[j-1], 5, 2)
            if pq <= 0.5:
            # if X[i-1]==Y[j-1]:
                cost = 0
                where.append(str(j))
            else:
                cost = 1
 
            T[i][j] = min(
                T[i - 1][j] + 1,
                T[i][j - 1] + 1,
                T[i - 1][j - 1] + cost
            )
    return T[m][n], where

def __Demerau_Levenshtein__(X, Y):
    (m, n) = (len(X), len(Y))

    T = [[0 for x in range(n + 1)] for y in range(m + 1)]

    for i in range(1, m + 1):
        T[i][0] = i

    for j in range(1, n + 1):
        T[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            nc = ncd(X[i-1], Y[j-1])
            if nc <= 0.5:
                cost = 0
            else:
                cost = 1
 
            T[i][j] = min(
                T[i - 1][j] + 1,
                T[i][j - 1] + 1,
                T[i - 1][j - 1] + cost
            )

            if 1<i<m and 1<j<n and X[i-1]==Y[j-2] and X[i-2]==Y[j-1]:
                T[i][j]=min(
                    T[i][j], T[i-2][j-2]+1
                )

    return T[m][n]


def __Phased_3__(test_case: str):
    # file_paths = JsonFile._get_file_paths(PHASED3_JESSFRAZ_PATH)
    file_paths = JsonFile._get_file_paths(PHASED3_GOLD_PATH)

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
    
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case][:6]:
        astCommand = AstCleaner._sort_by_asc_for_phased3_(json.loads(dumped_ast_command))
        test_obj["children"].append(astCommand)
        test_ncd.append(astCommand)
        # test_ncd.append(AstCleaner._delete_reserved_structure_(json.dumps(astCommand)))

    # test_ncd.pop(-1)

    for tn in test_ncd:
        print(json.dumps(tn))
    

    # file_paths = JsonFile._get_file_paths(PHASED3_JESSFRAZ_PATH)
    file_paths = JsonFile._get_file_paths(PHASED3_GOLD_PATH)
    # file_paths = JsonFile._get_file_paths(PHASED3_VIMAGICK_PATH)

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
            astCommand = AstCleaner._sort_by_asc_for_phased3_(json.loads(dumped_ast_command))
            sample_obj["children"].append(astCommand)
            sample_ncd.append(astCommand)
            # sample_ncd.append(AstCleaner._delete_reserved_structure_(json.dumps(astCommand)))
        # pprint.pprint(sample_obj)
        try:
            ncd, where = __Levenshtein__(test_ncd, sample_ncd)
            ncd = ncd/max(len(test_ncd), len(sample_ncd))*1.00
            edit_distances.append(
                {
                    "dumpedId": dumped_id,
                    "astCommands": sample_obj,
                    "ncd_distance": ncd,
                    "where": where,
                    "simple_distance": simple_distance(PQ_GramWrapper._zhang(test_obj), PQ_GramWrapper._zhang(sample_obj))/max(len(test_obj["children"]), len(sample_obj["children"]))*1.00
                }
            )
        except Exception as e:
            # print("NG")
            pass
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
        # edit_distances = sorted(output_distance[1], key=lambda x:len(x["where"]), reverse=True)
        for edit_distance in edit_distances:
            if count >= 15:
                break
            # pprint.pprint(edit_distance["astCommands"])
            print(edit_distance["dumpedId"].ljust(20), edit_distance["ncd_distance"], edit_distance["simple_distance"])
            count += 1


def __Phased_4__(test_case: str):
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
    # for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        test_obj["children"].append(astCommand)
        test_ncd.append(astCommand)
        # test_ncd.append(AstCleaner._delete_reserved_structure_(json.dumps(astCommand)))

    test_ncd.pop(-1)

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
            sample_ncd.append(astCommand)
            # sample_ncd.append(AstCleaner._delete_reserved_structure_(json.dumps(astCommand)))
        # pprint.pprint(sample_obj)
        try:
            ncd, where = __Levenshtein__(test_ncd, sample_ncd)
            ncd = ncd/max(len(test_ncd), len(sample_ncd))*1.00
            edit_distances.append(
                {
                    "dumpedId": dumped_id,
                    "astCommands": sample_obj,
                    "ncd_distance": ncd,
                    "where": where,
                    "simple_distance": simple_distance(PQ_GramWrapper._zhang(test_obj), PQ_GramWrapper._zhang(sample_obj))/max(len(test_obj["children"]), len(sample_obj["children"]))*1.00
                }
            )
        except Exception as e:
            # print("NG")
            pass
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
        # edit_distances = sorted(output_distance[1], key=lambda x:len(x["where"]), reverse=True)
        for edit_distance in edit_distances:
            if count >= 15:
                break
            # pprint.pprint(edit_distance["astCommands"])
            print(edit_distance["dumpedId"].ljust(20), edit_distance["ncd_distance"], edit_distance["simple_distance"])
            count += 1

def main():
    test_case = "privoxy:1"
    # test_case = "openssh:1"
    test_case = "mariadb:1"
    test_case = "mysql-proxy:1"
    # test_case = "vsftpd:1"
    # test_case = "privoxy:1"
    # test_case = "mediagoblin:1"
    # test_case = "kafka-manager:6"
    test_case = "afterthedeadline:4"
    # test_case = "100644861884e21cc1e1aa878b21042b810f04f4:5"
    
    # __Phased_3__(test_case)
    # print()
    __Phased_4__(test_case)

if __name__ == "__main__":
    main()