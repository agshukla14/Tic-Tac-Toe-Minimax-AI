import pygame
import sys

# REMEMBER TO ADD COMMENTS AS YOU GO!

class GuiView:
	"""
	Represents the GUI view of the Tic-Tac-Toe game.
	Handles window creation, rendering of menus, grid, pieces, and HUD.
	"""
	def __init__(self, width=900, height=700):
		"""
		Initializes pygame, creates the windowed display surface (900x700),
		loads fonts, and precomputes positions for the 3x3 board and UI buttons.
		"""
		self.pygame = pygame
		self.pygame.init()
		self.width = width
		self.height = height

		# Windowed mode (900 x 700) - accessible on any modern display
		self.display = pygame.display.set_mode((self.width, self.height))
		self.pygame.display.set_caption('Tic Tac Toe')

		self.bg_color = (255, 255, 215)
		self.display.fill(self.bg_color)
		self.clock = pygame.time.Clock()

		# Fonts for UI rendering (with fallback to default font if Comic Sans MS is unavailable)
		self.font_title = self.get_font('Comic Sans MS', 48)
		self.font_btn_normal = self.get_font('Comic Sans MS', 30)
		self.font_btn_hover = self.get_font('Comic Sans MS', 40)
		self.font_status = self.get_font('Comic Sans MS', 26)
		self.font_small = self.get_font('Comic Sans MS', 22)

		# Start Menu Button Rectangles
		self.btn_player_rect = pygame.Rect(300, 290, 300, 60)
		self.btn_computer_rect = pygame.Rect(300, 390, 300, 60)

		# End Game Button Rectangles
		self.btn_menu_rect = pygame.Rect(325, 315, 250, 50)
		self.btn_exit_rect = pygame.Rect(325, 405, 250, 50)

		# In-Game HUD Buttons (Menu top-left, Restart top-right)
		self.game_btn_menu_rect = pygame.Rect(30, 25, 110, 40)
		self.game_btn_restart_rect = pygame.Rect(760, 25, 110, 40)

		# 3x3 Board geometry (450 x 450 board centered horizontally)
		self.board_x = 225
		self.board_y = 150
		self.cell_size = 150

		# 9 Tile positions formatted as 4 corners:
		# [top-left, top-right, bottom-left, bottom-right]
		# Exactly matches the original data structure format.
		self.positions = {
			# Row 1:
			1: [[225, 150], [375, 150], [225, 300], [375, 300]],
			2: [[375, 150], [525, 150], [375, 300], [525, 300]],
			3: [[525, 150], [675, 150], [525, 300], [675, 300]],
			# Row 2:
			4: [[225, 300], [375, 300], [225, 450], [375, 450]],
			5: [[375, 300], [525, 300], [375, 450], [525, 450]],
			6: [[525, 300], [675, 300], [525, 450], [675, 450]],
			# Row 3:
			7: [[225, 450], [375, 450], [225, 600], [375, 600]],
			8: [[375, 450], [525, 450], [375, 600], [525, 600]],
			9: [[525, 450], [675, 450], [525, 600], [675, 600]],
		}

	def get_font(self, font_name, size):
		"""Safely gets a system font or falls back to Pygame's default font."""
		try:
			return self.pygame.font.SysFont(font_name, size)
		except Exception:
			return self.pygame.font.Font(None, size)

	def draw(self, state):
		"""
		Draws the current pieces (X and O) on to the screen based on state.board.
		"""
		for row in state.board:
			for tile in row:
				if tile["value"] != 0:
					position = self.positions[tile["position"]]
					if tile["value"] == 1:
						# Draw 'X' with two crossing diagonal lines
						self.pygame.draw.line(self.display, (0, 0, 0), [position[0][0] + 25, position[0][1] + 25], [position[3][0] - 25, position[3][1] - 25], 5)
						self.pygame.draw.line(self.display, (0, 0, 0), [position[1][0] - 25, position[1][1] + 25], [position[2][0] + 25, position[2][1] - 25], 5)
					else:
						# Draw 'O' with a circle centered in the cell
						center = [
							int(sum([position[0][0]*0.25, position[1][0]*0.25, position[2][0]*0.25, position[3][0]*0.25])),
							int(sum([position[0][1]*0.25, position[1][1]*0.25, position[2][1]*0.25, position[3][1]*0.25]))
						]
						self.pygame.draw.circle(self.display, (0, 0, 0), center, 50, 5)

	def draw_start_menu(self):
		"""
		Renders the main menu with interactive hover effects for 'v/s Player' and 'v/s Computer'.
		"""
		self.display.fill(self.bg_color)
		mouse = self.pygame.mouse.get_pos()

		# Title
		introText = self.font_title.render("Tic-Tac-Toe:", True, (0, 0, 0))
		title_rect = introText.get_rect(center=(self.width // 2, 170))
		self.display.blit(introText, title_rect)

		# Hover detection using button rectangles
		is_hover_player = self.btn_player_rect.collidepoint(mouse)
		is_hover_computer = self.btn_computer_rect.collidepoint(mouse)

		font_player = self.font_btn_hover if is_hover_player else self.font_btn_normal
		font_computer = self.font_btn_hover if is_hover_computer else self.font_btn_normal

		player_text = font_player.render("v/s Player", True, (0, 0, 0))
		player_rect = player_text.get_rect(center=self.btn_player_rect.center)
		self.display.blit(player_text, player_rect)

		computer_text = font_computer.render("v/s Computer", True, (0, 0, 0))
		computer_rect = computer_text.get_rect(center=self.btn_computer_rect.center)
		self.display.blit(computer_text, computer_rect)

	def draw_win_state(self, player):
		"""
		Renders the game over / victory screen with 'Menu' and 'Exit' buttons.
		"""
		self.display.fill(self.bg_color)
		mouse = self.pygame.mouse.get_pos()

		if player == "No one" or player == "Draw":
			win_message = "It's a Draw !!!"
		else:
			win_message = "Winner is {} !!!".format(player)

		introText = self.font_title.render(win_message, True, (0, 0, 0))
		title_rect = introText.get_rect(center=(self.width // 2, 200))
		self.display.blit(introText, title_rect)

		is_hover_menu = self.btn_menu_rect.collidepoint(mouse)
		is_hover_exit = self.btn_exit_rect.collidepoint(mouse)

		font_menu = self.font_btn_hover if is_hover_menu else self.font_btn_normal
		font_exit = self.font_btn_hover if is_hover_exit else self.font_btn_normal

		menu_text = font_menu.render("Menu", True, (0, 0, 0))
		menu_rect = menu_text.get_rect(center=self.btn_menu_rect.center)
		self.display.blit(menu_text, menu_rect)

		exit_text = font_exit.render("Exit", True, (0, 0, 0))
		exit_rect = exit_text.get_rect(center=self.btn_exit_rect.center)
		self.display.blit(exit_text, exit_rect)

	def draw_grid(self):
		"""
		Draws the 3x3 background grid on the screen.
		"""
		# Vertical grid lines
		self.pygame.draw.line(self.display, (0, 0, 0), [375, 150], [375, 600], 5)
		self.pygame.draw.line(self.display, (0, 0, 0), [525, 150], [525, 600], 5)
		# Horizontal grid lines
		self.pygame.draw.line(self.display, (0, 0, 0), [225, 300], [675, 300], 5)
		self.pygame.draw.line(self.display, (0, 0, 0), [225, 450], [675, 450], 5)

	def draw_game_hud(self, ai_mode, player_turn, model):
		"""
		Draws in-game status (whose turn it is) and navigation buttons (Menu and Restart).
		"""
		mouse = self.pygame.mouse.get_pos()

		# 'Menu' button (top-left)
		hover_menu = self.game_btn_menu_rect.collidepoint(mouse)
		font_menu = self.font_btn_normal if hover_menu else self.font_small
		menu_text = font_menu.render("Menu", True, (0, 0, 0))
		self.display.blit(menu_text, menu_text.get_rect(center=self.game_btn_menu_rect.center))

		# 'Restart' button (top-right)
		hover_restart = self.game_btn_restart_rect.collidepoint(mouse)
		font_restart = self.font_btn_normal if hover_restart else self.font_small
		restart_text = font_restart.render("Restart", True, (0, 0, 0))
		self.display.blit(restart_text, restart_text.get_rect(center=self.game_btn_restart_rect.center))

		# Status banner (top-center)
		if model.gameOver():
			sc = model.score()
			if sc == 10:
				status = "Player X Wins!"
			elif sc == -10:
				status = "Computer (O) Wins!" if ai_mode else "Player O Wins!"
			else:
				status = "It's a Draw!"
		else:
			if ai_mode:
				status = "Your Turn (X)"
			else:
				status = "Player X's Turn" if player_turn else "Player O's Turn"

		status_text = self.font_status.render(status, True, (0, 0, 0))
		self.display.blit(status_text, status_text.get_rect(center=(self.width // 2, 45)))
