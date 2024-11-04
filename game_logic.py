"""
The tic tac toe board class
Contains the functions to run the game dynamics and check the logic of the game

@author: navid
"""
import numpy as np

class TicTacToe():
    def __init__(self):
        self.board = np.zeros((3,3))
        self.player1_wins = 0
        self.player2_wins = 0
        self.draws = 0
        

    #reset the board    
    def reset(self):
        self.board = np.zeros((3,3))

    #update the board after each player makes a move
    def update_board(self,move,player):
        self.board[move] = player
    
    #check for valid moves given a board
    def get_valid_moves(self):
        valid_moves = np.where(self.board==0)
        valid_moves = list(zip(valid_moves[0],valid_moves[1]))
        return valid_moves

    #replace the filled cells on the board with NaN vlaue
    def remove_filled(self):
        a = np.zeros((3,3))
        filled = np.where(self.board != 0)
        filled = list(zip(filled[0],filled[1]))
        for i in range(len(filled)):
            a[filled[i]] = np.nan
        return a

    #evalute the game status (win/lose/draw) for the given player
    def eval_game(self, player):  
        if 0 in self.board:
            for i in range(3):
                if self.board[i,0] == player and self.board[i,1] == player and self.board[i,2] == player:
                    end_game = True
                    winner = player
                    break
                elif self.board[0,i] == player and self.board[1,i] == player and self.board[2,i] == player:
                    end_game = True
                    winner = player
                    break
                elif self.board[0,0] == player and self.board[1,1] == player and self.board[2,2] == player:
                    end_game = True
                    winner = player
                elif self.board[2,0] == player and self.board[1,1] == player and self.board[0,2] == player:
                    end_game = True
                    winner = player
                else:
                    end_game = False
                    winner = 0               
        else:
            end_game = True
            for i in range(3):
                if self.board[i,0] == player and self.board[i,1] == player and self.board[i,2] == player:
                    winner = player
                    break
                elif self.board[0,i] == player and self.board[1,i] == player and self.board[2,i] == player:
                    winner = player
                    break
                elif self.board[0,0] == player and self.board[1,1] == player and self.board[2,2] == player:
                    winner = player
                elif self.board[2,0] == player and self.board[1,1] == player and self.board[0,2] == player:
                    winner = player
                else:
                    winner = 0


        return winner , end_game    


    #print the board with x and o 
    def print_board(self):
        print("#####################")
        for i in range(3):
            printable = []
            for j in range(3):
                if self.board[i,j] == 0:
                    printable.append('-')
                elif self.board[i,j] == 1:
                    printable.append('x')
                else:
                    printable.append('o')
        
            print(f'{printable[0]} \t {printable[1]} \t {printable[2]}')
            
        print("#####################")

    #to track the game results
    def track_results(self,winner):
        if winner == 1:
            self.player1_wins += 1
        elif winner ==-1:
            self.player2_wins += 1
        else:
            self.draws += 1
            
        

