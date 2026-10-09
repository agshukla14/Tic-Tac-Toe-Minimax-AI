from gui import GuiView
from model import Model
from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
import pygame

class Controller:
	"""
	Represents a Controller that handles user input, AI decisions, 
	state transitions, and the main game loops.
	"""
	def __init__(self, model, view, agent):
		"""
		Initializes the game controller with a model, view, and an AI agent.
		"""
		self.model = model
		self.view = view
		self.agent = agent
		self.quit = False
		self.ai = False
		self.player = True  # True for Player X (Human), False for Player O

	def run_intro(self):
		"""
		Main entry point that manages the start menu and game sessions.
		Uses a non-recursive loop to safely allow multiple matches and menu returns.
		"""
		while not self.quit:
			self.model = Model()
			self.player = True

			mode = self._menu_loop()
			if mode == 'quit':
				break
			elif mode == 'player':
				self.ai = False
				self.run_game()
			elif mode == 'ai':
				self.ai = True
				self.run_game()

		pygame.quit()

	def _menu_loop(self):
		"""
		Runs the start menu event loop.
		Returns 'player', 'ai', or 'quit'.
		"""
		while not self.quit:
			for event in self.view.pygame.event.get():
				if event.type == self.view.pygame.QUIT:
					self.quit = True
					return 'quit'
				if event.type == self.view.pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse = getattr(event, 'pos', self.view.pygame.mouse.get_pos())
					# Check "v/s Player" button
					if self.view.btn_player_rect.collidepoint(mouse):
						return 'player'
					# Check "v/s Computer" button
					if self.view.btn_computer_rect.collidepoint(mouse):
						return 'ai'

			self.view.draw_start_menu()
			self.view.pygame.display.update()
			self.view.clock.tick(60)

		return 'quit'

	def run_game(self):
		"""
		Main game loop of the tic-tac-toe game.
		"""
		game_active = True
		while game_active and not self.quit:
			for event in self.view.pygame.event.get():
				if event.type == self.view.pygame.QUIT:
					self.quit = True
					return
				if event.type == self.view.pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse = getattr(event, 'pos', self.view.pygame.mouse.get_pos())

					# Check in-game Menu button
					if self.view.game_btn_menu_rect.collidepoint(mouse):
						return

					# Check in-game Restart button
					if self.view.game_btn_restart_rect.collidepoint(mouse):
						self.model = Model()
						self.player = True
						continue

					# Check board moves if game is still active
					if not self.model.gameOver():
						if self.ai:
							self.move_AI(mouse)
						else:
							if self.move(mouse):
								self.player = not self.player

			# Redraw game screen
			self.view.display.fill(self.view.bg_color)
			self.view.draw_grid()
			self.view.draw(self.model)
			self.view.draw_game_hud(self.ai, self.player, self.model)
			self.view.pygame.display.update()
			self.view.clock.tick(60)

			# If a terminal state was reached, display final board briefly then show win screen
			if self.model.gameOver():
				self.view.pygame.time.delay(500)
				action = self.run_end_game()
				if action == 'restart':
					self.model = Model()
					self.player = True
					continue
				else:
					# Return to start menu
					return

	def run_end_game(self):
		"""
		Victory / End-Game screen showing the winner and 'Menu' and 'Exit' buttons.
		Returns 'menu', 'restart', or 'quit'.
		"""
		player = "No one"
		if self.model.score() == 10:
			player = 'Player X'
		elif self.model.score() == -10:
			player = 'Player O'

		while not self.quit:
			for event in self.view.pygame.event.get():
				if event.type == self.view.pygame.QUIT:
					self.quit = True
					return 'quit'
				if event.type == self.view.pygame.MOUSEBUTTONDOWN and event.button == 1:
					mouse = getattr(event, 'pos', self.view.pygame.mouse.get_pos())
					# "Menu" button
					if self.view.btn_menu_rect.collidepoint(mouse):
						return 'menu'
					# "Exit" button
					if self.view.btn_exit_rect.collidepoint(mouse):
						self.quit = True
						return 'quit'

			self.view.draw_win_state(player)
			self.view.pygame.display.update()
			self.view.clock.tick(60)

		return 'quit'

	def move(self, mouse=None):
		"""
		Player vs Player input handler.
		Returns True if a valid move was made, False otherwise.
		"""
		if mouse is None:
			mouse = self.view.pygame.mouse.get_pos()
		for pos in range(1, len(self.view.positions) + 1):
			position = self.view.positions[pos]
			# Check if mouse is inside cell bounding box
			if position[0][0] <= mouse[0] <= position[1][0] and position[0][1] <= mouse[1] <= position[2][1]:
				if pos in self.agent.get_all_next_moves(self.model):
					current_player = 'X' if self.player else 'O'
					self.model.move(current_player, pos)
					return True
		return False

	def move_AI(self, mouse=None):
		"""
		Player vs Computer AI input handler.
		Human plays 'X', Computer AI plays 'O' using Minimax with Alpha-Beta pruning.
		Returns True if human made a move, False otherwise.
		"""
		if mouse is None:
			mouse = self.view.pygame.mouse.get_pos()
		for pos in range(1, len(self.view.positions) + 1):
			position = self.view.positions[pos]
			# Check if mouse is inside cell bounding box
			if position[0][0] <= mouse[0] <= position[1][0] and position[0][1] <= mouse[1] <= position[2][1]:
				if pos in self.agent.get_all_next_moves(self.model):
					# 1. Apply Human 'X' move
					self.model.move('X', pos)

					# 2. Render Human move immediately on the screen
					self.view.display.fill(self.view.bg_color)
					self.view.draw_grid()
					self.view.draw(self.model)
					self.view.draw_game_hud(self.ai, self.player, self.model)
					self.view.pygame.display.update()

					# 3. If game is not over, calculate and apply Computer 'O' move
					if not self.model.gameOver() and len(self.agent.get_all_next_moves(self.model)) > 0:
						self.view.pygame.time.delay(150)
						ai_move = self.agent.choose(self.model, False)[0]
						if ai_move != -1:
							self.model.move('O', ai_move)
					return True
		return False
