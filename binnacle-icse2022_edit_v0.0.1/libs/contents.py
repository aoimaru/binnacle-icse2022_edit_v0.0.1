from abc import *
import os
import numpy as np
import random

import pprint

RUN_CLEANING_WORDS = [
    "DOCKER-RUN",
    "BASH-SCRIPT",
    "BASH-AND-IF",
    "BASH-AND-MEM",
    "UNKNOWN"
]

class AstContent(metaclass=ABCMeta):
    pass

class DockerfileAst(AstContent):
    def __init__(self, content):
        self._content = content
    def _get_runs_by_ast(self) -> [dict()]:
        runs_by_ast = list()
        for cnt in self._content:
            if cnt["type"] != "DOCKER-RUN":
                continue
            runs_by_ast.append(cnt)
        return runs_by_ast


class DockerfileRunAst(AstContent):
    def __init__(self, content):
        self._content = content
    def _get_commands_by_ast(self) -> [dict()]:
        commands_by_ast = list()
        def _execute(me):
            if me["children"]:
                for child in me["children"]:
                    if child["type"] in RUN_CLEANING_WORDS:
                        _execute(child)
                    else:
                        commands_by_ast.append(child)
        _execute(self._content)
        return commands_by_ast
    
    def _get_commands_by_ast_with_bash_filter(self):
        commands_by_ast = list()
        def _execute(me):
            if me["children"]:
                for child in me["children"]:
                    if not child["type"].startswith("SC-"):
                        _execute(child)
                    else:
                        commands_by_ast.append(child)
        _execute(self._content)
        return commands_by_ast

class DockerfileCommandsAst(AstContent):
    def __init__(self, content):
        self._content = content
    


class AstCleaner(AstContent):
    @staticmethod
    def _sort_by_asc(content):
        def _execute(me):
            if me["children"]:
                children = list()
                for child in me["children"]:
                    children.append(_execute(child))
                children = sorted(children, key=lambda x:x["type"])
                return {
                    "type": me["type"],
                    "children": children
                }
            else:
                return me

        return _execute(content)
    
    @staticmethod
    def _delete_reserved_structure_(content):
        RESERVED = [
            '"children"',
            '"type"',
            '"value"'
        ]
        for reserved in RESERVED:
            content = content.replace(reserved, "")
        
        return content
    
    @staticmethod
    def _sort_by_asc_for_phased3_(content):
        def _execute(me):
            if me["children"]:
                children = list()
                for child in me["children"]:
                    children.append(_execute(child))
                children = sorted(children, key=lambda x:x["type"])
                return {
                    "type": me["type"],
                    "children": children
                }
            else:
                if "value" in me:
                    return {
                        "type": me["value"],
                        "children": []
                    }
                else:
                    return me

        return _execute(content)




class ASTSeed(AstContent):
    @staticmethod
    def _random(content, N=0.7, R=0.1, A=0.1, D=0.1, dummy=0.03):
        def _execute(me, depth):
            if me["children"]:
                children = list()
                for child in me["children"]:
                    children.append(_execute(child, depth+1))
                if len(children)>=2:
                    edit = np.random.choice(4, p=[N, R, A, D])
                    if edit==1:
                        selected = random.sample([child for child, _ in enumerate(children)], 2)
                        children[selected[0]], children[selected[1]] = children[selected[1]], children[selected[0]]
                    if edit==2:
                        selected = random.choice(children)
                        children.insert(random.choice([child for child, _ in enumerate(children)]), selected)
                    if edit==3:
                        selected = random.choice([child for child, _ in enumerate(children)])
                        children.pop(selected)
                if np.random.choice(2, p=[dummy*depth, 1.00-dummy*depth]):
                    return {
                        "type": me["type"],
                        "children": children
                    }
                else:
                    return {
                        "type": "DUMMY",
                        "children": children
                    }
            else:
                if np.random.choice(2, p=[dummy*depth, 1.00-dummy*depth]):
                    return me
                else:
                    return {
                        "type": "DUMMY",
                        "children": []
                    }

        return _execute(content, 0)