class Model():
	"""
	Model for the Tic-Tac-Toe game.
	"""
	def __init__(self):
		"""
		Initializes the game model.
		"""
		position = 0
		self.board = [[{"position": 0, "value": 0} for y in range(0, 3)] for x in range(0, 3)]

		#Set integer positions for each tile on the board...
		position = 0
		for row in self.board:
			for tile in row:
				position += 1
				tile["position"] = position

		# Number of tiles currently empty on the baord.
		self.depth = 9

		# The two playes of the game.
		self.players = ['X', 'O']

	def move(self, player, position):
		"""
		Places designated value on given position for a given player.
		By mutating the "value" field in self.board.
		Also, mutates remaining number of empty tiles on the board.
		1 for 'X' and '-1' for 'O'
		params: player: 'X' or 'O'
				position: 1...9
		errors: 
				- Invalid move.
				- Invalid player.
				- Position out of bounds.
		"""
		for row in self.board:
			for tile in row:
				if tile["position"] == position:
					if tile["value"] == 0:
						if player == 'X':
							tile["value"] = 1
							self.depth -= 1
							return
						elif player == 'O':
							tile["value"] = -1
							self.depth -= 1
							return
						else:
							raise Exception("Player {} not found.".format(player))
					else:
						raise Exception("Invalid move at {}.".format(position))
		raise Exception("Out of bounds {}.".format(position))

	def undo_move(self, player, position):
		"""
		Places designated value on given position for a given player.
		By mutating the "value" field in self.board.
		Also, mutates remaining number of empty tiles on the board.
		1 for 'X' and '-1' for 'O'
		params: player: 'X' or 'O'
				position: 1...9
		errors: 
				- Invalid move.
				- Invalid player.
				- Position out of bounds.
		"""
		for row in self.board:
			for tile in row:
				if tile["position"] == position:
					if tile["value"] != 0:
						tile["value"] = 0
						self.depth += 1
					else:
						raise Exception("No move to undo at {}.".format(position))



	def empty_tiles(self):
		"""
		Returns a list of all empty remaining tiles.
		"""
		return [[tile["position"] for tile in row if tile["value"] == 0] for row in self.board]


	def score(self):
		"""
		Mutates self.winner in the case a winning possibility is satisfied or if all tiles on the board are filled.
		Returns a boolen for if the game is over.
		"""
		

		verticals = [[row[i]["value"] for row in self.board] for i in range(len(self.board))]
		index = 2
		diagonals = [[self.board[num][num]["value"] for num in range(0, 3)], [self.board[num][index - num]["value"] for num in range(0, 3)]]
		winPossibilities = []
		winPossibilities.append([[tile["value"] for tile in row] for row in self.board])
		winPossibilities.append(verticals)
		winPossibilities.append(diagonals)

		for possibility in winPossibilities:
			for row in possibility:
				if sum(row) == 3:
					return 10
				elif sum(row) == -3:
					return -10

		return 0

	def gameOver(self):
		if self.score() > 0 or self.depth <= 0 or self.score() < 0:
			return True
		else:
			return False