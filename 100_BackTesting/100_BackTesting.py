#!/usr/bin/env python
# coding: utf-8


"""
******************************************************************************
Aplicaion que ejecuta Backtesting para una estrategia dada. Esta es la base 
para probar cualquier estrategia. En mejora continua

Scheduler: esta progrmada para poder ejecutarse con el schedular de windows.
Lanzamos una tarea al fichero cierre???.bat y paramos como parametro USA/EU
para segun la hora analizar un mercado u otro.
 
******************************************************************************
******************************************************************************

Mejoras:    

Started on MAR/2023
Version_1: 

Objetivo: 

Author: J3Viton

"""



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
sys.path.append("C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/999_Automatic/999_Automatic")


from eurostoxx import tickers_eurostoxx
from ibex import tickers_ibex
from sp500 import tickers_sp500
from nasdaq import tickers_nasdaq
from russell import tickers_russell_2000


lstm = importlib.import_module("LSTM", "C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM")
automatic = importlib.import_module("automatic", "C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/999_Automatic/999_Automatic")



from backtesting.test import SMA, GOOG

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )
TELEGRAM__ = True
ALPACA__ = True

sys.path.insert(0,"C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\libreria")
import quant_j3_lib as quant_j
from telegram_bot import *



TPSL_Ratio = 1

#myLSTMnet_4D_hull.dfx


from backtesting import Strategy
from backtesting import Backtest
import backtesting
#!pip install bokeh==2.4.3



class MyStrat(Strategy):
    """Clase que manejando la estrategia recoge el dataFrame comprando y vendiendo
    https://kernc.github.io/backtesting.py/
    https://www.youtube.com/watch?v=e4ytbIm2Xg0&ab_channel=ChadThackray
    Documentacion:
        https://www.learningmarkets.com/determining-expectancy-in-your-trading/#:~:text=What%20is%20expectancy%3F,and%20helps%20validate%20your%20backtesting.
        https://strategyquant.com/forum/topic/382-backtesting-guide/?ref=njt&utm_source=google&utm_medium=cpc&utm_campaign=nonus&gclid=CjwKCAiA0cyfBhBREiwAAtStHH1SlCp1KCf7jPKhgRa0b443EgFtt0KElG_Yn4FBss_l6R6oM78QaRoCsDkQAvD_BwE#:~:text=File%3A%20BackTestingReportBaseline.pdf
    
    
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
        if self.signal1>1: #and len(self.trades)<=2:   
            """
            sl1 = self.data.Close[-1] - 2*slatr
            tp1 = self.data.Close[-1] + 2*slatr*TPSLRatio            
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
            """
            self.buy()
            
        if (self.data.hull[-1] < self.data.hull[-2] ): 
            self.position.close()
        if(self.data.Close[-1] < 2*slatr):  #StopLoss    
            self.position.close()   





#/******************************** FUNCION PRINCIPAL main() *********/
#     def main():   
if __name__ == '__main__':   

    telegram_send("__________________________v3 ")

    #################### PROBAMOS LA ESTRATEGIA
    # Determino las fechas
    fechaInicio_ = dt.datetime(2005,1,10)
    fechaFin_ = dt.datetime.today()  #- dt.timedelta(days=1)    #dt.datetime(2023,2,21)
    dias_a_futuro = 4
    flag01= False
    
    
    if (sys.argv[1]== 'EU'):
        print('Mercado Europeo')
        telegram_send("EUROPA Estrategia 10: LSTM")
        tickers=  tickers_eurostoxx #+tickers_ibex 
    elif (sys.argv[1]== 'USA'):
        print('Mercado Americano')
        telegram_send("USA Estrategia 10: LSTM")
        tickers=  tickers_nasdaq
    elif (sys.argv[1]== 'RUSSELL'):     
        telegram_send("RUSSELL Estrategia 10: LSTM")
        tickers= tickers_russell_2000
        
        
    #test
    #Llamamos al constructor de la Clase
    alpacaAPI= automatic.tradeAPIClass()    

    
    for dias_a_futuro in [4]:  #range(0,2):   Pongo tres dias para estar en sintonia con la estrategia de subida en tres dias
    
        for jjj in range(0,len(tickers )): 
            instrumento_ =tickers[jjj]
            telegram_ping()
            
            ###♥ Chequeo por si no hay datos
            try: 
                dfpl = yf.download(instrumento_,  fechaInicio_,fechaFin_ )
            except:
                #logging.info('Ticker no existe'+instrumento_)
                continue
            if dfpl.empty:
                continue
            if len(dfpl) <300:
                continue
            ##Ver si tiene pocos datos        
            
            
            

            
            ########################### UNA prediciones HULL and CLOSE
            #myLSTMnet_4D_hull = lstm.LSTMClass(dias_a_futuro,Y_supervised_ = 'hull')          #Creamos la clase
            #df_signal_hull, predi, prediDesplazado = myLSTMnet_4D_hull.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_)
            
            myLSTMnet_4D_Close = lstm.LSTMClass(dias_a_futuro,Y_supervised_ = 'Close')          #Creamos la clase
            
            
            if (sys.argv[1]== 'RUSSELL'):    #no tengo modelo    
                df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, produccion_=False)
            else:
                df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, produccion_=True)        
            
            #df_signal=df_signal_hull['signal'] & df_signal_Close['signal']   #uno las señales
            #df_signal=df_signal.to_frame()
            #Finalmente solo aplicamos la estrategia close
            df_signal= df_signal_Close
            
            #ver= myLSTMnet_4D_Close.loss
            
            ########################################################
            
            
            dfpl_a = myLSTMnet_4D_Close.dfx[:].copy() #No me vale porque he quitado valores para que trabaje mejor la red
            
            #dfpl = yf.download(instrumento_, fechaInicio_,fechaFin_)

            """            
            try: 
                dfpl = yf.download(instrumento_,  fechaInicio_,fechaFin_ )
            except:
                #logging.info('Ticker no existe'+instrumento_)
                continue
            if dfpl.empty:
                continue
            """
                
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
            dfpl["Cclose"].iloc[-200:]=myLSTMnet_4D_Close.dfx['Close'].iloc[-200:]
            
            
            
            
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
            superimpose=True, resample=False, reverse_indicators=False, open_browser=False,
            filename=("../reports/temp/"+instrumento_+"_"+str(dias_a_futuro)+"d_Close"+".html"))
            
            
            #Salvo informacion Estadistica en html y/o excel
            
            df_new= stat.to_frame()
            df_new.rename(columns={0:instrumento_}, inplace=True)
            
            file_path ="../reports/temp/"+instrumento_+".xlsx"
            try:
                df_existing = pd.DataFrame()  #columns=[dias_a_futuro])
                df_existing= pd.read_excel(file_path, index_col=0)
                
                """
                with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                        # agregar el nuevo DataFrame a una nueva hoja 
                        df_new.to_excel(writer, sheet_name=str(dias_a_futuro), index=False)
                """
                df4= pd.concat([df_existing, df_new], axis=1)
                df4.to_excel(file_path, 
                     index=True,
                     )
                
            except:             #La primera ronda no existe el fichero
                df_new.to_excel(file_path, 
                     index=True,
                     )  #sheet_name=str(dias_a_futuro)
            
            #Convertimos a html
            """
            html = df.to_html()
            with open("../reports/temp/stat_"+instrumento_+".html", "w") as file:
                file.write(html)
            import webbrowser
            webbrowser.open("../reports/temp/stat_"+instrumento_+".html")    
            """    
            
            ## Comunico TELEGRAM si hay señal hoy
            if(TELEGRAM__):
                print ("Pasando por Telegram/backtessting")
                
                if( (dfpl["signal"].iloc[-1] > 1) and  
                   (stat[25]>2) and (stat[6]>20) and(stat[18]>50)                                     
                   ):
                    try:
                        telegram_send("Señal Estrategia 10 LSTM v2\n(IN)" +instrumento_
                                  +" Exp="+ str(round(stat[25], 1))+" Ret="+ str(round(stat[6], 1))  +" Win="+ str(round(stat[18], 1))+
                                  "\n % rampUp  " + str(round(dfpl["signal"].iloc[-1],2)))
                        flag01=True
                    except:
                        print("error Telegram 4")
                        continue
                    
                    
                    #ver= myLSTMnet_4D_Close.__getattribute__('loss')
                    #telegram_send("\nLoss " + str(round(myLSTMnet_4D_Close.loss,3)))
                    #telegram_send("TP--> +(precioCompra_+beneficioEsperado_) +  SL--> +(precioCompra_ - (stoploss_))")
                    
                    
            ## Llamo a ALPACA para comprar
            ## Parametros Expectancy >3
            if(ALPACA__):
                print ("Pasando por Alpaca")
                if( (dfpl["signal"].iloc[-1] > 1) and  
                   (stat[25]>2) and (stat[6]>20) and(stat[18]>50)
                   ):
                    try:
                        #Llamar al moneyManagement
                        TP_= ((dfpl["signal"].iloc[-1]*dfpl['Close'].iloc[-1])/100) 
                        SL_=1*dfpl['ATR'].iloc[-1]
                        cantidad= alpacaAPI.moneyManag(instrumento_, TP_, SL_)
                        #Poner una orden
                        if (cantidad > 0):
                            orderID= alpacaAPI.placeOrder(instrumento_, cantidad)
                        
                        telegram_send("TP = " +str(round(TP_,1))
                                  +" SL= "+ str(round(SL_,1)) +" Cantidad = "+ str(cantidad))
                    except:
                        print("error ALPACA")
                        continue
          
            
            ##################  Excel con todos los valores
            print('borrar')
            if (flag01== True):   #solo grabo el excel si hay señal buena
                flag01=False
                file_path ="../reports/temp/0_becnchmark.xlsx"
                try:
                    df_existing = pd.DataFrame() #columns=[instrumento_])
                    df_existing= pd.read_excel(file_path, index_col=0)
                    
                    """
                    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                            # agregar el nuevo DataFrame a una nueva hoja 
                            df_new.to_excel(writer, sheet_name=str(dias_a_futuro), index=False)
                    """
                    df4= pd.concat([df_existing, df_new], axis=1)
                    df4.to_excel(file_path, 
                         index=True,
                         )
                    
                except:             #La primera ronda no existe el fichero
                    df_new.to_excel(file_path, 
                         index=True
                         )  #sheet_name=str(dias_a_futuro)            
            
            
            
            
    print(stat._trades)
    print('This is it................ 7')
    telegram_send("This is it......")
    
