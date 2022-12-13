import pickle
import pprint
import json
import numpy as np

from libs.files import *
from libs.d2v import *
from pqgrams_wrapper import *
from libs.contents import *
from libs.algorithms import *

from keras.layers import Embedding
from keras.models import Sequential
from tensorflow.keras.layers import LSTM
from keras.layers.core import Dense, Activation
from keras.utils import np_utils 
from tensorflow.keras.optimizers import Adam

GOLD_JSON_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/json/gold"
GOLD_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/gold"
GITHUB_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/github"
GOLD_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/gold"
GITHUB_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/github"

VIMAGICK_DATA_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2020_doc2vec_v0.0.1/data/vimagick"
VIMAGICK_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/vimagick"

PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"

def get_embedding_matrix(model, word_index):
    """
    keras.layers.Embeddingのweights引数で指定するための重み行列作成
    model: gensim model
    num_word: modelのvocabularyに登録されている単語数
    emb_dim: 分散表現の次元
    word_index: gensim modelのvocabularyに登録されている単語名をkeyとし、token idをvalueとする辞書 ex) {'word A in gensim model vocab': integer token id} 
    """
    # gensim modelの分散表現を格納するための変数を宣言
    embedding_matrix = np.zeros((max(list(word_index.values())) + 1, model.vector_size), dtype="float32")
   
    # 分散表現を順に行列に格納する
    for word, label in word_index.items():
        if word == "None":
            embedding_matrix[label] = np.zeros((1, 100), dtype="float32")
            continue
        astCommand = AstCleaner._sort_by_asc(json.loads(word))
        astCommandSequence = Root._get(astCommand)
        astCommandVector = model.infer_vector(astCommandSequence, epochs=30)
        # gensimのvocabularyに登録している文字列をembedding layerに入力するone-hot vectorのインデックスに変換して、該当する重み行列の要素に分散表現を代入
        embedding_matrix[label] = astCommandVector
    return embedding_matrix

def main():

    file_paths = JsonFile._get_file_paths(GOLD_AST_ROOT_PATH)
    dumped_ast_commands = list()
    dumped_ast_commands_per_run_instruction_dictionaly = dict()
    for file_path in file_paths:
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

    length_of_dumped_ast_commands = len(dumped_ast_commands)

    embedding_matrix = np.zeros((length_of_dumped_ast_commands, d2v_model.vector_size))

    word_index = {dumped_ast_command: created_id for created_id, dumped_ast_command in enumerate(dumped_ast_commands)}
    word_index["None"] = len(dumped_ast_commands)
    embedding_matrix = get_embedding_matrix(d2v_model, word_index)

    pprint.pprint(embedding_matrix.shape)

    num_words, d2v_size = embedding_matrix.shape

    windows = [cnt*(-1) for cnt in range(1, 5)]
    windows.reverse()

    x_training_columns = list()
    y_training_columns = list()
    for _, dumped_ast_commands in dumped_ast_commands_per_run_instruction_dictionaly.items():
        for dumped_ast_commandId, _ in enumerate(dumped_ast_commands):
            if dumped_ast_commandId < 1:
                continue
            x_training_column = list()
            for window in windows:
                try:
                    x_training_dumped_ast_command_vector = embedding_matrix[word_index[dumped_ast_commands[dumped_ast_commandId+window]]]
                except Exception as e:
                    x_training_dumped_ast_command_vector = np.array([0.0]*100)
                x_training_column.append(x_training_dumped_ast_command_vector)
            x_training_columns.append(x_training_column)
            y_training_columns.append(word_index[dumped_ast_commands[dumped_ast_commandId]])
    
    x_training_columns = np.array(x_training_columns)

    y_y_training_columns = np_utils.to_categorical(y_training_columns, max(y_training_columns)+1)
    layer = max(y_training_columns)+1



if __name__ == "__main__":
    main()


"""
GITHUBデータ
Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 embedding (Embedding)       (None, 1500682, 100)      150068200 
                                                                 
 lstm (LSTM)                 (None, 50)                30200     
                                                                 
 dense (Dense)               (None, 25)                1275      
                                                                 
 dense_1 (Dense)             (None, 2)                 52        
                                                                 
 activation (Activation)     (None, 2)                 0         
                                                                 
=================================================================
Total params: 150,099,727
Trainable params: 31,527
Non-trainable params: 150,068,200
_________________________________________________________________
"""