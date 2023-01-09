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





def __Phased_4__(test_case: str):
    # file_paths = JsonFile._get_file_paths(PHASED3_JESSFRAZ_PATH)
    file_paths = JsonFile._get_file_paths(PHASED4_GOLD_PATH)

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
    # for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly[test_case]:
        astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        test_obj["children"].append(astCommand)
        test_ncd.append(astCommand)
        # test_ncd.append(AstCleaner._delete_reserved_structure_(json.dumps(astCommand)))

    # test_ncd.pop(-3)

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
        

        dacs = len(dumped_ast_commands)

        for dac_index in range(dacs):
            sample_ncd = list()
            for dumped_ast_command in dumped_ast_commands[dac_index:]:
                astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
                sample_ncd.append(astCommand)

            test_string = "".join(map(lambda x:json.dumps(x), test_ncd))
            sample_string = "".join(map(lambda x:json.dumps(x), sample_ncd))

            # print(test_string)
            # print(sample_string)
            if sample_string.startswith(test_string):
                edit_distances.append(
                    {
                        "id": "{}:{}".format(dumped_id, dac_index)
                    }
                )
    
    for edit_distance in edit_distances:
        print(edit_distance["id"])
            



            
        
    

def main():
    test_case = "privoxy:1"
    # test_case = "openssh:1"
    test_case = "mariadb:1"
    test_case = "mysql-proxy:1"
    # test_case = "vsftpd:1"
    # test_case = "privoxy:1"
    test_case = "mediagoblin:1"
    # test_case = "kafka-manager:6"
    test_case = "afterthedeadline:4"
    test_case = "100644861884e21cc1e1aa878b21042b810f04f4:5"
    
    # __Phased_3__(test_case)
    # print()
    __Phased_4__(test_case)

if __name__ == "__main__":
    main()