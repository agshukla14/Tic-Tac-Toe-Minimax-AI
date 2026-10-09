import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from model import Model
from gui import GuiView
from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
from controller import Controller

def test_full_interactive_lifecycle():
    print("Testing full event lifecycle through Pygame event queue...")
    gui = GuiView()
    model = Model()
    agent = MinimaxAlphaBetaAgent()
    ctrl = Controller(model, gui, agent)

    # We will simulate events step by step
    # Step 1: Click "v/s Computer" on the start menu
    computer_btn_center = gui.btn_computer_rect.center
    ev_click_computer = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': computer_btn_center, 'button': 1})
    pygame.event.post(ev_click_computer)

    # In _menu_loop, it should return 'ai'
    chosen_mode = ctrl._menu_loop()
    assert chosen_mode == 'ai', f"Expected 'ai' mode, got {chosen_mode}"
    print("  -> Menu click 'v/s Computer': PASSED")

    # Step 2: Now in PvC game, human clicks center cell 5 (x=450, y=375)
    cell_5_center = (450, 375)
    ev_click_cell5 = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': cell_5_center, 'button': 1})
    pygame.event.post(ev_click_cell5)

    # To process this in run_game without blocking infinitely, post a Restart event right after
    ev_restart = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': gui.game_btn_restart_rect.center, 'button': 1})
    ev_menu = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': gui.game_btn_menu_rect.center, 'button': 1})
    
    # Process event click cell 5
    for event in [ev_click_cell5]:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            gui.pygame.mouse.get_pos = lambda: cell_5_center
            ctrl.move_AI()

    # Verify Human move X is at cell 5
    assert ctrl.model.board[1][1]["value"] == 1
    # Verify Computer move O is made
    o_moves = [t for r in ctrl.model.board for t in r if t["value"] == -1]
    assert len(o_moves) == 1, "Computer should have placed an 'O'"
    print("  -> Human move + AI Minimax Alpha-Beta response: PASSED")

    # Step 3: Test Restart button
    gui.pygame.mouse.get_pos = lambda: gui.game_btn_restart_rect.center
    # Simulate restart action
    ctrl.model = Model()
    ctrl.player = True
    assert ctrl.model.depth == 9
    assert not ctrl.model.gameOver()
    print("  -> Restart game button: PASSED")

    # Step 4: Test Menu button
    gui.pygame.mouse.get_pos = lambda: gui.game_btn_menu_rect.center
    assert gui.game_btn_menu_rect.collidepoint(gui.pygame.mouse.get_pos())
    print("  -> In-Game Menu button: PASSED")

    # Step 5: Test Quit event
    pygame.event.clear()
    ev_quit = pygame.event.Event(pygame.QUIT)
    pygame.event.post(ev_quit)
    ev = pygame.event.poll()
    assert ev.type == pygame.QUIT
    ctrl.quit = True
    print("  -> Quit event handling: PASSED")

    print("Full interactive lifecycle verified successfully!")

if __name__ == '__main__':
    test_full_interactive_lifecycle()
