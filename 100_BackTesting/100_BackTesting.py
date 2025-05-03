#!/usr/bin/env python
# coding: utf-8


"""
******************************************************************************
100_BackTesting.py 

Aplicacion que ejecuta Backtesting para una estrategia dada. Esta es la base 
para probar cualquier estrategia. En mejora continua

Scheduler: esta programada para poder ejecutarse con el schedular de windows.
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

pd.set_option('future.no_silent_downcasting', True)   #no se muy bien lo que hace pero quita errores



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




import logging    #https://docs.python.org/3/library/logging.html
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename='C:\\Users\\INNOVACION\\Documents\\J3\\100.- cursos\\Quant_udemy\\programas\\Projects\\100_BackTesting\\log\\registro_back_new.log', level=logging.INFO ,force=True,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

 

# Obtiene un logger específico para el módulo principal
logger = logging.getLogger(__name__)
logger.info('Inicio de la aplicación Backtesting')
#logging.warning('Esto es una pruba backtesting.py')



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
        #self.predi= self.I(PREDI,overlay=True)
        self.predi_des= self.I(PREDI_DES,overlay=True)
        self.hull= self.I(HULL,overlay=True)
        self.Cclose= self.I(CLOSE_Original,overlay=True)
        
        self.contador=0
        
        self.estrategia = 0
        

    def next(self):
        """
        Descripcion: recorre cada fila una a una, evalua el criterio y decide Buy/Sell en el siguente paso
        Va a recorreer row by row los Indicadores declarados en el metodo I en el init(()) de la clase.
        
        Para poder determinar unos parametros de backtesting, soy generoso con las entradas para calcular las estadisticas
        Luego en simulado contra el broker soy más exigente. Pero esto me permite hacer un filtro.
        
            
        """         
        super().next()
        self.contador +=1
        
        slatr = self.data.ATR[-1] #grid_distance
        TPSLRatio = 1.2*TPSL_Ratio
        
        ## Logia de la estrategia
        if self.signal1>0.3: #and len(self.trades)<=2:   #Sube mas de un 0,5%
            if (self.data.hull[-2] < self.data.hull[-1] ):    #hull subinedo
        
                """
                sl1 = self.data.Close[-1] - 2*slatr
                tp1 = self.data.Close[-1] + 2*slatr*TPSLRatio            
                self.buy(sl=sl1, tp=tp1, size=self.mysize)
                """
                self.buy()

        #Subió ayer con referencia antes de ayer
        if (self.data.Close[-1] > self.data.Close[-2]):
            return
        #Ayer subio no vendo, aunque no subiera con referencia a antes de ayer
        if ((self.data.Close[-1] > self.data.Open[-1] )):
            return            
        
        if ((self.signal1[-2] < self.signal1[-1] )): #si señal se mantiene NO vendo
            return            
        
        
        self.position.close()
                
        """    
        if (self.data.hull[-1] < self.data.hull[-2] ): 
            self.position.close()
        if(self.data.Close[-1] < 2*slatr):  #StopLoss    
            self.position.close()  
        """     
    
#fin clase MyStrat()

        
#*************************************************************************************************
#*************************************************************************************************
def fun_estrategia(estrat_):
    """
    DESCRIPTION.  Funcion propia mia nada que ver con el backtesting process. pero me sirve para aisla la estrategia
    ## Parametros Expectancy stat[25] >2  Return stat[6]>20   WinRate stat[18]>50
    
    Esta fucnion tambien configura la cuenta del Broker de Alpaca tenemos varias
        
    #(stat[25]>2) and (stat[6]>20) and(stat[18]>50) 
    
    
    Mejora: me parece que el orden de los elementos en stat esta variando. COmo es una seri mejor acceder por el 'indice'
    
      Start                                   148.0
      End                                     347.0
      Duration                                199.0
      Exposure Time [%]                        33.5
      Equity Final [$]                 107274.89125
      Equity Peak [$]                  107375.53355
      Commissions [$]                    4230.49075
      Return [%]                            7.27489
      Buy & Hold Return [%]                  -1.544
      Return (Ann.) [%]                         0.0
      Volatility (Ann.) [%]                     NaN
      Sharpe Ratio                              NaN
      Sortino Ratio                             NaN
      Calmar Ratio                              0.0
      Max. Drawdown [%]                    -6.99659
      Avg. Drawdown [%]                    -2.18352
      Max. Drawdown Duration                  152.0
      Avg. Drawdown Duration               27.83333
      # Trades                                 21.0
      Win Rate [%]                         52.38095
      Best Trade [%]                        3.34456
      Worst Trade [%]                      -1.62037
      Avg. Trade [%]                        0.41361
      Max. Trade Duration                      16.0
      Avg. Trade Duration                   2.85714
      Profit Factor                          2.2958
      Expectancy [%]                        0.42242
      SQN                                   1.40264
      Kelly Criterion                       0.29357
      _strategy                             MyStrat
      _equity_curve                        Equit...
      _trades                       Size  EntryB...  
        
        
    """
    
    expentancy_=stat[26]    #en %  ganancias por cada 100 €invertidos  ESPERANZA MATEMATICA
    return_=stat[7]         #en %  El rendimiento total de la estrategia durante el período de análisis
    winRate_=stat[19]       #en %  El porcentaje de operaciones ganadoras sobre el total de 
    profitFactor_=stat[25]
    
    if (estrat_ == 0):
                            #operaciones realizadas.
        if(expentancy_>(1.75)):   #and (return_>5)
            return(True)
        return False
        #return True  #para pruebas
    
    elif (estrat_ == 32):
        if((winRate_>40) and (expentancy_ >0.75) and (profitFactor_>1.5)):
            return(True)
        
        return (False)
    
    else:
        return(False)





#/******************************** FUNCION PRINCIPAL main() *********/
#     def main():   
if __name__ == '__main__':   

    telegram_send("__________________________v7 ene2025  ")


    dias_a_futuro = 0
    flag01= False
    
    estrategiaType =0
    
    if (sys.argv[2]== 'estrategia32'):    #32=M
        estrategiaType = 32
    elif(sys.argv[2]== 'estrategia00'):    #00=J
        estrategiaType = 00 
    
    
    
    if (sys.argv[1]== 'EU'):
        print('Mercado Europeo')
        telegram_send("EUROPA Estrategia 10: LSTM")
        tickers=  tickers_eurostoxx #+tickers_ibex 
    elif (sys.argv[1]== 'USA'): 
        print('Mercado Americano sep 2024')
        telegram_send("USA Estrategia: "+str(estrategiaType)+ "  (32=M) LSTM 11/24 #### #### #### #### ")
        tickers=  tickers_sp500 #+tickers_nasdaq #+ tickers_commodity
    elif (sys.argv[1]== 'RUSSELL'):     
        telegram_send("RUSSELL Estrategia 10: LSTM")
        tickers= tickers_russell_2000
        


        

    #Llamamos al constructor de la Clase compraVenta con el ID de la cuenta
    alpacaAPI= automatic.tradeAPIClass(para2=estrategiaType)  
        
    #Probamos valores concretos para depurar
        
    #tickers = ["ISRG","JNPR"]       #, "PCAR","AMD","ALGN","AMGN","AVGO","INTC","NXPI","SIRI"]
     
    
    for dias_a_futuro in [3]:  #range(0,2):   Pongo tres dias para estar en sintonia con la estrategia de subida en tres dias
    
        for jjj in range(0,len(tickers )): 
            instrumento_ =  tickers[jjj]
            #instrumento_ = 'PCAR'
            telegram_ping()
            
            ###♥ Chequeo por si no hay datos
            logger.warning('[81]Instrumento  '+instrumento_)
            try: 
                #################### PROBAMOS LA ESTRATEGIA
                # Determino las fechas, que NO se han visto en training
                fechaInicio_ = dt.datetime.today()  - dt.timedelta(days=450)
                fechaFin_ = dt.datetime.today()  #- dt.timedelta(days=1)    #dt.datetime(2023,2,21)
                
                dfpl = yf.download(instrumento_,  fechaInicio_,fechaFin_ )
                dfpl.columns = dfpl.columns.droplevel(1)
                #dfpl_reset = dfpl.reset_index(drop=True, inplace=True)   #Esta linea resetea los indices y ahora pone una numerico y me quita la fecha.
            except:
                logger.warning('[83]Ticker no existe  '+instrumento_)
                continue
            if dfpl.empty:
                continue
            if len(dfpl) <150:
                continue
            ##Ver si tiene pocos datos        
         
            
            try: 
                myLSTMnet_4D_Close = lstm.LSTMClass(dias_a_futuro,Y_supervised_ = 'Close')          #Creamos el objeto de la clase lstm
            except:
                logger.error('Error 88 Al crear el objeto LSTM para el instrumento '+instrumento_)
                continue
            
            # Ojo que estoy haciendo el BACKTESTING con datos con los que he entrenado... pero a la vez no quiero dejar datos
            #del pasado cercano fuera del modelo. 
            #Tendria que hacer backtesting con los datos de test y luego guardar los parametros
            
            try:                
                df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, 
                                                                                                    produccion_=True, fullDataSet=False)        
            except:
                logger.error('Error al cargar trabajar con el modelo LSTM  '+instrumento_)
                continue
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
                
            dfpl['signal']=1.0
            dfpl["signal"] = dfpl["signal"].astype("float64")  # Forzar el tipo si es necesario
            
            dfpl.iloc[-200:, dfpl.columns.get_loc("signal")] = df_signal.iloc[-200:, df_signal.columns.get_loc("signal")].copy()    #corregido!!!
            
            dfpl['predi']=1.0
            dfpl["predi"] = dfpl["predi"].astype("float64")  # Asegura que "predi" pueda contener NaN
            dfpl['prediDesplazado']=1.0
            dfpl["prediDesplazado"] = dfpl["prediDesplazado"].astype("float64") 
            
            df_predi = pd.DataFrame(predi, columns=['X_dias'])
            df_predi.fillna(0, inplace=True)
            
            df_prediDesplazado = pd.DataFrame(prediDesplazado, columns=['X_dias'])
            df_prediDesplazado.fillna(0, inplace=True)        
            
            #dfpl["predi"].loc[-200:]=df_predi['X_dias'].loc[-200:].copy()
            
            
            
            #dfpl.loc[dfpl.index[-200:], "predi"] = df_predi.loc[df_predi.index[-200:], "X_dias"].copy()
            dfpl.iloc[-200:, dfpl.columns.get_loc("predi")] = df_predi.iloc[-200:, df_predi.columns.get_loc("X_dias")].copy()


            
            #dfpl["prediDesplazado"].iloc[-200:]=df_prediDesplazado['X_dias'].iloc[-200-dias_a_futuro:-dias_a_futuro].copy()
            dfpl.iloc[-200:, dfpl.columns.get_loc("prediDesplazado")] = df_prediDesplazado.iloc[-200-dias_a_futuro:-dias_a_futuro, df_prediDesplazado.columns.get_loc("X_dias")].copy()

            
            dfpl['hull'] = 0.0  # Inicializa con ceros como float
            dfpl['hull'] = dfpl['hull'].astype("float64")
            #dfpl["hull"].loc[-200:]=dfpl_a['hull'].loc[-200:]
            dfpl.iloc[-200:, dfpl.columns.get_loc("hull")] = dfpl_a.iloc[-200:, dfpl_a.columns.get_loc("hull")].copy()
            
            #Me traigo unos datos del dataFrame originial de la clase LSTM

            dfpl['Cclose'] = 1
            dfpl.iloc[-200:, dfpl.columns.get_loc("Cclose")] = myLSTMnet_4D_Close.dfx.iloc[-200:, myLSTMnet_4D_Close.dfx.columns.get_loc("Close")].copy()

            
            
            
            
            #Backa a disco para agilizar el desarrollo
            ## Guardo en HD el fichero de señales, para evitar perder tiempo con las redes neuronales
            ## Ojo que este paso a csv quieta el date indes y luego no sale la fecha en el graph
            #############dfpl.to_csv("../temp/datos2.csv", index=True)
            #borro el dataframe
            #############del dfpl
                
            #############dfpl = pd.read_csv("../temp/datos2.csv",dtype={'predi': float})
            
            #dfpl = df_signal[:].copy()
            #CREO MIS INDICADORES
            """
            def SIGNAL():
                return dfpl.signal[-200:]
            def HULL():
                #dfpl['hull'].iloc[-200:-194]=dfpl['hull'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
                dfpl.loc[-200:-194, 'hull'] = dfpl.loc[-190:-184, 'hull']
                return dfpl.hull[-200:]
            
            def PREDI(): 
                #dfpl['predi'].iloc[-200:-194]=dfpl['predi'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
                #return dfpl.predi[-200:]
                dfpl.loc[-200:-194, 'predi'] = dfpl.loc[-190:-184, 'predi']  # Actualizar los valores
                return dfpl['predi'][-200:]  # Retornar los últimos 200 valores
            
            def PREDI_DES(): 
                #dfpl['prediDesplazado'].iloc[-200:-194]=dfpl['prediDesplazado'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
                #return dfpl.prediDesplazado[-200:]

                dfpl.loc[-200:-194, 'prediDesplazado'] = dfpl.loc[-190:-184, 'prediDesplazado']  # Actualizar los valores
                return dfpl['prediDesplazado'][-200:]  # Retornar los últimos 200 valores

                
            def CLOSE_Original(): 
                #dfpl['Cclose'].iloc[-200:-194]=dfpl['Cclose'].iloc[-190:-184]  #Mejorable muuucho estos primeros valores
                #return dfpl.Cclose[-200:]
            
                dfpl.loc[-200:-194, 'Cclose'] = dfpl.loc[-190:-184, 'Cclose']  # Actualizar los valores
                return dfpl['Cclose'][-200:]  # Retornar los últimos 200 valores
            """
                        
            # Creación de los indicadores
            def SIGNAL():
                return dfpl['signal'][-200:]
            
            def HULL():
                dfpl.loc[dfpl.index[-200:-194], 'hull'] = dfpl.loc[dfpl.index[-190:-184], 'hull']
                return dfpl['hull'][-200:]
            
            """
            def PREDI(): 
                dfpl.loc[dfpl.index[-200:-194], 'predi'] = dfpl.loc[dfpl.index[-190:-184], 'predi']
                return dfpl['predi'][-200:]
            """
            
            def PREDI_DES(): 
                dfpl.loc[dfpl.index[-200:-194], 'prediDesplazado'] = dfpl.loc[dfpl.index[-190:-184], 'prediDesplazado']
                return dfpl['prediDesplazado'][-200:]
            
            def CLOSE_Original(): 
                dfpl.loc[dfpl.index[-200:-194], 'Cclose'] = dfpl.loc[dfpl.index[-190:-184], 'Cclose']
                return dfpl['Cclose'][-200:]
            
            
            dfpl['ATR'] = ta.atr(high = dfpl.High, low = dfpl.Low, close = dfpl.Close, length = 16)
            dfpl.dropna(inplace=True)
            
            #Ejecutamos la strategia
            bt = Backtest(dfpl[-200:], MyStrat, cash=100000, commission=.001)   ## , exclusive_orders=True data ; strategy ; initial Cash; 
            stat = bt.run()
            print(stat)
            
            
            # esta fucnion Grafica los valores y el resutlado del backTesting... La quito por temas de memoria
            generar_graficos =True            
            if (generar_graficos):
                backtesting.set_bokeh_output(notebook=False)
                bt.plot(show_legend=True, plot_width=None, plot_equity=True, plot_return=False, 
                plot_pl=True, plot_volume=True, plot_drawdown=False, smooth_equity=False, relative_equity=True, 
                superimpose=False, resample=False, reverse_indicators=False, open_browser=False,
                filename=("C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/100_BackTesting/reports/temp/"
                          +instrumento_+"_"+str(dias_a_futuro)+"d_Close"+".html"))
            
            
            #Salvo informacion Estadistica en html y/o excel
            
            df_new= stat.to_frame()
            df_new.rename(columns={0:instrumento_}, inplace=True)
            
            
            file_path =("C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/100_BackTesting/reports/temp/"
                    +instrumento_+".xlsx")
            try:
                df_existing = pd.DataFrame()  #columns=[dias_a_futuro])
                df_existing= pd.read_excel(file_path, index_col=0)
                
                
                #with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                # agregar el nuevo DataFrame a una nueva hoja 
                df_new.to_excel(writer, sheet_name=str(dias_a_futuro), index=False)
                
                df4= pd.concat([df_existing, df_new], axis=1)
                df4.to_excel(file_path, 
                     index=True,
                     )
                
            except:             #La primera ronda no existe el fichero
                logger.error("K_7") 
                df_new.to_excel(file_path, 
                     index=True,
                     )  #sheet_name=str(dias_a_futuro)
                
            # MARCO ESTRATEGIA EN REAL ES BUENA..
            estrategia =False
            estrategia= fun_estrategia(estrategiaType )
            
            
            #estrategia =False   # CON ESTA INSTRUCCION PARO LAS COMPRAS!!!!
            
            if( estrategia ):   
                try:
                        
                    estrategia =True
                    #cargo el modelo entrenado con todos los datos a ver que me dice para hoy
                    df_signal_Close, predi, prediDesplazado = myLSTMnet_4D_Close.estrategia_LSTM_01( instrumento_, fechaInicio_, fechaFin_, 
                                                                                                    produccion_=True, fullDataSet=True)     
                except:
                    logger.error("K_9")  
                    continue
                
                    
               
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
                                  +" Exp="+ str(round(stat[27], 1))+" Ret="+ str(round(stat[7], 1))  +" Win="+ str(round(stat[20], 1))+
                                  "\n % rampUp  " + str(round(dfpl["signal"].iloc[-1],2)))
                        flag01=True
                    except:
                        print("error Telegram K_8")
                        logger.error("K_8") 
                        continue
                    
                    
                    #ver= myLSTMnet_4D_Close.__getattribute__('loss')
                    #telegram_send("\nLoss " + str(round(myLSTMnet_4D_Close.loss,3)))
                    #telegram_send("TP--> +(precioCompra_+beneficioEsperado_) +  SL--> +(precioCompra_ - (stoploss_))")
                    
                    
            ## Llamo a ALPACA para comprar
            ## Parametros Expectancy stat[25] >2  Return stat[6]>20   WinRate stat[18]>50
            
            if(ALPACA__ and estrategia):
                print ("Pasando por Alpaca")
                
                #dfpl["signal"].iloc[-1]=2
                if( (dfpl["signal"].iloc[-1] > 1) and (estrategia==True)):
                    try:
                        
                        
                        #### ESTRATEGIA ST//TP  Distinto de lo que hago en Bacttesting.
                        #Llamar al moneyManagement
                        TP_= ((dfpl["signal"].iloc[-1]*dfpl['Close'].iloc[-1])/100) 
                        
                        SL_=5*dfpl['ATR'].iloc[-1]           # Le doy un multiplo de 5 para dar 'espacio' al ATR
                            #SL_=dfpl['hull'].iloc[-1]      # Ojo que hull es valor de la accion no delta 
                        cantidad= alpacaAPI.moneyManag(instrumento_, TP_, SL_)

                        
                        #Poner una orden
                        latest_ask_price=00
                        
                        if (cantidad > 0):
                                
                            if (estrategiaType == 0):  # J3
                                cantidad = int (cantidad)   #convertir a valor entero de acciones a comprar
                                latest_ask_price, is_open= alpacaAPI.getLastQuote(instrumento_)
                                
                                orderID= alpacaAPI.placeOrder(instrumento_, cantidad)
                                #      latest_ask_price, is_open= alpacaAPI.getLastQuote(instrumento_)
                                #      orderID= alpacaAPI.placeBracketOrder( instrumento_ , cantidad, float (latest_ask_price+TP_), float ( SL_))  #latest_ask_price-#
                                
                                
                                
                                #Anoto en carteta                            
                                #nuevaPosicion ={'asset':instrumento_ , 'qty':cantidad,'buyPrice':dfpl['Close'].iloc[-1],'buyDay':dt.datetime.today(),
                                #                'SL':SL_, 'TP':TP_, 'sellDay':'0', 'sellPrice':0, 'reason':'0'}
                                #alpacaAPI.cartera202301 = alpacaAPI.cartera202301.append(nuevaPosicion, ignore_index=True)
                                #alpacaAPI.actualizarCartera('cartera01', nuevaPosicion)   
                                
                                
                            
                            elif (estrategiaType == 32):  #ALBA
                            
                                cantidad = int (cantidad)   #convertir a valor entero de acciones a comprar
                                #      orderID= alpacaAPI.placeOrder(instrumento_, cantidad)
                                latest_ask_price, is_open= alpacaAPI.getLastQuote(instrumento_)
                                orderID= alpacaAPI.placeBracketOrder( instrumento_ , cantidad, float (latest_ask_price+TP_), float ( latest_ask_price+ - SL_))  #latest_ask_price-#
                                
                                #Anoto en carteta                            
                                #nuevaPosicion ={'asset':instrumento_ , 'qty':cantidad,'buyPrice':dfpl['Close'].iloc[-1],'buyDay':dt.datetime.today(),
                                #                'SL':SL_, 'TP':TP_, 'sellDay':'0', 'sellPrice':0, 'reason':'0'}
                                #alpacaAPI.cartera202301 = alpacaAPI.cartera202301.append(nuevaPosicion, ignore_index=True)
                                #alpacaAPI.actualizarCartera('cartera01', nuevaPosicion)   
                                
                                
                            
                            else:
                                pass                      
                                                  

                        
                        telegram_send("TP = " +str(round(TP_,1))
                                  +" SL= "+ str(round(SL_,1)) +" Cantidad = "+ str(cantidad)
                                  + " Price: "+ str(latest_ask_price))
                    
                    except Exception as e:    
                        print("error ALpaca ....")
                        telegram_send("error Alpaca .... k69")
                        print(e)
                        logger.error(str(e) +" ALpaca K69")  
                        continue

            
            ##################  Excel con todos los valores
            
            print('borrar')
            if (( estrategia== True) or True ):   #solo grabo el excel si hay señal buena
                #flag01=False
                
                if (estrategiaType == 00):
                    file_path ="C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/100_BackTesting/reports/temp/0_becnchmark_00.xlsx"
                    
                elif (estrategiaType == 32):
                    file_path ="C:/Users/INNOVACION/Documents/J3/100.- cursos/Quant_udemy/programas/Projects/100_BackTesting/reports/temp/0_becnchmark_32.xlsx"
                    
                    
                try:
                    df_existing = pd.DataFrame() #columns=[instrumento_])
                    df_existing= pd.read_excel(file_path, index_col=0)
                    
                    ""
                    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
                            # agregar el nuevo DataFrame a una nueva hoja 
                            df_new.to_excel(writer, sheet_name=str(dias_a_futuro), index=False)
                    ""
                    df4= pd.concat([df_existing, df_new], axis=1)
                    df4.to_excel(file_path, 
                         index=True,
                         )
                    
                except:             #La primera ronda no existe el fichero
                    logger.error("k_4") 
                    df_new.to_excel(file_path, 
                         index=True
                         )  #sheet_name=str(dias_a_futuro)            
            
            
            
            
            print(stat._trades)
            del myLSTMnet_4D_Close    #Borro la clase para liberar memporia
            
    print('This is it................ 7')
    telegram_send("Estrategia = " + str(estrategiaType))
    telegram_send("This is it......")

    
    #Cierro LOGGING    
    logger.warning('Ejecutado con exito')
    logger.error('Estrategia  '+str(estrategiaType) + '  acabado correctamente'  )
    logging.shutdown()

    sys.exit(2)    #me salgo para no ejecutar el resto del codigo.
    
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