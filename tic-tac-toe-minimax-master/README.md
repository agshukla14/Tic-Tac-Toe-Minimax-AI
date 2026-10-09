# Tic-Tac-Toe

## Introduction:

A basic version of the popular game "Tic Tac Toe" also known as Knots & Crosses.
The purpose of this project from me was to learn and apply the Minimax algorithm with Alpha Beta Pruning.

## Dependencies

This project is built on base Python 3.7.2 along with the pygame library for the gui.

Installing pygame,
Open Console:



		pip install pygame
		

## How to execute code:

You will first have to download the repository as a .zip file and then extract the contents into a folder. Then you can open the folder as in a compiler such as PyCharm or SublimeText3.

### GUI

To run the gui version of the project through a python complier, you will need to run the Tic-Tac-Toe.py file in Resources->code

Example of GUI Gameplay:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/gameplay.jpg)

### Text based

To run the text version the project through a python complier, you will need to run the textBased.py file in Resources->code

Example of Text based version gameplay:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/textGamePlay.jpg)


## Minimax and Alpha Beta Pruning:

"Minimax is a kind of backtracking algorithm that is used in decision making and game theory to find the optimal move for a player, assuming that your opponent also plays optimally. It is widely used in two player turn-based games such as Tic-Tac-Toe

In Minimax the two players are called maximizer and minimizer. The maximizer tries to get the highest score possible while the minimizer tries to do the opposite and get the lowest score possible.

Every board state has a value associated with it. In a given state if the maximizer has upper hand then, the score of the board will tend to be some positive value. If the minimizer has the upper hand in that board state then it will tend to be some negative value. The values of the board are calculated by some heuristics which are unique for every type of game."

                                                                               (Explanation from Geeks for Geeks, see resources)

### Pseudocode for Minimax:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/Pseudocode%20Minimax.jpg)

### Minimax Example:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/Minimax%20Example.jpg)

### Minimax Properties:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/Minimax%20Properties.jpg)

### Psuedocode for Alpha-Beta-Pruning:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/Alpha-Beta%20Pruning%20Algorithm.jpg)

### Alpha-Beta-Pruning done on the given Minimax Example:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/Alpha-Beta-Pruning-Example.jpg)

### Minimax Tic Tac Toe Game Tree Example:

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/gameTreeMinimax.jpg)

## My application of Minimax-Alpha-Beta-Pruning:



	def minimax_alpha_beta(self, state, depth, alpha, beta, isMax):
			if state.gameOver() or depth is 0:
				return -1, state.score() - depth
			if isMax:
				bestValue = -1, -inf
			else:
				bestValue = -1, inf

			for s in self.get_all_next_moves(state):
				player = 'X' if isMax else 'O'
				state.move(player, s)
				value = s, self.minimax_alpha_beta(state, depth - 1, alpha, beta, not isMax)[1]
				state.undo_move(player, s)
				if isMax:
					bestValue = max(bestValue, value, key= lambda i: i[1])
					alpha = max(alpha, bestValue[1])
					if alpha >= beta:
						break
						#return s, alpha
				else:
					bestValue = min(bestValue, value, key= lambda i: i[1])
					beta = min(beta, value[1])
					if alpha >= beta:
						break
						#return s, beta
			return bestValue


   Seen in Resources->code->minimaxAlphaBetaAgent.py


## How to run the Game?

### For Windows:
1. Download the repository and unzip it.
2. Unzip the "Tic-Tac-Toe Game".zip file
![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/TTTReadme1.jpg)
![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/TTTReadme2.jpg)
4. Open the extracted folder and navigate to the "Tic-Tac-Toe" Folder
5. Scroll down to the "Tic-Tac-Toe.exe" file and doiable click it to run
![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/TTTReadme3.jpg)
6. Voila! You're in the game!

![alt text](https://github.com/Pranshu-Bahadur/Tic-Tac-Toe/blob/master/Resources/images/TTTReadme4.jpg)


## Resources:

MIT Artifical Intelligence, Lecture 6: Search: Games, Minimax, and Alpha-Beta:
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/lecture-videos/lecture-6-search-games-minimax-and-alpha-beta/

Pesudocode for Minimax and Alpha-Beta Pruning from MIT:
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/tutorials/MIT6_034F10_tutor02.pdf

CS4100 Lecture Notes, Northeastern University, Prof.Robert Platt, Adversarial Search:
http://www.ccs.neu.edu/home/rplatt/cs4100_spring2018/slides/adversarial_search.pdf

GeeksforGeeks Minimax Explanation:
https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/

Geeksforgeeks Alpha Beta Pruning Explanation:
https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

Another Tic-Tac-Toe, Minimax Repo:
https://github.com/Cledersonbc/tic-tac-toe-minimax


#### Explanation Images are taken from CS4100 Lecture Slides on Adversarial Search by Robert Platt.

