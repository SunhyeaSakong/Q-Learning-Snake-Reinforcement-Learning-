# 'agent.py'
import random

#Define the directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

class Agent:
    """
    A agent that decides the snake's next action based on tis vision.
    This agent's policy is to prioritize going toward green apples.
    """

    def decide_action(self, vision_vectors):
        """
        Takes a vision data and returns a direction(UP, DOWN, LEFT. RIGHT).
        """

        horizontal_vision = vision_vectors['Horizontal']
        vertical_vision = vision_vectors['Vertical']

        # 1. First identify all safe moves.
        safe_moves = []

        # Check if moving UP is safe
        h_vert_index = vertical_vision.find('H')
        if h_vert_index > 0 and vertical_vision[h_vert_index - 1] not in ['W', 'S']:
            safe_moves.append(UP)

        # Check DOWN
        if h_vert_index < len(vertical_vision) - 1 and vertical_vision[h_vert_index + 1] not in ['W', 'S']:
            safe_moves.append(DOWN)

        # Check LEFT
        h_horiz_index = horizontal_vision.find('H')
        if h_horiz_index > 0 and horizontal_vision[h_horiz_index - 1] not in ['W', 'S']:
            safe_moves.append(LEFT)

        # Check RIGHT
        if h_horiz_index < len(horizontal_vision) - 1 and horizontal_vision[h_horiz_index + 1] not in ['W', 'S']:
            safe_moves.append(RIGHT)

        # If there are no safe moves, the agent is trapped.
        if not safe_moves:
            return UP # Or a default move, though the game will end soon anyway.

        # 2. From the safe moves, see if any lead to a green apple.
        for move in safe_moves:
            if move == UP and 'G' in vertical_vision[:vertical_vision.find('H')]:
                return UP
            if move == DOWN and 'G' in vertical_vision[vertical_vision.find('H'):]:
                return DOWN
            if move == LEFT and 'G' in horizontal_vision[:horizontal_vision.find('H')]:
                return LEFT
            if move == RIGHT and 'G' in horizontal_vision[horizontal_vision.find('H'):]:
                return RIGHT
            
        # 3. If no safe move leads to an apple, choose one randomly.
        return random.choice(safe_moves)
            
        
        