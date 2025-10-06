import random
import time
from enum import Enum
from agent import Agent

# --- New: Define directions for clarity ---
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
        Moves the snake and updates the game state.
        Returns False if the game is over, True otherwise.
        """
        head_r, head_c = self.snake[0]
        new_head = (head_r + direction[0], head_c + direction[1])
        
        if not (0 <= new_head[0] < self.size and 0 <= new_head[1] < self.size):
            print("Game Over: Hit the wall!")
            return False
            
        if new_head in self.snake and new_head != self.snake[-1]:
            print("Game Over: Collided with own tail!")
            return False

        next_cell = self.board[new_head[0]][new_head[1]]

        if next_cell == Cell.GREEN_APPLE:
            print("Ate a green apple! Snake grows.")
            self.score += 1
            self.green_apples.remove(new_head)
            self._place_new_green_apple()
        elif next_cell == Cell.RED_APPLE:
            print("Ate a red apple! Snake shrinks.")
            self.score = max(0, self.score - 1)
            self.red_apple = None
            tail = self.snake.pop()
            self.board[tail[0]][tail[1]] = Cell.EMPTY
            if not self.snake:
                print("Game Over: There is no snake!")
                return False
            self._place_new_red_apple()
        else:
            tail = self.snake.pop()
            self.board[tail[0]][tail[1]] = Cell.EMPTY

        self.snake.insert(0, new_head)
        self.board[new_head[0]][new_head[1]] = Cell.SNAKE
        
        return True

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

    def agent_decide_action(vision_vectors):
        """
        Takes the vision data and returns the direction(UP, DOWN, LEFT, RIGHT)
        """
        horizontal_vision = vision_vectors['Horizontal']
        vertical_vision = vision_vectors['Vertical']

        # Find the position of head and any green apples
        h_horiz_index = horizontal_vision.find('H')
        g_horiz_index = horizontal_vision.find('G')
        h_vert_iindex = vertical_vision.find('H')
        g_vert_index = vertical_vision.find('G')

        # 1. Prioritize Green Apples
        # Check for geen apple horizontally
        if g_horiz_index != -1 and g_horiz_index != h_horiz_index:
            if g_horiz_index > h_horiz_index:
                return RIGHT
            else:
                return LEFT
            
        # Ceck for green apple vertically
        if g_vert_index != -1 and g_vert_index != h_vert_iindex:
            if g_vert_index > h_vert_iindex:
                return DOWN
            else: 
                return UP
            
        # 2. Safty First: Avoid Walls and body
        safe_moves = []
        # Check Up: if the first chracter after H is not W or S
        if vertical_vision[vertical_vision.find('H') - 1] not in ['W', 'S']:
            safe_moves.append(UP)
        # Check DOWN
        if vertical_vision[vertical_vision.find('H') + 1] not in ['W', 'S']:
            safe_moves.append(DOWN)
        # Check LEFT
        if horizontal_vision[horizontal_vision.find('H') - 1] not in ['W', 'S']:
            safe_moves.append(LEFT)
        # Check RIGHT
        if horizontal_vision[horizontal_vision.find('H') + 1] not in ['W', 'S']:
            safe_moves.append(RIGHT)

        # 3. Take the safest move, or a Random Safe Move
        if len(safe_moves) > 0:
            return random.choice(safe_moves)
        else:
            # This means that the snake is trapped. game over is inevitable
            # We return a defalt move because the game ends here.
            return RIGHT 
    

# --- A simple game loop to test the functionality ---
if __name__ == "__main__":
    game = SnakeEnvironment(size=10)
    # Initiation the Agent
    snake_agent = Agent()
    game_over = False

    # Map the direction tuples to readable string for print Agent's decision
    direction_names = {
        UP: "UP", 
        DOWN: "DOWN",
        LEFT: "LEFT", 
        RIGHT: "RIGHT"
    }

    print("Welcome to the Snake Game! The agent will now play automatically")

    while not game_over:
        game.print_board()
        print(f"Current Score: {game.score}")
        
        vision_vectors = game.get_vision_vectors()
        print(f"Horizontal line: {vision_vectors['Horizontal']}")
        print(f"Vertical line: {vision_vectors['Vertical']}")
        
        # Agent decides to move
        current_direction = snake_agent.decide_action(vision_vectors)

        # Print the agent's decision
        print(f"Agents decision: {direction_names.get(current_direction, 'Unknown')}")

        # The game environment takes the action from the agent
        game_over = not game.move(current_direction)

        # A small delay to make the game playable to watch
        time.sleep(0.7)
            
    print("Final Score:", game.score)
