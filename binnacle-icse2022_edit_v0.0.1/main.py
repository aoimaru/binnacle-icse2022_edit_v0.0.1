import pickle
import pprint
import json
import numpy as np

from libs.files import *
from libs.d2v import *
from pqgrams_wrapper import *
from libs.contents import *
from libs.algorithms import *

# from keras.layers import Embedding
# from keras.models import Sequential
# from tensorflow.keras.layers import LSTM
# from keras.layers.core import Dense, Activation
# from keras.utils import np_utils 
# from tensorflow.keras.optimizers import Adam

import tensorflow as tf 
from tensorflow.keras import Sequential 
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.optimizers import SGD

import tqdm

GOLD_JSON_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/json/gold"
GOLD_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/gold"
GITHUB_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/github"
GOLD_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/gold"
GITHUB_MODEL_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/model/github"

VIMAGICK_DATA_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2020_doc2vec_v0.0.1/data/vimagick"
VIMAGICK_AST_ROOT_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/ast/vimagick"

PNG_PATH = "/Users/nakamurahekikai/Desktop/binnacle-icse2022_ast-path_v0.0.2/images"


def create_lstm_model():

    file_paths = JsonFile._get_file_paths(GITHUB_AST_ROOT_PATH)
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

    windows = [cnt*(-1) for cnt in range(1, 5)]
    windows.reverse()

    x_training_columns = list()
    y_training_columns = list()
    print(" cleating training vector ========>>> ")
    for _, dumped_ast_commands in tqdm.tqdm(dumped_ast_commands_per_run_instruction_dictionaly.items()):
        for dumped_ast_commandId, _ in enumerate(dumped_ast_commands):
            if dumped_ast_commandId < 1:
                continue
            x_training_column = list()
            for window in windows:
                try:
                    x_astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_commands[dumped_ast_commandId+window]))
                    x_astCommandSequence = Root._get(x_astCommand)
                    x_training_dumped_ast_command_vector = d2v_model.infer_vector(x_astCommandSequence, epochs=30)
                except Exception as e:
                    x_training_dumped_ast_command_vector = np.array([0.0]*100)
                x_training_column.append(x_training_dumped_ast_command_vector.T.tolist())
            x_training_columns.append(x_training_column)

            y_astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_commands[dumped_ast_commandId]))
            y_astCommandSequence = Root._get(y_astCommand)
            y_training_dumped_ast_command_vector = d2v_model.infer_vector(y_astCommandSequence, epochs=30)
            y_training_columns.append(y_training_dumped_ast_command_vector.T.tolist())
    

    x_stacked = list()
    y_stacked = list()
    print(" cleating embedding vector ========>>> ")
    for x_training_column, y_training_column in zip(tqdm.tqdm(x_training_columns), tqdm.tqdm(y_training_columns)):
        x_stacked.append(np.array(x_training_column))
        y_stacked.append(np.array([y_training_column]))

    x_train = np.stack(x_stacked, axis=0)
    y_train = np.stack(y_stacked, axis=0)
    print(x_train.shape)
    print(y_train.shape)


    # model = Sequential([
    #     SimpleRNN(100, activation=None, input_shape=(None, 100), return_sequences=True)
    # ])
    model = Sequential([
        SimpleRNN(100, input_shape=(None, 100), return_sequences=True)
    ])
    model.compile(optimizer=SGD(learning_rate=0.0001), loss="mean_squared_error")
    model.fit(x_train, y_train, batch_size=512, epochs=100)

    model.save("github-tanh.h5")



def test():
    from keras.models import load_model
    # from gensim.similarities.nmslib import NmslibIndexer
    
    lstm_model = load_model("github-tanh.h5")
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

    windows = [cnt*(-1) for cnt in range(1, 5)]
    windows.reverse()

    x_training_columns = list()
    y_training_columns = list()
    

    y_astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_commands_per_run_instruction_dictionaly["mediagoblin:2"][12]))
    y_astCommandSequence = Root._get(y_astCommand)
    y_training_dumped_ast_command_vector = d2v_model.infer_vector(y_astCommandSequence, epochs=30)
    y_training_columns.append(y_training_dumped_ast_command_vector.T.tolist())

    x_training_column = list()
    for dumped_ast_command in dumped_ast_commands_per_run_instruction_dictionaly["mediagoblin:2"][7:11]:
        x_astCommand = AstCleaner._sort_by_asc(json.loads(dumped_ast_command))
        x_astCommandSequence = Root._get(x_astCommand)
        x_training_dumped_ast_command_vector = d2v_model.infer_vector(x_astCommandSequence, epochs=30)
        x_training_column.append(x_training_dumped_ast_command_vector.T.tolist())
    x_training_columns.append(x_training_column)

    
    x_stacked = list()
    y_stacked = list()
    print(" cleating embedding vector ========>>> ")
    for x_training_column, y_training_column in zip(tqdm.tqdm(x_training_columns), tqdm.tqdm(y_training_columns)):
        x_stacked.append(np.array(x_training_column))
        y_stacked.append(np.array([y_training_column]))

    x_train = np.stack(x_stacked, axis=0)
    y_train = np.stack(y_stacked, axis=0)
    print(x_train.shape)
    print(y_train.shape)

    predicted = lstm_model.predict(x_train)
    
    cos = cos_sim(predicted[-1][-1], y_train[-1][-1])
    print(cos)


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def main():
    test()
    # create_lstm_model()

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