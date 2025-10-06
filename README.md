🐍 Reinforcement Learning Snake Game

This project implements a Reinforcement Learning (RL) agent to play a variant 
of the classic Snake Game.
The goal of the agent (or the player, in manual mode) is to collect green apples 
while avoiding red apples and walls.
If the snake collides with a wall or its own body, the game ends.

📦 1. Installation

Before running the game, make sure all dependencies are installed.
You can do this easily by using the provided requirements.txt file:
    "python -m venv venv"
    "source venv/bin/activate"
    "pip install -r requirements.txt"

▶️ 2. Running the Game

To start the Snake Game manually, simply run:
    "python Snake_Game.py"
Use the following controls to move the snake:
    Key	Action
    W	Move Up
    A	Move Left
    S	Move Down
    D	Move Right
🍏 Game Rules

-Green apples → Increase your score and length.
-Red apples → Dangerous! Avoid them.
-Walls → Hitting a wall ends the game.
-Self-collision → The snake dies if it has no valid moves or runs into itself.

🧠 3. Autonomous Snake Agent

In addition to manual play, this project includes an autonomous Snake Agent 
implemented in Snake_Agent.py.
Unlike traditional Reinforcement Learning models that require training, this 
agent follows a rule-based or logic-driven approach to navigate the 
environment intelligently.

🎮 How to Run

To watch the autonomous snake in action, run:
    "python Snake_Agent.py"
The agent will automatically move toward green apples while avoiding:
    Red apples
    Walls
    Its own body
It uses a simple yet effective decision-making algorithm to select the safest 
and most rewarding moves based on the game state.

🧩 4. How It Works (Overview)

The agent analyzes the environment at each step (position of apples, walls, 
and snake body).
It selects the next move using internal logic (e.g., direction prioritization, 
distance to apple, collision prediction).
If you modify the speed of the snake modify the number of this line(at the end):
    # A small delay to make the game playable to watch
    time.sleep(0.7)
No external training or model files are required — all intelligence is 
implemented in code. 

💎 5. Reward Implementation (Part 4)

Before training the Reinforcement Learning agent, you must define the reward 
system that guides its learning process.
This logic is implemented in the file Reward_Snake.py.

At this stage, the snake is aware of rewards and penalties but still untrained 
— it does not yet know how to act optimally.
The reward system helps it learn from experience once training begins.

📂 Entering the Reward Directory

Before running this phase, make sure you are inside the Reward folder:
    "cd Reward"
Then execute the reward-based snake script:
    "python reward_Snake.py"

🧮 Reward Design

The snake’s goal is to reach a length of at least 10 cells and survive as long 
as possible.
Rewards and penalties are assigned as follows:

Situation	Reward	Description
Eats a green apple 🍏	Positive	Encourages the agent to collect green apples.
Eats a red apple 🍎	Negative	Punishes the agent for choosing dangerous actions.
Eats nothing	Small negative	Discourages inaction or wandering without progress.
Game over (hit wall, self, or zero length) 💀

⚠️ Important Note

The snake at this stage does not know anything — it moves randomly or foolishly 
because it hasn’t yet been trained. This phase only defines how rewards are 
computed; learning will come in the next step.

💾 6. Using and Customizing Trained Models

To make testing and experimentation easier, this project includes pretrained models 
with different training durations.
Each model file corresponds to the number of games used during training:
| Model File            | Training Games  | Description                                                                 |
| --------------------- | --------------- | --------------------------------------------------------------------------- |
| `10tr_model.pkl`      | 10 games        | Very early stage — the agent barely learns; mostly random movements.        |
| `1000tr_model.pkl`    | 1,000 games     | Intermediate learning — the agent starts showing intelligent moves.         |
| `1000000tr_model.pkl` | 1,000,000 games | Fully trained — smooth, consistent gameplay with strong avoidance behavior. |


These models can be used directly in evaluation mode (see Section 8).
    "python Eval_Reward_Snake.py --eval --model final_model.pkl"

⚙️ Customizing the Training Duration and Model Name

If you want to train your own model with a different number of games or save it under a 
custom name, you can modify two simple lines inside Eval_Reward_Snake.py, near the 
training section of the main() function.

# Training mode
else:  # This is training mode
    print("Starting training mode...")
    num_games = 10   # ← Change this number for how many games to train
    ...
    agent.save_model("10tr_model.pkl")  # ← Change this name to save under a new file

🛠️ To customize:

Change num_games to control how long the model trains:
    num_games = 10000

Change the model name to save it with your preferred filename:
    agent.save_model("10000tr_model.pkl")

Then simply run to train the model:
    "python Eval_Reward_Snake.py"

🧠 Running Evaluation

Once you have chosen which model to test, run the following command from the 
QLearning 
directory:
    "python Eval_Reward_Snake.py --eval --model 1000tr_model.pkl"
Replace 1000tr_model.pkl with any of the pretrained models you want to test
(10tr_model.pkl, 1000tr_model.pkl, or 1000000tr_model.pkl).

🎮 What Happens During Evaluation

The agent runs 5 automatic game rounds using the chosen trained model.
During each round, the console shows:
    The final score for that round.
After all 5 games, the script calculates and prints the average score
    Evaluation completed. Average Score over 5 games: 8.60
This allows you to compare performance between different models easily.
