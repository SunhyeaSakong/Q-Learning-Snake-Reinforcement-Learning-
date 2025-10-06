import random
import time
from collections import deque
import pickle

# Define the directions for consistency and clarity.
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Define the numerical rewards based on your rules.
# These values are crucial for guiding the agent's learning process.
REWARD_VALUES = {
    'game_over': -100,
    'green_apple': +20,
    'red_apple': -15,
    'eating_nothing': -0.1,
}

class Agent:
    """
    A reinforcement learning agent that learns to play the snake game using
    the Q-learning algorithm.
    """
    def __init__(self):
        # n_games tracks the number of games played, used to control the exploration rate.
        self.n_games = 0
        
        # Epsilon is the exploration rate. It controls the randomness of the agent's actions.
        # It will decrease over time, moving from exploration to exploitation.
        self.epsilon = 0  
        
        # Gamma is the discount factor. It determines the importance of future rewards.
        # A higher value makes the agent more forward-thinking.
        self.gamma = 0.40 
        
        # The learning rate determines how much new information (the reward)
        # overrides old information in the Q-table.
        self.learning_rate = 0.1
        
        # The Q-table is a dictionary that maps a state-action pair to a Q-value.
        # The Q-value is the agent's estimate of the total future reward for taking that action
        # in that specific state. The key is (state_tuple, action_tuple).
        self.q_table = {}

    def get_state(self, vision_vectors):
        """
        Converts the game's vision vectors into a simplified, hashable state representation
        (a tuple of booleans). This is the 'observation' the agent uses for learning.
        """
        horizontal_vision = vision_vectors['Horizontal']
        vertical_vision = vision_vectors['Vertical']

        # Find the position of the head and the apples
        h_horiz_index = horizontal_vision.find('H')
        g_horiz_index = horizontal_vision.find('G')
        r_horiz_index = horizontal_vision.find('R')
        
        h_vert_index = vertical_vision.find('H')
        g_vert_index = vertical_vision.find('G')
        r_vert_index = vertical_vision.find('R')

        # The state is a tuple of booleans representing the presence of walls, body segments,
        # or apples in each direction relative to the snake's head.
        state = (
            # Danger in each direction? (Wall or snake body)
            vertical_vision[h_vert_index - 1] in ['W', 'S'],  # danger_up
            vertical_vision[h_vert_index + 1] in ['W', 'S'],  # danger_down
            horizontal_vision[h_horiz_index - 1] in ['W', 'S'], # danger_left
            horizontal_vision[h_horiz_index + 1] in ['W', 'S'], # danger_right

            # Green apple in each direction?
            g_vert_index != -1 and g_vert_index < h_vert_index, # green_apple_up
            g_vert_index != -1 and g_vert_index > h_vert_index, # green_apple_down
            g_horiz_index != -1 and g_horiz_index < h_horiz_index, # green_apple_left
            g_horiz_index != -1 and g_horiz_index > h_horiz_index, # green_apple_right

            # Red apple in each direction?
            r_vert_index != -1 and r_vert_index < h_vert_index, # red_apple_up
            r_vert_index != -1 and r_vert_index > h_vert_index, # red_apple_down
            r_horiz_index != -1 and r_horiz_index < h_horiz_index, # red_apple_left
            r_horiz_index != -1 and r_horiz_index > h_horiz_index, # red_apple_right
        )
        return state

    def get_reward(self, game_over, apple_eaten, apple_type=None, eaten_nothing=False):
        """
        Calculates the reward based on the game outcome for a single step.
        """
        if game_over:
            return REWARD_VALUES['game_over']
        elif apple_eaten:
            if apple_type == 'green':
                return REWARD_VALUES['green_apple']
            elif apple_type == 'red':
                return REWARD_VALUES['red_apple']
        else:  # Snake just move.
            return REWARD_VALUES['eating_nothing']
        

    def train_short_memory(self, state, action, reward, next_state):
        """
        Updates the Q-table using the Bellman equation. This is the core of the learning.
        Retreives the current q-value for next states by BELLMAN equation.
        """
        # Convert action list to a tuple for use as a dictionary key.
        action_tuple = tuple(action)

        # Initialize the Q-value for the state-action pair if it doesn't exist.
        if (state, action_tuple) not in self.q_table:
            self.q_table[(state, action_tuple)] = 0.0

        # Find the highest possible Q-value for the next state.
        next_state_values = []
        possible_actions = [UP, DOWN, LEFT, RIGHT]
        for a in possible_actions:
            next_state_values.append(self.q_table.get((next_state, a), 0.0))
        
        next_q_value = max(next_state_values) if next_state_values else 0.0

        # Apply the Q-learning update rule.
        current_q_value = self.q_table[(state, action_tuple)]
        updated_q_value = current_q_value + self.learning_rate * (reward + self.gamma * next_q_value - current_q_value)
        self.q_table[(state, action_tuple)] = updated_q_value

    def get_action(self, state, snake_body):
        """
        Decides the agent's next move using an epsilon-greedy strategy.
        It balances between exploring new actions and exploiting known good actions.

        Args: 
            state: The current state of the game.
            snake_body: A list of tuples representing the snake's coordinates.
        """

        # Determine and filter out the reverse direction
        # The snake body have at least 2 segments to determine direction.
        if len(snake_body) >= 2:
            head_pos = snake_body[0]
            second_segment_pos = snake_body[1]
            current_direction = (
                head_pos[0] - second_segment_pos[0],
                head_pos[1] - second_segment_pos[1]
            )
            reverse_direction = (
                -current_direction[0],
                -current_direction[1]
            )
            valid_actions = [action for action in [UP, DOWN, LEFT, RIGHT] if action != reverse_direction]
        else:
            # If the snake is just a head, all directions are valid.
            valid_actions = [UP, DOWN, LEFT, RIGHT]
        
        # Balance between exploration and exploitation.
        self.epsilon = 80 - self.n_games
        
        # Decide whether to explore or exploit 
        if random.randint(0, 200) < self.epsilon:
            # Exploration: choose a random action from the valid options.
            return random.choice(valid_actions)
        else:
            # Exploitation: choose the action from the valid options.
            q_values = {}
            for action in valid_actions:
                q_values[action] = self.q_table.get((state, action), 0.0)

            # Fallback to a random valid move if q-values exist for the state.
            if not q_values:
                # Fallback to a random move if the q_table is empty for this state.
                return random.choice(valid_actions)
            
            # Find the best action from the filtered list.
            best_action = max(q_values, key=q_values.get)
            return best_action
        
    def save_model(self, file_path):
        """
        Saves the agent's learning state to a file
        """
        with open(file_path, 'wb') as f:
            # We save the Q-table and the number of games played
            model_data = {
                'q_table': self.q_table,
                'n_games': self.n_games
            }
            pickle.dump(model_data, f)
        print(f"Model saved successfully to {file_path}")

    def load_model(self, file_path):
        """
        Load a previously saved model from a file.
        """
        try:
            with open(file_path, '+rb') as f:
                model_data = pickle.load(f)
                self.q_table = model_data['q_table']
                self.n_games = model_data['n_games']
            print(f"Model loaded successfully from {file_path}")
            # When loading, you might adjust the epsilon decay
            #For evaluation, set epsilon to zero.
            self.epsilon = 0  # Exemple for evaluation mode
        except FileNotFoundError:
            print(f"Error: Model file not found at {file_path}")
            return False
        return True
        
        