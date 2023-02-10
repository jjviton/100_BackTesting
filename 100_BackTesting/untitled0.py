# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 19:52:36 2023

@author: INNOVACION
"""
size=np.array([1,2,3,4,5])
size = np.interp(size, (size.min(), size.max()), (8, 20)) 
print (size)
