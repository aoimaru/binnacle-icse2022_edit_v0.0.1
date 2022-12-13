from abc import *
import copy

class Algorithm(metaclass=ABCMeta):
    pass


class DFS(Algorithm):
    @staticmethod
    def _get(me):
        pass

class Simple(Algorithm):
    @staticmethod
    def _get(me):
        ast_paths = list()
        def _execute(me, visited):
            if me["children"]:
                for child in me["children"]:
                    ch_visited = copy.copy(visited)
                    ch_visited.append(child["type"])
                    _execute(child, ch_visited)
            else:
                ast_paths.append(visited)
        _execute(me, visited=[me["type"]])


class Root(Algorithm):
    @staticmethod
    def _get(me):
        """
        ASTを根から探索して葉まで到達したら, また根まで戻ってまた葉まで探索を行う
        """
        ast_paths = list()
        def _execute(me, visited):
            if me["children"]:
                for child in me["children"]:
                    ch_visited = copy.copy(visited)
                    ch_visited.append(child["type"])
                    _execute(child, ch_visited)
            else:
                ast_paths.append(visited)
        _execute(me, visited=[me["type"]])

        back_and_forth_ast_paths = list()
        for ast_path in ast_paths:
            reversed_ast_path = copy.copy(ast_path); reversed_ast_path.reverse()
            back_and_forth_ast_paths.append(ast_path+reversed_ast_path[1:])
        
        if not back_and_forth_ast_paths:
            return []
        
        created_ast_path = back_and_forth_ast_paths.pop(0)
        for back_and_forth_ast_path in back_and_forth_ast_paths:
            created_ast_path.extend(back_and_forth_ast_path[1:])

        return created_ast_path

