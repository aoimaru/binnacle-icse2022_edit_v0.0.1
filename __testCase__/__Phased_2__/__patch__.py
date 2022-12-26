import json
import pprint
import sys
import os

RUN_CLEANING_WORDS = [
    "DOCKER-RUN",
    "BASH-SCRIPT",
    "BASH-AND-IF",
    "BASH-AND-MEM",
    "UNKNOWN"
]

FILE_SHA="file_sha"
CHILDREN="children"

JESSFRAZ_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_2__/jessfraz"
VIMAGICK_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_2__/vimagick"
GOLD_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_edit_v0.0.1/__testCase__/__Phased_2__/gold"

def _get_contents_(file_path: str):
    """ファイルパスからコンテンツを取得する関数(jsonlを取得)"""
    with open(file_path, mode="r") as f:
        contents = list(f)
    return [json.loads(content) for content in contents]

def _get_commands_(file_sha: str, content: dict):
    file_sha = content[FILE_SHA]
    results = list()
    for cnt_id, cnt in enumerate(content["children"]):
        commands = list()
        def _filter_(me):
            """クロージャ"""
            if me["children"]:
                for child in me["children"]:
                    if not child["type"].startswith("BASH-COMMAND-"):
                        _filter_(child)
                    else:
                        commands.append(child)

        if cnt["type"]!="DOCKER-RUN":
            continue
        _filter_(cnt)

        column = list()
        columns = list()
        for command_id, command in enumerate(commands):
            tokens = list()
            def _token_(me):
                if me["children"]:
                    for child in me["children"]:
                        _token_(child)
                else:
                    if "value" in me:
                        tokens.append(me["value"])
            
            _token_(command)

            if command["type"]=="BASH-COMMAND-PREFIX":
                columns.append(column)
                column = list()
            column.extend(tokens)

            # print("tokens:", command["type"].ljust(20), tokens)
        for column_id, column in enumerate(columns):
            if not column:
                continue
            
            column_id = "{}:{}:{}".format(file_sha, cnt_id, column_id)
            results.append(
                {
                    "astCommandId": column_id,
                    "astCommand": column
                }
            )
    return results


        

def _to_file_(file_path, columns):
    with open(file_path, mode="w") as f:
        json.dump(columns, f, indent=4)


def main():
    file_path = "gold.jsonl"
    contents = _get_contents_(file_path)

    results = list()
    for content_id, content in enumerate(contents):
        file_sha = content[FILE_SHA]
        results = _get_commands_(file_sha, content)

        file_path = "{}/{}.json".format(GOLD_PATH, file_sha)
        _to_file_(file_path, results)


if __name__ == "__main__":
    main()