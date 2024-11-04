"""
The Q-learning Agent class for tictactoe
Contains the functions to train Q-learning agents and choose moves

@author: navid
"""


import numpy as np

class Agent():
    def __init__(self, player, epsilon, alpha, discount):
        self.Q = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount

    #get the state (state is defined to be the byte value of the board)
    def get_state(self,board,removed_filled_board):
        state = board.tobytes()
        if state not in self.Q:
            self.Q.update({state:removed_filled_board})
        return state

    # get a move based on and epsilon-greedy policy
    def get_move(self, state , valid_moves):
        if np.random.uniform() > self.epsilon:    
            move = valid_moves[0]
            for i in range(1,len(valid_moves)):
                if self.Q[state][move] < self.Q[state][valid_moves[i]]:
                    move = valid_moves[i]
            return move

        else:
            move = valid_moves[np.random.choice(len(valid_moves))]
            return move
        
    #update the Q-values (train the agent)
    def learn(self, state , new_state , action , R , end_game):
        if end_game:
            max_estimate = 0
        else:
            max_estimate = np.nanmax(self.Q[new_state])
            
        self.Q[state][action] += self.alpha*(R + (self.discount*max_estimate) - self.Q[state][action])

    #save the resulting Q-table in HDF5 file
    def save(self,filename):
        q = np.zeros((len(self.Q.keys()),2,3,3))
        i = 0
        for key in self.Q.keys():
            q[i,0] = np.frombuffer(key).reshape(3,3)
            q[i,1] = self.Q[key]
            i+=1

        import h5py
        data = h5py.File(f'{filename}.h5' , 'w')

        data.create_dataset('Q', data = q)
       
        data.close()

        
