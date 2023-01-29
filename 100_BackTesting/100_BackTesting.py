#!/usr/bin/env python
# coding: utf-8

import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import datetime as dt

import importlib

import sys
sys.path.append("C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\libreria")
sys.path.append("C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM/")


from eurostoxx import tickers_eurostoxx
from ibex import tickers_ibex

lstm = importlib.import_module("LSTM", "C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM/")



#################### PROBAMOS LA ESTRATEGIA
# Determino las fechas
fechaInicio_ = dt.datetime(2018,1,10)
fechaFin_ = dt.datetime.today()  - dt.timedelta(days=1)    

myLSTMnet_6D = lstm.LSTMClass(6)          #Creamos la clase
df_signal= myLSTMnet_6D.estrategia_LSTM_01( tickers_ibex[6], fechaInicio_, fechaFin_)
########################################################


## Guardo en HD el fichero de señales, para evitar perder tiempo con las redes neuronales
df_signal['signal'].to_csv("../temp/datos.csv", index=False)
df_signal2 = pd.read_csv("../temp/datos.csv")


grid_distance = 0.005
TPSL_Ratio = 1
midprice = 1.065
def generate_grid(midprice, grid_distance, grid_range):
    return (np.arange(midprice-grid_range, midprice+grid_range, grid_distance))

grid = generate_grid(midprice=midprice, grid_distance=grid_distance, grid_range=0.1)
grid

#dfpl = myLSTMnet_6D.dfx[:].copy() No me vale porque he quitado valores para que trabaje mejor la red

dfpl = yf.download(tickers_ibex[1], fechaInicio_,fechaFin_)

dfpl['signal']=1
dfpl["signal"].iloc[-200:]=df_signal['signal'].iloc[:].copy()

#dfpl = df_signal[:].copy()
def SIGNAL():
    return dfpl.signal[-200:]
dfpl['ATR'] = ta.atr(high = dfpl.High, low = dfpl.Low, close = dfpl.Close, length = 16)
dfpl.dropna(inplace=True)

myLSTMnet_6D.dfx


from backtesting import Strategy
from backtesting import Backtest
import backtesting
#!pip install bokeh==2.4.3



class MyStrat(Strategy):
    """Clase que manejando la estrategia recoge el dataFrame comprando y vendiendo
    https://kernc.github.io/backtesting.py/
    https://www.youtube.com/watch?v=e4ytbIm2Xg0&ab_channel=ChadThackray
        
    Parámetros:
    a -- 
    
    """       
    
    
    mysize = 0.5  #creo que cuando compra, invierte la mitad de lo que tenemos
    def init(self):
        """
        Descripcion: Hereda del Init de la Clase. Se ejecuta una vez a la creacion de la clase
        Calculamos los datos necesarios par ejecutar la estrategia y que utilizaremos luego
        Estos datos pasaran de uno en uno en la fucnion next

        """        
        super().init()
        self.signal1 = self.I(SIGNAL) 
        #self.rsi= self.I(talib.RSI, self.data.close, 14)  # llama a la fucnion RSI con los parametros
        #self.sma1 =self.I(SMA,close, seld.n1)
        
        

    def next(self):
        """
        Descripcion: recorre cada fila una a una, evalua el criterio y decide Buy/Sell en el siguente paso
        Va a recorreer row by row los Indicadores declarados en el metodo I en el init(()) de la clase.
            
        """         
        super().next()
        
        slatr = self.data.ATR[-1] #grid_distance
        TPSLRatio = 1.2*TPSL_Ratio
        
        ## Logia de la estrategia
        if self.signal1==1: #and len(self.trades)<=2:   
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
            

            #sl1 = self.data.Close[-1] + slatr
            #tp1 = self.data.Close[-1] - slatr*TPSLRatio
            #self.sell(sl=sl1, tp=tp1, size=self.mysize)


#Ejecutamos la strategia
bt = Backtest(dfpl[-200:], MyStrat, cash=100, commission=.001)   ## data ; strategy ; initial Cash; 
stat = bt.run()
print(stat)


backtesting.set_bokeh_output(notebook=False)
bt.plot(show_legend=True, plot_width=None, plot_equity=True, plot_return=False, 
plot_pl=True, plot_volume=True, plot_drawdown=False, smooth_equity=False, relative_equity=True, 
superimpose=True, resample=False, reverse_indicators=False, open_browser=True)


#salvo informacion en html
df = stat.to_frame()
html = df.to_html()
with open("df.html", "w") as file:
    file.write(html)
import webbrowser

webbrowser.open("df.html")    



print(stat._trades)

print('This is it................ 7')

