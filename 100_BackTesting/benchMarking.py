# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:54:35 2023

@author: INNOVACION
"""

# -*- coding: utf-8 -*-


"""
******************************************************************************
Clase que implementa una LSTM para evaluar la serie temporal de una secuencia
 de precios y mostrar la prevision calculada.
 
Como objetivo tenemos entrenar una red LSTM para que descubra patrones esta-
cionales que nos permitan hacer trading de exito.
El proyecto 100_backtrading, permite evaluar la estrategia antes de pasar a PROD
Luego entrenamos la red con todos los datos disponibles hasta la fecha y 
salvamos el modelos para ponerle a operar diariamente y que nos dé señales.
Al comienzo creo que haremos las entradas y el moneymangement a mano.

Todo apunta que esta formula va a dar buenos resultados, espero no equivocarme 
o que lo que vemos a feb-23 no sea un espejismo o fruto de una buena racha.
 
******************************************************************************
******************************************************************************

Mejoras:    

Started on DIC/2022
Version_1: 

Objetivo: 

Author: J3Viton

"""

# J3_DEBUG__ = False  #variable global (global J3_DEBUG__ )


################################ IMPORTAMOS MODULOS A UTILIZAR.
import pandas as pd
import numpy as np
import datetime as dt
#import pandas_datareader as web
import datetime as dt
import yfinance as yf
import sys


####################### LOGGING
import logging    #https://docs.python.org/3/library/logging.html
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename='../log/registro.log', level=logging.INFO ,force=True,
                    format='%(asctime)s:%(levelname)s:%(message)s')
logging.warning('esto es una BenchMArk')

#### Variables globales  (refereniarlas con 'global' desde el codigo
versionVersion = 1.1
globalVar  = True


class BenchmarkClass:

    """CLASE ESTRATEGIA

       
    """  
    
    #Variable de CLASE
    backtesting = False  #variable de la clase, se accede con el nombre

    def __init__(self, previson_a_x_days=3, Y_supervised_ = 'hull', para1=False, para2=1):
        
        #Variable de INSTANCIA
        self.para_02 = para2   #variable de la isntancia

        return
    
    """
    Getter y setter para el acceso a atributo/propiedades
    """    
    def __getattribute__(self, attr):
        if attr == 'loss':
            return self._loss
        elif attr == 'xxx':
            return self._edad
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, valor):
        if attr == 'loss':
            self._loss = valor
        elif attr == 'xxx':
            self._edad = valor
        else:
            object.__setattr__(self, attr, valor)    
    
        
    def analisis(self, instrumento, startDate, endDate, DF):
        """
        Descripcion: sample method
        
        Parameters
        ----------
        beneficio : TYPE
            DESCRIPTION.

        Returns
        -------


        """
        pass
   
        return
   
    
#################################################### Clase FIN






#/******************************** FUNCION PRINCIPAL main() *********/
#     def main():   
if __name__ == '__main__':    
        
    """Esta parte del codigo se ejecuta cuando llamo tipo EXE
    Abajo tenemos el else: librería que es cuando se ejecuta como libreria.
        
    Parámetros:
    a -- 
    b -- 
    c -- 
    
    Devuelve:
    Valores 

    Excepciones:
    ValueError -- Si (a == 0)
    
    """   

    print(sys.argv[1])   #se configura en 'run' 'configuration per file'

    print ('version(J): ',versionVersion) 

    if (False and sys.argv[1]== 'train'):
        print('Train & Save')
 

        sys.exit()
    
    if (True or sys.argv[1]== 'prod' ):
        print('Produccion')

        instrumento_ = sys.argv[2]        
        #Recuepro el modelos entrenado       
        #instrumento_ = tickers_ibex[6]
        n_future = 4
        
                
        
  