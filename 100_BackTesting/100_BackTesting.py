#!/usr/bin/env python
# coding: utf-8


"""
******************************************************************************
100_BackTesting.py 

Aplicacion que ejecuta Backtesting para una estrategia dada. Esta es la base 
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

####################### LOGGING
import logging    #https://docs.python.org/3/library/logging.html
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename='../log/registro.log', level=logging.WARNING ,force=True,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logging.warning('Esto es una pruba backtesting.py')


root_path ="C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\libreria"

sys.path.append("C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\libreria")
sys.path.append("C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM/")
sys.path.append("C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/999_Automatic/999_Automatic")


from eurostoxx import tickers_eurostoxx
from ibex import tickers_ibex
from sp500 import tickers_sp500
from nasdaq import tickers_nasdaq
from russell import tickers_russell_2000
from comodities import tickers_commodity


lstm = importlib.import_module("LSTM", "C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/10_LSTM/10_LSTM")
automatic = importlib.import_module("automatic", "C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/999_Automatic/999_Automatic")



def activarlog():
    import logging    #https://docs.python.org/3/library/logging.html
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename='../log/registro_back.log', level=logging.INFO ,force=True,
                        format='%(asctime)s:%(levelname)s:%(message)s')
    logging.warning('esto es una pruba backtesting.py')



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
        
        #activarlog()
        
#fin class        
        

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
            
        

def fun_estrategia():
    """
    DESCRIPTION.  Funcion propia mia nada que ver con el backtesting process. pero me sirve para aisla la estrategia
    ## Parametros Expectancy stat[25] >2  Return stat[6]>20   WinRate stat[18]>50
        
    #(stat[25]>2) and (stat[6]>20) and(stat[18]>50) 

    """
    expentancy_=stat[25]    #en %
    return_=stat[6]         #en %
    winRate_=stat[18]
    if(expentancy_>(0.5)and(winRate_>33)):   #and (return_>5)
        return(True)
    return False
    #return True  #para pruebas


#/******************************** FUNCION PRINCIPAL main() *********/
#     def main():   
if __name__ == '__main__':   

    telegram_send("__________________________v5 Sep2024 ")


    dias_a_futuro = 0
    flag01= False
    
    
    if (sys.argv[1]== 'EU'):
        print('Mercado Europeo')
        telegram_send("EUROPA Estrategia 10: LSTM")
        tickers=  tickers_eurostoxx #+tickers_ibex 
    elif (sys.argv[1]== 'USA'):
        print('Mercado Americano sep 2024')
        telegram_send("USA Estrategia 10: LSTM 09/24")
        tickers=  tickers_nasdaq #+ tickers_commodity
    elif (sys.argv[1]== 'RUSSELL'):     
        telegram_send("RUSSELL Estrategia 10: LSTM")
        tickers= tickers_russell_2000
     
        
     #Probamos valores concretos para depurar
        
    #tickers = ["WDAY"]       #, "PCAR","AMD","ALGN","AMGN","AVGO","INTC","NXPI","SIRI"]
     
    #test
    #Llamamos al constructor de la Clase
    alpacaAPI= automatic.tradeAPIClass()    

    
    for dias_a_futuro in [3]:  #range(0,2):   Pongo tres dias para estar en sintonia con la estrategia de subida en tres dias
    
        for jjj in range(0,len(tickers )): 
            instrumento_ =  tickers[jjj]
            #instrumento_ = 'WDAY'
            telegram_ping()
            
            ###♥ Chequeo por si no hay datos
            try: 
                #################### PROBAMOS LA ESTRATEGIA
                # Determino las fechas, que NO se han visto en training
                fechaInicio_ = dt.datetime.today()  - dt.timedelta(days=510)
                fechaFin_ = dt.datetime.today()  #- dt.timedelta(days=1)    #dt.datetime(2023,2,21)
                
                dfpl = yf.download(instrumento_,  fechaInicio_,fechaFin_ )
            except:
                #logging.info('Ticker no existe'+instrumento_)
                continue
            if dfpl.empty:
                continue
            if len(dfpl) <200:
                continue
            ##Ver si tiene pocos datos        
         
            ########################### UNA prediciones HULL and CLOSE
            #myLSTMnet_4D_hull = lstm.LSTMClass(dias_a_futuro,Y_supervised_ = 'hull')          #Creamos la clase
            #df_signal_hull, predi, prediDesplazado = myLSTMnet_4D_hull.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_)
            
            myLSTMnet_4D_Close = lstm.LSTMClass(dias_a_futuro,Y_supervised_ = 'Close')          #Creamos la clase
            
            # Ojo que estoy haciendo el BACKTESTING con datos con los que he entrenado... pero a la vez no quiero dejar datos
            #del pasado cercano fuera del modelo. 
            #Tendria que hacer backtesting con los datos de test y luego guardar los parametros
            
            if (sys.argv[1]== 'RUSSELL'):    #no tengo modelo    
                df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, produccion_=False)
            else:
                df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, produccion_=True, fullDataSet=False)        
            
            #df_signal=df_signal_hull['signal'] & df_signal_Close['signal']   #uno las señales
            #df_signal=df_signal.to_frame()
            #Finalmente solo aplicamos la estrategia close
            df_signal= df_signal_Close
            
            #ver= myLSTMnet_4D_Close.loss
            
            ########################################################
            
            
            dfpl_a = myLSTMnet_4D_Close.dfx[:].copy() #
            
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
                
            #MARCO ESTRATEGIA EN REAL ES BUENA..
            estrategia =False
            estrategia= fun_estrategia()
            if( estrategia ):       
                    #[6]=return [25]=expentace  [18]=winrate
                estrategia =True
                #cargo el modelo entrenado con todos los datos a ver que me dice para hoy
                df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, produccion_=True, fullDataSet=True)     
               
            #Convertimos a html
            """
            html = df.to_html()
            with open("../reports/temp/stat_"+instrumento_+".html", "w") as file:
                file.write(html)
            import webbrowser
            webbrowser.open("../reports/temp/stat_"+instrumento_+".html")    
            """         
            
            ## Comunico TELEGRAM si hay señal hoy
            if(TELEGRAM__ and estrategia):
                print ("Pasando por Telegram/backtessting")
                
                if( (dfpl["signal"].iloc[-1] > 1) and  (estrategia==True)):
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
            ## Parametros Expectancy stat[25] >2  Return stat[6]>20   WinRate stat[18]>50
            
            if(ALPACA__ and estrategia):
                print ("Pasando por Alpaca")
                
                if( (dfpl["signal"].iloc[-1] > 1) and (estrategia==True)):
                    try:
                        
                        
                        #### ESTRATEGIA ST//TP  Distinto de lo que hago en Bacttesting.
                        #Llamar al moneyManagement
                        TP_= ((dfpl["signal"].iloc[-1]*dfpl['Close'].iloc[-1])/100) 
                        SL_=5*dfpl['ATR'].iloc[-1]
                        #SL_=dfpl['hull'].iloc[-1]     #Ojo que hull es valor de la accion no delta 
                        cantidad= alpacaAPI.moneyManag(instrumento_, TP_, SL_)

                        
                        #Poner una orden
                        
                        if (cantidad > 0):
                            
                            cantidad = int (cantidad)   #convertir a valor entero de acciones a comprar
                            orderID= alpacaAPI.placeOrder(instrumento_, cantidad)
                            #      latest_ask_price, is_open= alpacaAPI.getLastQuote(instrumento_)
                            #      orderID= alpacaAPI.placeBracketOrder( instrumento_ , cantidad, float (latest_ask_price+TP_), float ( SL_))  #latest_ask_price-#
                            #Anoto en carteta                            
                            nuevaPosicion ={'asset':instrumento_ , 'qty':cantidad,'buyPrice':dfpl['Close'].iloc[-1],'buyDay':dt.datetime.today(),
                                            'SL':SL_, 'TP':TP_, 'sellDay':'0', 'sellPrice':0, 'reason':'0'}
                            #alpacaAPI.cartera202301 = alpacaAPI.cartera202301.append(nuevaPosicion, ignore_index=True)
                            alpacaAPI.actualizarCartera('cartera01', nuevaPosicion)                        

                        
                        telegram_send("TP = " +str(round(TP_,1))
                                  +" SL= "+ str(round(SL_,1)) +" Cantidad = "+ str(cantidad))
                    
                    except Exception as e:    
                        print("error ....")
                        telegram_send("error ....")
                        print(e)
                        logging.error(e)  
                        continue

            
            ##################  Excel con todos los valores
            print('borrar')
            if ( flag01== True):   #solo grabo el excel si hay señal buena
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
    
    #Cierro LOGGING    

    logging.shutdown()
    
    """ Backtesting parameter
    
    Start (Inicio): La fecha y hora de inicio del período de análisis de la estrategia.

    End (Fin): La fecha y hora de finalización del período de análisis de la estrategia.
    
    Duration (Duración): La duración total del período de análisis, expresada en días, horas y minutos.
    
    Exposure Time [%] (Tiempo de Exposición [%]): El porcentaje del tiempo total en el que la estrategia estuvo invertida en el mercado.
    
    Equity Final [$] (Capital Final [$]): El valor final del capital de la estrategia al final del período de análisis.
    
    Equity Peak [$] (Pico de Capital [$]): El valor máximo alcanzado por el capital de la estrategia durante el período de análisis.
    
    Return [%] (Rendimiento [%]): El rendimiento total de la estrategia durante el período de análisis, expresado como un porcentaje.
    
    Buy & Hold Return [%] (Rendimiento de Compra y Retención [%]): El rendimiento que habría generado un inversor que hubiera comprado y mantenido la inversión durante todo el período de análisis.
    
    Return (Ann.) [%] (Rendimiento Anualizado [%]): El rendimiento anualizado de la estrategia, expresado como un porcentaje.
    
    Volatility (Ann.) [%] (Volatilidad Anualizada [%]): La volatilidad anualizada de la estrategia, expresada como un porcentaje.
    
    Sharpe Ratio (Ratio de Sharpe): Una medida de la relación entre el rendimiento de la estrategia y su volatilidad, ajustada al riesgo.
    
    Sortino Ratio (Ratio de Sortino): Similar al Ratio de Sharpe, pero solo tiene en cuenta los rendimientos negativos, lo que lo hace más útil para evaluar estrategias con asimetría de riesgo.
    
    Calmar Ratio (Ratio de Calmar): Una medida de la relación entre el rendimiento de la estrategia y su máximo drawdown.
    
    Max. Drawdown [%] (Máximo Drawdown [%]): La mayor disminución desde un pico del capital hasta un mínimo durante el período de análisis, expresada como un porcentaje.
    
    Avg. Drawdown [%] (Drawdown Promedio [%]): La disminución promedio desde un pico del capital hasta un mínimo durante el período de análisis, expresada como un porcentaje.
    
    Max. Drawdown Duration (Duración del Máximo Drawdown): La duración máxima de un drawdown durante el período de análisis.
    
    Avg. Drawdown Duration (Duración Promedio del Drawdown): La duración promedio de los drawdowns durante el período de análisis.
    
    # Trades (Número de Operaciones): El número total de operaciones realizadas durante el período de análisis.
    
    Win Rate [%] (Tasa de Éxito [%]): El porcentaje de operaciones ganadoras sobre el total de operaciones realizadas.
    
    Best Trade [%] (Mejor Operación [%]): El mejor rendimiento obtenido en una sola operación, expresado como un porcentaje.
    
    Worst Trade [%] (Peor Operación [%]): El peor rendimiento obtenido en una sola operación, expresado como un porcentaje.
    
    Avg. Trade [%] (Operación Promedio [%]): El rendimiento promedio de todas las operaciones realizadas, expresado como un porcentaje.
    
    Max. Trade Duration (Duración Máxima de la Operación): La duración máxima de una sola operación.
    
    Avg. Trade Duration (Duración Promedio de la Operación): La duración promedio de todas las operaciones realizadas.
    
    Profit Factor (Factor de Ganancia): La relación entre las ganancias totales y las pérdidas totales de todas las operaciones realizadas.
    
    Expectancy [%] (Expectativa [%]): El rendimiento esperado promedio por operación, expresado como un porcentaje. Ganancias por cada 100 euros invertidos
    
    SQN (System Quality Number): Una medida de la calidad del sistema de trading, que tiene en cuenta el rendimiento, la volatilidad y el número de operaciones.
    
    _strategy (_estrategia): El nombre de la estrategia utilizada en el análisis.
    
    _equity_curve (_curva de capital): Detalles de la curva de capital de la estrategia.
    
    _trades (_operaciones): Detalles de las operaciones realizadas durante el período de análisis, incluyendo tamaño, entrada, salida, etc.
    """