#!/usr/bin/env python
# coding: utf-8

#https://kernc.github.io/backtesting.py/

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


from backtesting.test import SMA, GOOG





TPSL_Ratio = 1

#myLSTMnet_6D.dfx


from backtesting import Strategy
from backtesting import Backtest
import backtesting
#!pip install bokeh==2.4.3



class MyStrat(Strategy):
    """Clase que manejando la estrategia recoge el dataFrame comprando y vendiendo
    https://kernc.github.io/backtesting.py/
    https://www.youtube.com/watch?v=e4ytbIm2Xg0&ab_channel=ChadThackray
    
    Notas: el dataFrame 'predi' de predicciones no se ajusta. Hoy me dice la predcicion
    a n_future days.
        
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
        self.predi= self.I(PREDI,overlay=True)
        self.predi= self.I(PREDI_DES,overlay=True)
        self.hull= self.I(HULL,overlay=True)
        self.Cclose= self.I(CLOSE_Original,overlay=True)
        
        self.contador=0
        
        

    def next(self):
        """
        Descripcion: recorre cada fila una a una, evalua el criterio y decide Buy/Sell en el siguente paso
        Va a recorreer row by row los Indicadores declarados en el metodo I en el init(()) de la clase.
            
        """         
        super().next()
        self.contador +=1
        
        slatr = self.data.ATR[-1] #grid_distance
        TPSLRatio = 1.2*TPSL_Ratio
        
        ## Logia de la estrategia
        if self.signal1==1: #and len(self.trades)<=2:   
            """
            sl1 = self.data.Close[-1] - 2*slatr
            tp1 = self.data.Close[-1] + 2*slatr*TPSLRatio            
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
            """
            self.buy()
            
        if (self.data.hull[-1] < self.data.hull[-2] ):  #El dataframe que no se incluye en llamada a run() nos eincrementan
            self.position.close()
        if(self.data.Close[-1] < 2*slatr):  #StopLoss    
            self.position.close()   





#/******************************** FUNCION PRINCIPAL main() *********/
#     def main():   
if __name__ == '__main__':   



    
    #################### PROBAMOS LA ESTRATEGIA
    # Determino las fechas
    fechaInicio_ = dt.datetime(2018,1,10)
    fechaFin_ = dt.datetime.today()  - dt.timedelta(days=1)    
    dias_a_futuro =6
    #
    
    
    for jjj in range(0,len(tickers_eurostoxx)): 
        
        instrumento_ =tickers_eurostoxx[jjj]
        myLSTMnet_6D = lstm.LSTMClass(dias_a_futuro)          #Creamos la clase
        df_signal, predi, prediDesplazado = myLSTMnet_6D.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_)
        ########################################################
        
        
        dfpl_a = myLSTMnet_6D.dfx[:].copy() #No me vale porque he quitado valores para que trabaje mejor la red
        
        dfpl = yf.download(instrumento_, fechaInicio_,fechaFin_)
        
        dfpl['signal']=1
        dfpl["signal"].iloc[-200:]=df_signal['signal'].iloc[-200:].copy()
        dfpl['predi']=1
        dfpl['prediDesplazado']=1
        
        df_predi = pd.DataFrame(predi, columns=['X_dias'])
        df_predi.fillna(0, inplace=True)
        
        df_prediDesplazado = pd.DataFrame(prediDesplazado, columns=['X_dias'])
        df_prediDesplazado.fillna(0, inplace=True)        
        
        dfpl["predi"].iloc[-200:]=df_predi['X_dias'].iloc[-200:].copy()
        dfpl["prediDesplazado"].iloc[-200:]=df_prediDesplazado['X_dias'].iloc[-200-dias_a_futuro:-dias_a_futuro].copy()
        
        dfpl['hull']=1
        dfpl["hull"].iloc[-200:]=dfpl_a['hull'].iloc[-200:]
        
        #Me traigo unos datos del dataFrame originial de la clase LSTM
        
        dfpl['Cclose']=1
        dfpl["Cclose"].iloc[-200:]=myLSTMnet_6D.dfx['Close'].iloc[-200:]
        
        
        
        
        #Backa a disco para agilizar el desarrollo
        ## Guardo en HD el fichero de señales, para evitar perder tiempo con las redes neuronales
        ## Ojo que este paso a csv quieta el date indes y luego no sale la fecha en el graph
        #############dfpl.to_csv("../temp/datos2.csv", index=True)
        #borro el dataframe
        #############del dfpl

        
        #############dfpl = pd.read_csv("../temp/datos2.csv",dtype={'predi': float})
        
        #dfpl = df_signal[:].copy()
        #CREO MIS INDICADORES
        def SIGNAL():
            return dfpl.signal[-200:]
        def HULL():
            dfpl['hull'].iloc[-200:-194]=dfpl['hull'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
            return dfpl.hull[-200:]
        def PREDI(): 
            dfpl['predi'].iloc[-200:-194]=dfpl['predi'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
            return dfpl.predi[-200:]
        def PREDI_DES(): 
            dfpl['prediDesplazado'].iloc[-200:-194]=dfpl['prediDesplazado'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
            return dfpl.prediDesplazado[-200:]
        def CLOSE_Original(): 
            dfpl['Cclose'].iloc[-200:-194]=dfpl['Cclose'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
            return dfpl.Cclose[-200:]
        
        dfpl['ATR'] = ta.atr(high = dfpl.High, low = dfpl.Low, close = dfpl.Close, length = 16)
        dfpl.dropna(inplace=True)
        
        #Ejecutamos la strategia
        bt = Backtest(dfpl[-200:], MyStrat, cash=100000, commission=.001)   ## , exclusive_orders=True data ; strategy ; initial Cash; 
        stat = bt.run()
        print(stat)
        
        backtesting.set_bokeh_output(notebook=False)
        bt.plot(show_legend=True, plot_width=None, plot_equity=True, plot_return=False, 
        plot_pl=True, plot_volume=True, plot_drawdown=False, smooth_equity=False, relative_equity=True, 
        superimpose=True, resample=False, reverse_indicators=False, open_browser=True,
        filename=("../reports/temp/graph_6d_"+instrumento_+".html"))
        
        
        #Salvo informacion Estadistica en html
        """ Comento para ir rapido en DEG
        df = stat.to_frame()
        html = df.to_html()
        with open("../reports/temp/stat_"+instrumento_+".html", "w") as file:
            file.write(html)
        import webbrowser
        webbrowser.open("../reports/temp/stat_"+instrumento_+".html")    
        """    
    
    print(stat._trades)
    print('This is it................ 7')
    
