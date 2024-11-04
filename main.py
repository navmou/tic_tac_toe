import numpy as np
import h5py
from game_logic import TicTacToe
from Qlearning import Agent


# Hyper parameters
total_games = 50_000 #number of games to play
game_counter = 0 #counter to track the number of games
epsilon = 1 #the initial exploration rate
alpha = 0.2 #learning rate
discount = 1 #discount factor
win_reward = 1 #reward for winning the game
lose_reward = -1 #reward for losing the game
draw_reward = 0 #reward for draw
move_reward = -0.01 #reward for playing a move

player1_mark = 1
player2_mark = -1


#initializing the game and agents
game = TicTacToe()
player1 = Agent(player1_mark, epsilon, alpha, discount)
player2 = Agent(player2_mark, epsilon, alpha, discount)


while game_counter < total_games:
    #to set the exploration rate to 0 after a number of games
    if (game_counter+1)%10_000 == 0:
        player1.epsilon = 0
        player2.epsilon = 0


    end_game = False
    
    game.reset()

    player1_state = player1.get_state(game.board, game.remove_filled())
    player1_move = player1.get_move(player1_state, game.get_valid_moves())
    game.update_board(player1_move, player1_mark)

    player2_state = player2.get_state(game.board, game.remove_filled())
    player2_move = player2.get_move(player2_state, game.get_valid_moves())
    game.update_board(player2_move, player2_mark)

    player1_new_state = player1.get_state(game.board, game.remove_filled())
    player1.learn(player1_state, player1_new_state, player1_move, move_reward, end_game)    

    player1_state = player1_new_state
    
    while not end_game:
        player1_move = player1.get_move(player1_state, game.get_valid_moves())
        game.update_board(player1_move, player1_mark)

        winner, end_game = game.eval_game(player1_mark)
        if end_game:
            break
        else:
            player2_new_state = player2.get_state(game.board, game.remove_filled())
            player2.learn(player2_state, player2_new_state, player2_move, move_reward, end_game)
            player2_state = player2_new_state

        player2_move = player2.get_move(player2_state, game.get_valid_moves())
        game.update_board(player2_move, player2_mark)

        winner, end_game = game.eval_game(player2_mark)
        if end_game:
            break
        else:
            player1_new_state = player1.get_state(game.board, game.remove_filled())
            player1.learn(player1_state, player1_new_state, player1_move, move_reward, end_game)
            player1_state = player1_new_state

            
    game.track_results(winner)
    game_counter+=1 #adding to the number of games played

    #update Q-values after finishing each game
    if winner == player1_mark:
        player1.learn(player1_state, player1_state, player1_move, win_reward , end_game)
        player2.learn(player2_state, player2_state, player2_move, lose_reward , end_game)
    elif winner == player2_mark:
        player1.learn(player1_state, player1_state, player1_move, lose_reward , end_game)
        player2.learn(player2_state, player2_state, player2_move, win_reward , end_game )
    else:
        player1.learn(player1_state, player1_state, player1_move, draw_reward , end_game)
        player2.learn(player2_state, player2_state, player2_move, draw_reward , end_game)


    if (game_counter+1)%1000 == 0:
        print(f'{game_counter+1} games played')
        print(f"player1 wins in last 1000 games = {game.player1_wins/1000*100}%")
        print(f"player2 wins in last 1000 games = {game.player2_wins/1000*100}%")
        print(f"draws in last 1000 games = {game.draws/1000*100}%")
        print(f"epsilon1: {player1.epsilon} \t epsilon2: {player2.epsilon}")
        print(f"player1 number of states: {len(player1.Q.keys())}")
        print(f"player2 number of states: {len(player2.Q.keys())}")
        print("###################################################")
        game.player1_wins = 0
        game.player2_wins = 0
        game.draws = 0



#saving the resulting Q-tables.
player1.save("player1_Q")
player2.save("player2_Q")
    
        

    
            
        
        
