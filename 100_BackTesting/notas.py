# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:11:56 2023

@author: INNOVACION
"""


Coefficients: 
 [-0.14291959]
Independent term: 
 87.26113024543314
                         Close   Volume    EMA_100  ...       hull  dia     MA_Vol
Date       position                                 ...                           
2022-06-09 98.0      61.209999  1811000  55.495505  ...  66.768606    3  2677030.0
2022-06-10 99.0      59.790001  1540800  55.580545  ...  65.915623    4  2652880.0
2022-06-13 100.0     55.480000  2113200  55.578554  ...  64.198283    0  2650690.0
2022-06-14 101.0     54.439999  2330400  55.556008  ...  62.015590    1  2528465.0
2022-06-15 102.0     58.200001  3891700  55.608364  ...  60.132861    2  2552460.0

[5 rows x 8 columns]
(183, 8)
list['Volume', 'EMA_100', 'EMA_30', 'Kalman', 'hull', 'dia', 'MA_Vol', 'Close']
Traceback (most recent call last):

  File "C:\Users\INNOVACION\anaconda3\envs\AI\lib\site-packages\spyder_kernels\py3compat.py", line 356, in compat_exec
    exec(code, globals, locals)

  File "c:\users\innovacion\documents\j3\100.- cursos\quant_udemy\programas\projects\100_backtesting\100_backtesting\100_backtesting.py", line 142, in <module>
    df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_)

  File "C:\Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM\LSTM.py", line 169, in estrategia_LSTM_01
    self.dataPreparation_1(instrumento_,startDate_, endDate_)

  File "C:\Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM\LSTM.py", line 378, in dataPreparation_1
    self.trainX, trainX_test_kk, self.trainY, self.trainY_test  = train_test_split(self.trainXX, self.trainYY, test_size = 0.001,shuffle = False)

  File "C:\Users\INNOVACION\anaconda3\envs\AI\lib\site-packages\sklearn\model_selection\_split.py", line 2448, in train_test_split
    n_train, n_test = _validate_shuffle_split(

  File "C:\Users\INNOVACION\anaconda3\envs\AI\lib\site-packages\sklearn\model_selection\_split.py", line 2126, in _validate_shuffle_split
    raise ValueError(

ValueError: With n_samples=0, test_size=0.001 and train_size=None, the resulting train set will be empty. Adjust any of the aforementioned parameters.


runfile('C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/100_BackTesting/100_BackTesting/100_BackTesting.py', wdir='C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/100_BackTesting/100_BackTesting')
Reloaded modules: eurostoxx, ibex, sp500, quant_j3_lib, generarCSV, comodity, LSTM, telegram_bot, __autograph_generated_filem9p9ffj6, __autograph_generated_filef3mbpr1n, __autograph_generated_file09ouaasg, nasdaq
formato libreria
version:  1
 libreria
version(l):  1.1
{'id': 1473252352, 'first_name': 'vital_bot', 'is_bot': True, 'username': 'vital_quant_bot', 'can_join_groups': True, 'can_read_all_group_messages': False, 'supports_inline_queries': False}
ZTS
[*********************100%***********************]  1 of 1 completed