import random
import time
from enum import Enum
# import the new Agent class from agent.py
from agent import Agent, REWARD_VALUES

# Define directions for clarity ---
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

class Cell(Enum):
    EMPTY = 0
    SNAKE = 1
    GREEN_APPLE = 2
    RED_APPLE = 3

class SnakeEnvironment:
    def __init__(self, size=10):
        self.size = size
        self.board = [[Cell.EMPTY for _ in range(size)] for _ in range(size)]
        self.snake = []
        self.green_apples = []
        self.red_apple = None
        self._place_snake()
        self._place_initial_apples()
        self.score = 0 
        self.moves_since_apple = 0

    def _get_random_empty_cell(self):
        """
        Returns a random empty cell coordinates (r, c).
        """
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == Cell.EMPTY]
        if not empty_cells:
            return None
        return random.choice(empty_cells)

    def _place_snake(self):
        placed = False
        while not placed:
            direction = random.choice([UP, DOWN, LEFT, RIGHT])
            start_row = random.randint(0, self.size - 1)
            start_col = random.randint(0, self.size - 1)
            
            coords = []
            for i in range(3):
                r = start_row + i * direction[0]
                c = start_col + i * direction[1]
                if 0 <= r < self.size and 0 <= c < self.size:
                    coords.append((r, c))
                else:
                    break
            
            if len(coords) == 3 and all(self.board[r][c] == Cell.EMPTY for r, c in coords):
                for r, c in coords:
                    self.board[r][c] = Cell.SNAKE
                self.snake = coords
                placed = True

    def _place_initial_apples(self):
        """
        Places the initial set of apples (2 green and 1 red).
        """
        for _ in range(2):
            cell = self._get_random_empty_cell()
            if cell:
                r, c = cell
                self.board[r][c] = Cell.GREEN_APPLE
                self.green_apples.append(cell)

        cell = self._get_random_empty_cell()
        if cell:
            r, c = cell
            self.board[r][c] = Cell.RED_APPLE
            self.red_apple = cell
    
    def _place_new_green_apple(self):
        """
        Places a single new green apple.
        """ 
        cell = self._get_random_empty_cell()
        if cell:
            r, c = cell
            self.board[r][c] = Cell.GREEN_APPLE
            self.green_apples.append(cell)

    def _place_new_red_apple(self):
        """
        Places a single new red apple.
        """
        cell = self._get_random_empty_cell()
        if cell:
            r, c = cell
            self.board[r][c] = Cell.RED_APPLE
            self.red_apple = cell
        
    def move(self, direction):
        """
        Moves the snake one step in the given direction and handles all game
        logic, including collisions, eating apples, and updating the board 
        state.
        Args:
            direction (tuple): A tuple representing the direction of movement
            Ex)(0, 1) for right.
        Returns:
            tuple: A tuple containing(game_over, apple_eaten, apple_type).   
        """
       # Check for Game Over conditions
        game_over = False
        apple_eaten = False
        apple_type = None

        # Get the current head of the snake
        head_r, head_c = self.snake[0]

        # Calculate the new head's position
        new_head = (head_r + direction[0], head_c + direction[1])

        # Check for collisions with walls
        if not (0 <= new_head[0] < self.size and 0 <= new_head[1] < self.size):
            print("Game Over: Hit the wall!")
            game_over = True
            return (game_over, apple_eaten, apple_type)

        # Check for self-collision with the snake's body
        # Check against the entire body exept for the tail, which will move.
        if new_head in self.snake[:-1]:
            print("Game Over: Hit its own tail!")
            game_over = True
            return (game_over, apple_eaten, apple_type)
        
        # Check the contents of the cell the snake is moving into
        next_cell_content = self.board[new_head[0]][new_head[1]]

        # Case 1: The snake eats green apple
        if next_cell_content == Cell.GREEN_APPLE:
            print("Ate a green apple! Snake grows.")
            apple_eaten = True
            apple_type = 'green'
            self.score += 1
            
            # Remove the eaten apple from the list and place a new one
            if new_head in self.green_apples:
                self.green_apples.remove(new_head)
                self._place_new_green_apple()

        # Case 2: the snake eats a red apple        
        elif next_cell_content == Cell.RED_APPLE:
            print("Ate a red apple! Snake shrinks.")
            apple_eaten = True
            apple_type = 'red'
            self.score = max(0, self.score - 1)
            self.red_apple = None
            self._place_new_red_apple()

            # The snake shrinks, so we remove the tail.
            if len(self.snake) > 1:
                tail = self.snake.pop()
                self.board[tail[0]][tail[1]] = Cell.EMPTY
            else:
                # If the snake has only one segment, eating a red apple
                # ends the game.
                print("Game Over: Snake shrunk to nothing!")
                game_over = True
                return (game_over, apple_eaten, apple_type) 

        # Case 3: The snake moves without eating anything
        else:
            # The snake moves normally, so pop the tail maintain length
            if self.snake:
                tail = self.snake.pop()
                self.board[tail[0]][tail[1]] = Cell.EMPTY

        # Finally, add the new head to the front of the snake and update
        # the board. 
        self.snake.insert(0, new_head)
        self.board[new_head[0]][new_head[1]] = Cell.SNAKE
        
        # Return the game state
        return (game_over, apple_eaten, apple_type)

    def get_vision_vectors(self):
        """
        Generates and returns the full horizontal and vertical vision vectors.
        """
        if not self.snake:
            return {"Horizontal": "No snake", "Vertical": "No snake"}
            
        head_r, head_c = self.snake[0]
        char_map = {
            Cell.EMPTY: "0",
            Cell.GREEN_APPLE: "G",
            Cell.RED_APPLE: "R",
        }
        
        # --- Build the Vertical Line ---
        vertical_line = ""
        
        # Scan upwards from the head
        r = head_r - 1
        while r >= 0:
            if (r, head_c) in self.snake:
                vertical_line = "S" + vertical_line
            else:
                cell_content = self.board[r][head_c]
                vertical_line = char_map[cell_content] + vertical_line
            r -= 1
        vertical_line = "W" + vertical_line
        
        # Add the head to the vertical line
        vertical_line += "H"
        
        # Scan downwards from the head
        r = head_r + 1
        while r < self.size:
            if (r, head_c) in self.snake:
                vertical_line += "S"
            else:
                cell_content = self.board[r][head_c]
                vertical_line += char_map[cell_content]
            r += 1
        vertical_line += "W"
        
        # --- Build the Horizontal Line ---
        horizontal_line = ""
        
        # Scan to the left from the head
        c = head_c - 1
        while c >= 0:
            if (head_r, c) in self.snake:
                horizontal_line = "S" + horizontal_line
            else:
                cell_content = self.board[head_r][c]
                horizontal_line = char_map[cell_content] + horizontal_line
            c -= 1
        horizontal_line = "W" + horizontal_line
        
        # Add the head to the horizontal line
        horizontal_line += "H"
        
        # Scan to the right from the head
        c = head_c + 1
        while c < self.size:
            if (head_r, c) in self.snake:
                horizontal_line += "S"
            else:
                cell_content = self.board[head_r][c]
                horizontal_line += char_map[cell_content]
            c += 1
        horizontal_line += "W"
        
        return {"Horizontal": horizontal_line, "Vertical": vertical_line}

    def print_board(self):
        """Prints a visual representation of the game board."""
        emoji_map = {
            Cell.EMPTY: "⬜",
            Cell.SNAKE: "🟦",
            Cell.GREEN_APPLE: "🍏",
            Cell.RED_APPLE: "🍎"
        }
        head_r, head_c = self.snake[0]

        print("-" * (self.size * 2 + 1))
        for r in range(self.size):
            row_str = "|"
            for c in range(self.size):
                if (r, c) == (head_r, head_c):
                    row_str += "🐍|"
                else:
                    row_str += emoji_map[self.board[r][c]] + "|"
            print(row_str)
        print("-" * (self.size * 2 + 1))
    
def main():
    agent = Agent()
    environment = SnakeEnvironment()
    game_over = False
    total_reward = 0

    # Initialize a variable to track the total reward for the episode
    total_reward = 0

    while not game_over:
        # 1. Get the current state
        vision_vectors_old = environment.get_vision_vectors()
        state_old = agent.get_state(vision_vectors_old)

        # Print the snake's vision for debugging
        print(f"Snake Vision (Horizontal): {vision_vectors_old['Horizontal']}")
        print(f"Snake Vision (Vertical): {vision_vectors_old['Vertical']}")

        state_old = agent.get_state(vision_vectors_old)
        # 2. Get the agent's action (direction)
        direction_to_move = agent.get_action(state_old, environment.snake)

        # 3. Play a step in the environment and get the outcome
        game_over, apple_eaten, apple_type = environment.move(direction_to_move)
        
        # 4. Get the new state
        vison_vectors_new = environment.get_vision_vectors()
        state_new = agent.get_state(vison_vectors_new)

        # 5. Calculate the reward
        reward = agent.get_reward(game_over, apple_eaten, apple_type)
        
        # Add the current step's reward to the total
        total_reward += reward

        # **This is the new part:** Print the reward for the current step.
        print(f"Step Reward: {reward}")

        # 6. Train the agent with the new experience
        agent.train_short_memory(state_old, direction_to_move, reward, state_new)

        environment.print_board()
        time.sleep(1.5)
        
    # The loop has ended, so the total_reward variable is now correct
    print(f"Game ended. Final Score: {environment.score}, Total Reward: {total_reward}")
    agent.n_games += 1

if __name__ == "__main__":
    main()