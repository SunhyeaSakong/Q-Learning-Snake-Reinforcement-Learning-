import random
from enum import Enum

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

# --- A simple game loop to test the functionality ---
if __name__ == "__main__":
    game = SnakeEnvironment(size=10)
    game_over = False
    current_direction = RIGHT
    
    direction_map = {
        'w': UP, 's': DOWN, 'a': LEFT, 'd': RIGHT,
        'W': UP, 'S': DOWN, 'A': LEFT, 'D': RIGHT
    }

    print("Welcome to the Snake Game!")
    print("Use 'w', 'a', 's', 'd' to move. Press 'q' to quit.")

    while not game_over:
        game.print_board()
        print(f"Current Score: {game.score}")
        
        vision_vectors = game.get_vision_vectors()
        if vision_vectors:
            print(f"Horizontal line: {vision_vectors['Horizontal']}")
            print(f"Vertical line: {vision_vectors['Vertical']}")
        
        move_input = input("Enter a move: ")
        
        if move_input.lower() == 'q':
            print("Quitting game.")
            break
        
        if move_input in direction_map:
            new_direction = direction_map[move_input]
            if (new_direction[0] * -1 != current_direction[0] or 
                new_direction[1] * -1 != current_direction[1]):
                current_direction = new_direction
            
            game_over = not game.move(current_direction)
        else:
            print("Invalid input. Use 'w', 'a', 's', 'd'.")
            
    print("Final Score:", game.score)