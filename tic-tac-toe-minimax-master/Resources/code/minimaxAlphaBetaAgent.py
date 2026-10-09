from math import inf
import copy

class MinimaxAlphaBetaAgent():

	def __init__(self):
		return
	
	def staticEval(self, state):
		return state.score()

	def minimax_alpha_beta(self, state, depth, alpha, beta, isMax):
		if state.gameOver() or depth == 0:
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

	def choose(self, state, player):
		return self.minimax_alpha_beta(state, len(self.get_all_next_moves(state)), -inf, inf, player)

	def get_all_next_moves(self, state):
		moves = []
		for row in state.empty_tiles():
			for tile in row:
				moves.append(tile)
		return moves
