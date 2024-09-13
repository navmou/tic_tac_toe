#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 07:15:35 2020

@author: navid
"""
import numpy as np
import h5py
import matplotlib.pyplot as plt



def remove_filled(board):
    a = np.ones((3,3))
    filled = np.where(board != 0)
    filled = list(zip(filled[0],filled[1]))
    for i in range(len(filled)):
        a[filled[i]] = np.nan
    return a

def get_state(Q , board):
    for i in range(len(Q)):
        if np.array_equal(Q[i][0], board):
            return i

data = h5py.File('Data.h5','r')
#data = h5py.File('data.h5','r')

Q1 = np.array(data.get('Q1'))
Q2 = np.array(data.get('Q2'))



#Empty board
board = np.array([[0,0,0],[0,0,0],[0,0,0]])
state = get_state(Q1, board)
print('Empty board')
print(Q1[state])



#win state
board = np.array([[1,1,0],[-1,-1,0],[0,0,0]])
state = get_state(Q1, board)
print('Win')
print(Q1[state])

#Block state
board = np.array([[1,0,0],[0,-1,0],[1,0,0]])
state = get_state(Q2, board)
print('Block')
print(Q2[state])

#Fork
board = np.array([[1,0,0],[-1,1,0],[0,0,-1]])
state = get_state(Q1, board)
print('Fork')
print(Q1[state])

#Block fork
board = np.array([[-1,1,0],[1,0,0],[0,0,0]])
state = get_state(Q2, board)
print('Block Fork')
print(Q2[state])

board = np.array([[0,1,0],[1,0,0],[-1,0,0]])
state = get_state(Q2, board)
print('Block Fork filled intersection')
print(Q2[state])

#Play center
board = np.array([[1,0,0],[0,0,0],[0,0,0]])
state = get_state(Q2, board)
print('Play Center')
print(Q2[state])

#Opposite Corner
board = np.array([[1,0,0],[0,-1,0],[0,1,0]])
state = get_state(Q2, board)
print('Opposite Corner')
print(Q2[state])

#Empty Corner
board = np.array([[0,0,0],[0,1,0],[0,0,0]])
state = get_state(Q2, board)
print('Empty Corner')
print(Q2[state])


#Empty Corner
board = np.array([[1,-1,1],[0,-1,1],[0,1,-1]])
state = get_state(Q2, board)
print('Empty Corner')
print(Q2[state])
data.close()
    

#Empty Corner
board = np.array([[-1,0,1],[1,1,-1],[-1,0,0]])
state = get_state(Q1, board)
print('Empty Corner')
print(Q1[state])
data.close()


#Empty board
board = np.array([[0,0,0],[0,0,0],[0,0,0]])
state = get_state(Q1, board)
print('Empty Corner')
print(Q1[state])
data.close()


#Opponent on side
board = np.array([[0,1,0],[0,0,0],[0,0,0]])
state = get_state(Q2, board)
print('Empty Corner')
print(Q2[state])
data.close()


#Opponent on corner
board = np.array([[1,0,0],[0,-1,0],[0,0,1]])
state = get_state(Q2, board)
print('Empty Corner')
print(Q2[state])
data.close()


#Check student's
board = np.array([[0,-1,1],[0,0,1],[0,0,-1]])
state = get_state(Q1, board)
print('Empty Corner')
print(Q1[state])
data.close()



#Check student's
board = np.array([[1,0,0],[0,0,0],[0,0,0]])
state = get_state(Q2, board)
print('Empty Corner')
print(Q2[state])
data.close()




#Check student's
board = np.array([[0,-1,0],[1,1,0],[0,0,0]])
state = get_state(Q2, board)
print('Empty Corner')
print(Q2[state])
data.close()