#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 07:15:35 2020

@author: navid
"""
import numpy as np

def initialize_borad():
    board = np.zeros((3,3))
    return board


def get_valid_moves(board):
    possible_moves = np.where(board== 0)
    possible_moves = list(zip(possible_moves[0],possible_moves[1]))
    return possible_moves
    
    
def get_move(Q , state , epsilon , board):
    possible_moves = get_valid_moves(board)
    if np.random.uniform() > epsilon:    
        move = possible_moves[0]
        for i in range(1,len(possible_moves)):
            if Q[state][move] < Q[state][possible_moves[i]]:
                move = possible_moves[i]
        return move
    else:
        move = possible_moves[np.random.choice(len(possible_moves))]
        return move
  
def remove_filled(board):
    a = np.zeros((3,3))
    filled = np.where(board != 0)
    filled = list(zip(filled[0],filled[1]))
    for i in range(len(filled)):
        a[filled[i]] = np.nan
    return a

def eval_game(board , player):  
    if 0 in board:
        for i in range(3):
            if board[i,0] == player and board[i,1] == player and board[i,2] == player:
                end_game = True
                winner = player
                break
            elif board[0,i] == player and board[1,i] == player and board[2,i] == player:
                end_game = True
                winner = player
                break
            elif board[0,0] == player and board[1,1] == player and board[2,2] == player:
                end_game = True
                winner = player
            elif board[2,0] == player and board[1,1] == player and board[0,2] == player:
                end_game = True
                winner = player
            else:
                end_game = False
                winner = 0               
    else:
        end_game = True
        for i in range(3):
            if board[i,0] == player and board[i,1] == player and board[i,2] == player:
                winner = player
                break
            elif board[0,i] == player and board[1,i] == player and board[2,i] == player:
                winner = player
                break
            elif board[0,0] == player and board[1,1] == player and board[2,2] == player:
                winner = player
            elif board[2,0] == player and board[1,1] == player and board[0,2] == player:
                winner = player
            else:
                winner = 0

    return winner , end_game    

def update_Q(Q , state , new_state , action , R , end_game , board):
    if end_game:
        max_estimate = 0
    else:
        possible = get_valid_moves(board)
        max_estimate = Q[new_state][possible[0]]
        for i in range(1,len(possible)):
            if max_estimate < Q[new_state][possible[i]]:
                max_estimate = Q[new_state][possible[i]]
    Q[state][action] += alpha*(R + (gamma*max_estimate) - Q[state][action])
# =============================================================================
#     dummy = np.copy(Q[state][0])
#     for rotation in range(1,4):
#         rotated_board = np.rot90(dummy, rotation)
#         rotated_state , Q = get_state(Q, rotated_board)
#         Q[rotated_state][1] = np.rot90(Q[state][1],rotation)
# =============================================================================
    return Q

def get_move_random(board):
    possible_moves = np.where(board == 0)
    possible_moves = list(zip(possible_moves[0],possible_moves[1]))
    move = possible_moves[np.random.choice(len(possible_moves))]
    return move


def print_board(board):
    for i in range(3):
        printable = []
        for j in range(3):
            if board[i,j] == 0:
                printable.append('-')
            elif board[i,j] == 1:
                printable.append('x')
            else:
                printable.append('o')
        print(f'{printable[0]} \t {printable[1]} \t {printable[2]}')



MAX_GAMES = 100000
Q1 = {}
Q2 = {}
epsilon = 1
alpha = 0.1
gamma = 1

game_number = 0
player1_wins = 0
player2_wins = 0
draw = 0

win_rate1 = []
win_rate2 = []
draw_rate = []
epsilon_list = []
player1_prev_state = 0
player2_state = 0
player2_move = 0
player1_wins = 0
player2_wins = 0
draw = 0
win_reward = 2
lose_reward = -1
draw_reward = 0
last_Q1_len = 1
last_Q2_len = 1
eps_zero_game = 0
counter = 0
while game_number < MAX_GAMES:
    if (game_number+1)%1000 == 0:
        if len(Q1.keys())/last_Q1_len == 1:
            epsilon = 0
            if counter == 0:
                eps_zero_game = game_number
            counter+=1
            
        
        #with open('log-two-AI.txt','a+') as log:
        #    log.write(f'{game_number/MAX_GAMES}\t{epsilon}\t{player1_wins/1000}\t{player2_wins/1000}\t{draw/1000}\t{len(Q1.keys())}\t{len(Q2.keys())}\n')
           
        print(f'{game_number/MAX_GAMES}% played - eps:{epsilon} - P1:{player1_wins/1000} - P2:{player2_wins/1000} - D:{draw/1000} - Q1:{len(Q1.keys())} - Q2:{len(Q2.keys())}')
        win_rate1.append(player1_wins)
        win_rate2.append(player2_wins)
        draw_rate.append(draw)
        
        player1_wins = 0
        player2_wins = 0
        draw = 0
        last_Q1_len = len(Q1.keys())
            
    board = initialize_borad()
    end_game = False
    
    player1_state = board.tobytes()
    if player1_state not in Q1:
        Q1.update({player1_state:remove_filled(board)})
    player1_move = get_move(Q1, player1_state, epsilon, board)
    board[player1_move] = 1
    player2_state = board.tobytes()
    if player2_state not in Q2:
        Q2.update({player2_state:remove_filled(board)})
    player2_move = get_move(Q2 , player2_state , epsilon, board)
    board[player2_move] = -1
    player1_new_state = board.tobytes()
    if player1_new_state not in Q1:
        Q1.update({player1_new_state:remove_filled(board)})
    Q1 = update_Q(Q1, player1_state, player1_new_state, player1_move, 0 , False, board)
    player1_state = player1_new_state
    while not end_game: 
        player1_move = get_move(Q1, player1_state, epsilon, board)
        board[player1_move] = 1
        
        winner , end_game = eval_game(board,1)
        if end_game:
            break
        else:
            player2_new_state = board.tobytes()
            if player2_new_state not in Q2:
                Q2.update({player2_new_state:remove_filled(board)})
            Q2 = update_Q(Q2, player2_state, player2_new_state, player2_move, 0 , False , board)
            player2_state = player2_new_state
        player2_move = get_move(Q2 , player2_state , epsilon, board)
        board[player2_move] = -1
        winner , end_game = eval_game(board,-1)
        if end_game:
            break
        else:
            player1_new_state = board.tobytes()
            if player1_new_state not in Q1:
                Q1.update({player1_new_state:remove_filled(board)})
            Q1 = update_Q(Q1, player1_state, player1_new_state, player1_move, 0 , False, board)
            player1_state = player1_new_state
            
            
    game_number += 1    
    if winner == 1:
        player1_wins += 1
        Q1 = update_Q(Q1, player1_state, player1_state, player1_move, win_reward , True,board)
        Q2 = update_Q(Q2, player2_state, player2_state, player2_move, lose_reward , True , board)
    elif winner == -1:
        player2_wins += 1
        Q1 = update_Q(Q1, player1_state, player1_state, player1_move, lose_reward , True, board)
        Q2 = update_Q(Q2, player2_state, player2_state, player2_move, win_reward , True, board)
    else:
        draw += 1
        Q1 = update_Q(Q1, player1_state, player1_state, player1_move, draw_reward , True, board)
        Q2 = update_Q(Q2, player2_state, player2_state, player2_move, draw_reward , True,board)
    epsilon_list.append(epsilon)


print(f'total games played: {game_number}')
print(f'player 1 wins: {player1_wins}')
print(f'player 2 wins: {player2_wins}')    
print(f'Draws: {draw}')


import matplotlib.pyplot as plt

plt.figure(figsize=(15,10))
plt.plot(np.array(win_rate1)/10,label ='P1-win')
plt.plot(np.array(win_rate2)/10,label='P2-win')
plt.plot(np.array(draw_rate)/10 , label='Draw')
plt.plot(np.ones(50)*eps_zero_game/1000,np.linspace(-2,102,50),'r--',label=r'$\epsilon = 0$')
plt.legend(fontsize=30)
plt.xlabel(r'Played games$\times 10^{3}$', fontsize=30)
plt.ylabel('%',fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.ylim(-2,102)
plt.xlim(0,100)
plt.savefig('rates.png')


q1 = np.zeros((len(Q1.keys()),2,3,3))
q2 = np.zeros((len(Q2.keys()),2,3,3))
i = 0
for key in Q1.keys():
    q1[i,0] = np.frombuffer(key).reshape(3,3)
    q1[i,1] = Q1[key]
    i+=1

i = 0
for key in Q2.keys():
    q2[i,0] = np.frombuffer(key).reshape(3,3)
    q2[i,1] = Q2[key]
    i+=1
    

import h5py
data = h5py.File('Data.h5' , 'w')

data.create_dataset('Q1', data = q1)
data.create_dataset('Q2', data = q2)
data.create_dataset('win_rate1', data = np.array(win_rate1))
data.create_dataset('win_rate2', data = np.array(win_rate2))
data.create_dataset('draw_rate', data = np.array(draw_rate))
data.create_dataset('epsilon', data = np.array(epsilon_list))

data.close()