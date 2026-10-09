from model import Model
from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
import copy

class TextView():
	def __init__(self, state):
		self.currState = state
		self.initState = state
		self.gameRepr = ""
		self.rules = ""
		self.rules +="\n\n"
		for row in self.currState.board:
			for tile in row:
				self.rules +="| {} |".format(tile["position"])
			self.rules += "\n"
		self.rules += "\n"

	def draw(self):
		"""
		Creates a text representation of the tic tac toe board, Also displays positions on the board the player can choose..
		"""
		self.gameRepr = ""		
		for row in self.currState.board:
			for tile in row:
				if tile["value"] != 0:
					self.gameRepr +="| {} |".format('X' if tile["value"] == 1 else 'O')
				else:
					self.gameRepr +="|   |"
			self.gameRepr += "\n"
		return self.gameRepr

	def reset(self):
		"""
		Resets the game to its initial state.
		"""
		self.currState = self.initState

def main(view, agent):
	player = 1
	temp = ''
	while not view.currState.gameOver():
		temp = 'X' if player == 1 else 'O'
		print("=======================================================================================")
		print(view.rules)
		print("=======================================================================================\n\n")
		move = 0
		if player == 1:
			move = input("Player {}' turn:\n".format(temp))
		else:
			print("Player O's turn:")
			depth = len(agent.get_all_next_moves(view.currState))
			print(depth)
			#move = agent.minimax(view.currState, depth, False)[0]
			move = agent.choose(view.currState, False)[0]
			print(move)
		view.currState.move(temp, int(move))
		print("=======================================================================================")
		print(view.draw())
		print(view.currState.empty_tiles())
		player = -player
	if view.currState.score() == 10:
		print("Player X wins!")

	elif view.currState.score() == -10:
		print("Player O wins!")

	else:
		print("It's a draw!")

if __name__ == '__main__':
	game = Model()
	text = TextView(game)
	agent = MinimaxAlphaBetaAgent()
	#agent = MinimaxAgent()
	main(text, agent)

"""
text = TextView(game)
text.currState.move('X', 9)
text.currState.move("O", 1)

text.currState.move('X', 3)
text.currState.move("O", 8)

move = agent.choose(text.currState, True)

print(move)

text.currState.move('X', move[0])

print(text.draw())
"""


