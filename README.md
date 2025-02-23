# Kun_man---Game-Project-Based-on-Q-Learning
## **Project Overview**

Kun_man is a game similar to Pac-Man. In this game, players need to control a basketball elf named MAN to evade the pursuit of a group of cute enemies called KUN and help MAN collect all the coins scattered on the map to complete the game. This game project is developed using the Pygame library and integrates the Q-learning reinforcement learning algorithm, enabling game characters to optimize their game strategies through continuous learning and achieve the goals of clearing levels and obtaining high scores.

## **Technical Realization**

Programming Language: Python

Main Libraries:pygame,numpy,matplotlib,pyautogui,pickle

## **Installation and Execution**

### **1. Install dependencies**

Ensure that your system has installed the Python environment.
Install the required libraries with pip:

	pip install pygame
 	pip install numpy
	pip install pickle
	pip install pyautogui
 	pip install matplotlib
	
### **2. Run Project**

After downloading this project, enter the project folder:

	cd kun_man
 
Play the game:

	python main.py
 
Perform Q-learning:

***Notice: Please ensure that your computer has sufficient computing power and that you have ample time for the training before executing the following code. This is because the Q-learning algorithm employed in this project will undergo 500 training cycles. After every 50 training sessions, the Q-table results obtained from the training will be saved, it is not recommended to stop the training process midway.***

***The currently set 500 training sessions are only for testing purposes. Generally, it is not possible to successfully train the model to clear the game with this number of sessions. If you are determined to train the model and expect to be able to clear the game, you can modify the number of training sessions to 5000 in the Q_learning.py file.***

***If your computer's performance is insufficient to support the completion of the entire training, you can open the result folder in the project directory. This folder contains the Q-table files (in .pkl format) saved from the 50th to the 350th training sessions, you can carry out subsequent operations based on these saved results.***

	python Q-learning.py

### **3.Load and Evaluate Q-learning：**

To read the Q-table file of a single training result：

	python load.py XX

 XX represents the corresponding number of times, such as 50 representing 50.pkl

To read the Q-table files of multiple training results and evaluate the effectiveness, run the following code:

	python load.py XX-YY
 
XX-YY represents reading all pkl files between XX and YY, for example: 50-350 represents 50.pkl, 100.pkl, 150.pkl ··· 350.pkl.

## **Code Structure Explanation**

**Sprites.py**: Defines sprite classes for walls, players, 和 enemies, including appearance, position, 和 interaction rules.

**Levels.py**: Sets up game levels, specifying enemy movement patterns and the positions of walls and gates.

**main.py**: The main entry point. Initializes the game environment and game logic for users to play, without Q - learning training.

**Q_learning.py**: Handles Q - learning training and stores Q - tables at regular intervals.

**load.py**: Reads stored Q - tables and evaluates training results using clearance rate and score, presenting results in line plots.

## **Q - learning Parameter Explanation**

**Learning Rate** (ALPHA = 0.1): Controls the influence of new experiences on Q - value updates.

**Discount Factor** (GAMMA = 0.9): Balances immediate and future rewards.

**Initial Exploration Rate** (INITIAL_EPSILON = 0.9): Determines the initial exploration probability.

**Exploration Rate Decay Value** (EPSILON_DECAY = 0.05): Amount by which exploration rate decreases.

**Minimum Exploration Rate** (MIN_EPSILON = 0.1): Sets the lower limit of exploration rate.

**Exploration Rate Decay Interval** (DECAY_INTERVAL = 10): Number of training sessions between decays.

## **Reward Calculation Mechanism**

**Collide with Ghost**: -100, to avoid fatal collisions.

**Eat Food**: +10, to encourage food collection.

**Clear Level**: WIN_BONUS (2000), to motivate level completion.

**No Bean Eaten**: -NO_BEAN_PENALTY (10), to prevent inactivity.

**Exceed Max Steps**: -100, to ensure timely decision - making.

**Other Situations**: -1, to encourage effective actions.
