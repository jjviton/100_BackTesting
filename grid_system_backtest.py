#!/usr/bin/env python
# coding: utf-8

import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta

dataF = yf.download("EURUSD=X", start="2022-11-13", end="2023-01-11", interval='1h')
dataF.iloc[:,:]


grid_distance = 0.005
TPSL_Ratio = 1
midprice = 1.065
def generate_grid(midprice, grid_distance, grid_range):
    return (np.arange(midprice-grid_range, midprice+grid_range, grid_distance))

grid = generate_grid(midprice=midprice, grid_distance=grid_distance, grid_range=0.1)
grid


#Generamos una columna con el dato de la señal
signal = [0]*len(dataF)
i=0
for index, row in dataF.iterrows():
    for p in grid:
        if min(row.Low, row.High)<p and max(row.Low, row.High)>p:
            signal[i]=1
    i+=1
dataF["signal"]=signal
dataF[dataF["signal"]==1]


dfpl = dataF[:].copy()
def SIGNAL():
    return dfpl.signal
dfpl['ATR'] = ta.atr(high = dfpl.High, low = dfpl.Low, close = dfpl.Close, length = 16)
dfpl.dropna(inplace=True)


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
    
    
    mysize = 0.5
    def init(self):
        """
        Descripcion: Hereda del Init de la Clase. Se ejecuta una vez a la creacion de la clase
        Calculamos los datos necesarios par ejecutar la estrategia y que utilizaremos luego
        Estos datos pasaran de uno en uno en la fucnion next

        """        
        super().init()
        self.signal1 = self.I(SIGNAL) 
        self.rsi= self.I(talib.RSI, self.data.close, 14)  # llama a la fucnion RSI con los parametros
        self.sma1 =self.I(SMA,close, seld.n1)
        
        

    def next(self):
        """
        Descripcion: recorre cada fila una a una, evalua el criterio y decide Buy/Sell en el siguente paso
            
        """         
        super().next()
        
        slatr = self.data.ATR[-1] #grid_distance
        TPSLRatio = 1.2*TPSL_Ratio
        ## Logia de la estrategia
        if self.signal1==1 and len(self.trades)<=2:   
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
            
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)


#Ejecutamos la strategia
bt = Backtest(dfpl, MyStrat, cash=100, margin=1/1, commission=.000)   ## data ; strategy ; initial Cash; 
stat = bt.run()
stat



backtesting.set_bokeh_output(notebook=False)
bt.plot(show_legend=False, plot_width=None, plot_equity=True, plot_return=False, 
plot_pl=False, plot_volume=False, plot_drawdown=False, smooth_equity=False, relative_equity=True, 
superimpose=True, resample=False, reverse_indicators=False, open_browser=True)



stat._trades



