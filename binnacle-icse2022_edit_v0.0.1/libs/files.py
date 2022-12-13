from abc import *
import glob
import json
import os

class File(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def _get_contents():
        pass

    @staticmethod
    @abstractmethod
    def _get_file_paths():
        pass
    
    @staticmethod
    @abstractmethod
    def _create_file():
        pass
    
    @staticmethod
    @abstractmethod
    def _get_basename():
        pass

class JsonFile(File):
    @staticmethod
    def _get_contents(file_path: str):
        with open(file_path, mode="r") as f:
            contents = json.load(f)
        return contents
        
    @staticmethod
    def _get_file_paths(root_path: str):
        return glob.glob("{root_path}/**/*.json".format(root_path=root_path), recursive=True)
    
    @staticmethod
    def _create_file(file_path, obj):
        with open(file_path, mode="w") as f:
            json.dump(obj, f, indent=4)

    @staticmethod
    def _get_basename(file_path):
        file_basename = os.path.basename(file_path); file_basename = file_basename.replace(".json", "")
        return file_basename


