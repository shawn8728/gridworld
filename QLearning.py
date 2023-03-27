import numpy as np

def q_learning(size, alpha, gamma, epsilon, num_episodes, start, end, blocks):

    # Define the gridworld
    gridworld = np.zeros((size, size))

    # Add the blocks to the gridworld as 1
    for block in blocks:
        gridworld[block[0]][block[1]] = 1

    # Define the possible actions
    actions = ['up', 'down', 'left', 'right']

    # Define the Q-table
    q_table = np.zeros((size, size, len(actions)))

    # Run the Q-learning algorithm
    for i in range(num_episodes):
        state = start
        done = False
        while not done:
            # Choose an action using an epsilon-greedy exploration strategy
            if np.random.uniform() < epsilon:
                action = np.random.choice(actions)
            else:
                action = actions[np.argmax(q_table[state])]
            
            # Take the chosen action and observe the next state and reward
            if action == 'up':
                next_state = (state[0]-1, state[1])
                if next_state[0] < 0 or gridworld[next_state] == 1:
                    next_state = state
                reward = -1
            elif action == 'down':
                next_state = (state[0]+1, state[1])
                if next_state[0] > size-1 or gridworld[next_state] == 1:
                    next_state = state
                reward = -1
            elif action == 'left':
                next_state = (state[0], state[1]-1)
                if next_state[1] < 0 or gridworld[next_state] == 1:
                    next_state = state
                reward = -1
            elif action == 'right':
                next_state = (state[0], state[1]+1)
                if next_state[1] > size-1 or gridworld[next_state] == 1:
                    next_state = state
                reward = -1
            
            # Update the Q-value using the Q-learning update rule
            q_table[state][actions.index(action)] += alpha * (reward + gamma * np.max(q_table[next_state]) - q_table[state][actions.index(action)])
            
            # Move to the next state
            state = next_state
            
            # Check if the episode is done
            if state == end:
                done = True
        
        # Reduce the exploration rate over time
        epsilon = epsilon * (1 - 1/num_episodes)

    # Find the optimal path using the learned Q-table
    state = start
    path = [state]

    while state != end:
        action = actions[np.argmax(q_table[state])]
        
        if action == 'up':
            state = (state[0]-1, state[1])
        elif action == 'down':
            state = (state[0]+1, state[1])
        elif action == 'left':
            state = (state[0], state[1]-1)
        elif action == 'right':
            state = (state[0], state[1]+1)

        path.append(state)

    return path