# import tensorflow as tf 
# import numpy as np 
# from tensorflow.keras import Sequential 
# from tensorflow.keras.layers import SimpleRNN
# from tensorflow.keras.optimizers import SGD

# import pprint

# tf.random.set_seed(111)
# np.random.seed(111)

# model = Sequential([
#     SimpleRNN(100, activation=None, input_shape=(None, 100), return_sequences=True)
# ])
# model.compile(optimizer=SGD(learning_rate=0.0001), loss="mean_squared_error")

# n = 51200
# x = np.random.random((n, 4, 100))
# pprint.pprint(x)
# print(x.shape)

# y = x.cumsum(axis=1)
# print(y.shape)
# y = np.random.random((n, 1, 100))
# print(y.shape)

# model.fit(x, y, batch_size=512, epochs=10)

# print(model.layers[0].weights)
# [<tf.Variable 'simple_rnn/kernel:0' shape=(1, 1) dtype=float32, numpy=array([[0.6021545]], dtype=float32)>,
#  <tf.Variable 'simple_rnn/recurrent_kernel:0' shape=(1, 1) dtype=float32, numpy=array([[1.0050855]], dtype=float32)>,
#  <tf.Variable 'simple_rnn/bias:0' shape=(1,) dtype=float32, numpy=array([0.20719269], dtype=float32)>]

# ans = model.predict(np.random.random((1, 4, 100)))
# print(ans.shape)
# pprint.pprint(ans)
# print(model.predict(np.ones((1, 30, 2)) * 0.5))
# array([ 0.5082699,  1.0191246,  1.5325773,  2.0486412,  2.5673294,
#         3.0886555,  3.6126328,  4.1392746,  4.6685944,  5.2006063,
#         5.7353234,  6.27276  ,  6.8129296,  7.3558464,  7.901524 ,
#         8.449977 ,  9.00122  ,  9.555265 , 10.112128 , 10.6718235,
#        11.2343645, 11.799767 , 12.368044 , 12.939212 , 13.513284 ,
#        14.090276 , 14.670201 , 15.253077 , 15.838916 , 16.427734 ],
#       dtype=float32)

# print(np.ones((1, 30, 1)) * 0.5)
# pprint.pprint(x)




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


ME = {'children': [{'children': [{'children': [], 'type': 'SC-CURL-F-LOCATION'},
                            {'children': [], 'type': 'SC-CURL-F-SHOW-ERROR'},
                            {'children': [], 'type': 'SC-CURL-F-SILENT'},
                            {'children': [{'children': [{'children': [],
                                                         'type': 'ABS-EXTENSION-TAR'},
                                                        {'children': [],
                                                         'type': 'ABS-PROBABLY-URL'},
                                                        {'children': [],
                                                         'type': 'ABS-URL-PROTOCOL-HTTPS'}],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-CURL-URL'}],
               'type': 'SC-CURL'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-TAR-ARG'}],
                             'type': 'SC-TAR-ARGS'},
                            {'children': [{'children': [],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-TAR-STRIP-COMPONENTS'}],
               'type': 'SC-TAR'}],
 'type': 'ROOT'}

ME_2 = {'children': [],
 'type': 'ROOT'}

ME_3 = {'children': [{'children': [{'children': [], 'type': 'SC-SET-F-E'},
                            {'children': [], 'type': 'SC-SET-F-X'}],
               'type': 'SC-SET'},
              {'children': [{'children': [], 'type': 'SC-APK-F-UPDATE-CACHE'},
                            {'children': [{'children': [],
                                           'type': 'SC-APK-PACKAGE'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:AUTOCONF'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:AUTOMAKE'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:BUILD-BASE'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:CURL'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:GNUTLS'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:GNUTLS-DEV'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:TAR'}],
                             'type': 'SC-APK-PACKAGES'}],
               'type': 'SC-APK-ADD'},
              {'children': [{'children': [], 'type': 'SC-ADD-USER-F-DEFAULTS'},
                            {'children': [], 'type': 'SC-ADD-USER-H'},
                            {'children': [{'children': [],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-ADD-USER-USER'}],
               'type': 'SC-ADD-USER'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-MKDIR-PATH'}],
                             'type': 'SC-MKDIR-PATHS'}],
               'type': 'SC-MKDIR'},
              {'children': [{'children': [{'children': [],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-CD-PATH'}],
               'type': 'SC-CD'},
              {'children': [{'children': [], 'type': 'SC-CURL-F-LOCATION'},
                            {'children': [], 'type': 'SC-CURL-F-SHOW-ERROR'},
                            {'children': [], 'type': 'SC-CURL-F-SILENT'},
                            {'children': [{'children': [],
                                           'type': 'BASH-VARIABLE:NM_URL'}],
                             'type': 'SC-CURL-URL'}],
               'type': 'SC-CURL'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-TAR-ARG'}],
                             'type': 'SC-TAR-ARGS'},
                            {'children': [{'children': [],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-TAR-STRIP'}],
               'type': 'SC-TAR'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-MV-PATH'},
                                          {'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-MV-PATH'}],
                             'type': 'SC-MV-PATHS'}],
               'type': 'SC-MV'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'},
                                                        {'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'BASH-CONCAT'}],
                             'type': 'SC-CHMOD-MODE'},
                            {'children': [{'children': [{'children': [{'children': [],
                                                                       'type': 'ABS-PROBABLY-URL'}],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-CHMOD-PATH'}],
                             'type': 'SC-CHMOD-PATHS'}],
               'type': 'SC-CHMOD'},
              {'children': [{'children': [], 'type': 'SC-CONFIGURE-ENABLE-TLS'},
                            {'children': [{'children': [{'children': [],
                                                         'type': 'ABS-MAYBE-PATH'},
                                                        {'children': [],
                                                         'type': 'ABS-PATH-ABSOLUTE'},
                                                        {'children': [],
                                                         'type': 'ABS-PATH-VAR'}],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-CONFIGURE-LOCALSTATEDIR'},
                            {'children': [{'children': [{'children': [{'children': [],
                                                                       'type': 'ABS-MAYBE-PATH'},
                                                                      {'children': [],
                                                                       'type': 'ABS-PATH-ABSOLUTE'}],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'BASH-PATH'}],
                             'type': 'SC-CONFIGURE-PREFIX'},
                            {'children': [{'children': [{'children': [],
                                                         'type': 'ABS-MAYBE-PATH'},
                                                        {'children': [],
                                                         'type': 'ABS-PATH-ABSOLUTE'}],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-CONFIGURE-SYSCONFDIR'}],
               'type': 'SC-CONFIGURE'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-MAKE-ARG'}],
                             'type': 'SC-MAKE-ARGS'},
                            {'children': [{'children': [],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-MAKE-TARGET'}],
               'type': 'SC-MAKE'},
              {'children': [{'children': [{'children': [{'children': [],
                                                         'type': 'ABS-MAYBE-PATH'}],
                                           'type': 'BASH-LITERAL'}],
                             'type': 'SC-CD-PATH'}],
               'type': 'SC-CD'},
              {'children': [{'children': [], 'type': 'SC-RM-F-FORCE'},
                            {'children': [], 'type': 'SC-RM-F-RECURSIVE'},
                            {'children': [{'children': [{'children': [],
                                                         'type': 'BASH-LITERAL'}],
                                           'type': 'SC-RM-PATH'}],
                             'type': 'SC-RM-PATHS'}],
               'type': 'SC-RM'},
              {'children': [{'children': [{'children': [],
                                           'type': 'SC-APK-PACKAGE:AUTOCONF'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:AUTOMAKE'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:BUILD-BASE'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:CURL'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:GNUTLS-DEV'},
                                          {'children': [],
                                           'type': 'SC-APK-PACKAGE:TAR'}],
                             'type': 'SC-APK-PACKAGES'}],
               'type': 'SC-APK-DEL'},
              {'children': [{'children': [], 'type': 'SC-RM-F-FORCE'},
                            {'children': [], 'type': 'SC-RM-F-RECURSIVE'},
                            {'children': [{'children': [{'children': [{'children': [{'children': [],
                                                                                     'type': 'ABS-GLOB-STAR'}],
                                                                       'type': 'BASH-GLOB'},
                                                                      {'children': [{'children': [],
                                                                                     'type': 'ABS-MAYBE-PATH'},
                                                                                    {'children': [],
                                                                                     'type': 'ABS-PATH-ABSOLUTE'},
                                                                                    {'children': [],
                                                                                     'type': 'ABS-PATH-VAR'}],
                                                                       'type': 'BASH-LITERAL'}],
                                                         'type': 'BASH-CONCAT'}],
                                           'type': 'SC-RM-PATH'}],
                             'type': 'SC-RM-PATHS'}],
               'type': 'SC-RM'}],
 'type': 'ROOT'}

def main():
    # ast = ASTSeed._random(ME)
    # pprint.pprint(ast)
    # print()
    ast = ASTSeed._random(ME_3)
    pprint.pprint(ast)




if __name__ == "__main__":
    main()