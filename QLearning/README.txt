Presentation of three different models : 100tr_model(Training iteration 100), 
                                         final_model(Training iteration 1000),  
                                         10000tr_model(Training iteration 10000)
                                         in .pkl format

Concerning the hyperparameters they have the same condition like below:
-self.learning_rate = 0.1
    The learning rate determines how much new information (the reward)
    overrides old information in the Q-table

-self.gamma = 0.40
    Gamma is the discount factor. It determines the importance of future rewards.
    A higher value makes the agent more forward-thinking.

-self.epsilon = 0
    Epsilon is the exploration rate. It controls the randomness of the agent's actions.
    It will decrease over time, moving from exploration to exploitation.

<<<Evaluation globale pour les trois models>>>
        100 times traning -> 2.4 of average score
        1000 times training -> 14 of average score
        10000 times training -> 19.20 average score