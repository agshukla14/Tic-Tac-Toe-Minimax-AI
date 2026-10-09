import os
import sys

# Ensure headless execution for Pygame during automated testing if needed
# (or test with SDL dummy driver if headless, or native driver)
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
from model import Model
from gui import GuiView
from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
from controller import Controller

def test_model():
    print("Testing Model...")
    m = Model()
    assert m.depth == 9
    assert not m.gameOver()
    assert m.score() == 0

    # Move X at 1
    m.move('X', 1)
    assert m.depth == 8
    assert m.board[0][0]["value"] == 1

    # Occupied move raises Exception
    try:
        m.move('O', 1)
        assert False, "Should have raised exception for occupied tile"
    except Exception as e:
        assert "Invalid move" in str(e)

    # Undo move
    m.undo_move('X', 1)
    assert m.depth == 9
    assert m.board[0][0]["value"] == 0

    # Test X horizontal win
    m.move('X', 1)
    m.move('O', 4)
    m.move('X', 2)
    m.move('O', 5)
    m.move('X', 3)
    assert m.gameOver()
    assert m.score() == 10
    print("  -> Model horizontal win: PASSED")

    # Test O vertical win
    m2 = Model()
    m2.move('X', 1)
    m2.move('O', 2)
    m2.move('X', 4)
    m2.move('O', 5)
    m2.move('X', 9)
    m2.move('O', 8)
    assert m2.gameOver()
    assert m2.score() == -10
    print("  -> Model vertical win: PASSED")

    # Test Diagonal win
    m3 = Model()
    m3.move('X', 1)
    m3.move('O', 2)
    m3.move('X', 5)
    m3.move('O', 3)
    m3.move('X', 9)
    assert m3.gameOver()
    assert m3.score() == 10
    print("  -> Model diagonal win: PASSED")

    # Test Draw
    # X O X
    # X O O
    # O X X
    m4 = Model()
    moves = [('X', 1), ('O', 2), ('X', 3), ('O', 5), ('X', 4), ('O', 6), ('X', 8), ('O', 7), ('X', 9)]
    for p, pos in moves:
        m4.move(p, pos)
    assert m4.gameOver()
    assert m4.score() == 0
    assert m4.depth == 0
    print("  -> Model draw detection: PASSED")

def test_minimax():
    print("Testing MinimaxAlphaBetaAgent...")
    agent = MinimaxAlphaBetaAgent()
    m = Model()

    # O blocks X winning line
    m.move('X', 1)
    m.move('O', 5)
    m.move('X', 2)
    best_move, val = agent.choose(m, False)
    assert best_move == 3, f"Expected O to block at 3, got {best_move}"
    print("  -> Minimax blocking move: PASSED")

    # O takes winning move
    m2 = Model()
    m2.move('X', 1)
    m2.move('O', 4)
    m2.move('X', 2)
    m2.move('O', 5)
    m2.move('X', 8)
    best_move, val = agent.choose(m2, False)
    assert best_move == 6, f"Expected O to take winning move at 6, got {best_move}"
    print("  -> Minimax winning move: PASSED")

    # Verify AI never loses in all possible human moves
    def verify_no_ai_loss(state, is_x):
        if state.gameOver():
            assert state.score() <= 0, "AI lost to human!"
            return
        if is_x:
            for nxt in agent.get_all_next_moves(state):
                state.move('X', nxt)
                verify_no_ai_loss(state, False)
                state.undo_move('X', nxt)
        else:
            ai_move = agent.choose(state, False)[0]
            assert ai_move in agent.get_all_next_moves(state), f"AI picked invalid move {ai_move}"
            state.move('O', ai_move)
            verify_no_ai_loss(state, True)
            state.undo_move('O', ai_move)

    verify_no_ai_loss(Model(), True)
    print("  -> Full game tree verification (AI never loses): PASSED")

def test_gui_and_controller():
    print("Testing GUI and Controller resolution and buttons...")
    gui = GuiView()
    assert gui.width == 900
    assert gui.height == 700
    assert gui.display.get_size() == (900, 700)
    assert len(gui.positions) == 9

    # Verify all 9 positions are within window bounds
    for pos, pts in gui.positions.items():
        assert 0 <= pts[0][0] < pts[1][0] <= 900
        assert 0 <= pts[0][1] < pts[2][1] <= 700

    # Verify start menu buttons
    assert gui.btn_player_rect.collidepoint((450, 320))
    assert gui.btn_computer_rect.collidepoint((450, 420))

    # Verify end game buttons
    assert gui.btn_menu_rect.collidepoint((450, 340))
    assert gui.btn_exit_rect.collidepoint((450, 430))

    # Verify in-game buttons
    assert gui.game_btn_menu_rect.collidepoint((85, 45))
    assert gui.game_btn_restart_rect.collidepoint((815, 45))
    print("  -> GUI layout and hitboxes: PASSED")

    print("Testing Controller gameplay simulation...")
    model = Model()
    agent = MinimaxAlphaBetaAgent()
    ctrl = Controller(model, gui, agent)

    # Test "v/s Computer" simulation
    ctrl.ai = True
    # Simulate human clicking cell 5 (center: x=450, y=375)
    # Cell 5 is between x=375..525, y=300..450
    center_tile_5 = (450, 375)
    
    # Mock mouse position
    original_get_pos = gui.pygame.mouse.get_pos
    gui.pygame.mouse.get_pos = lambda: center_tile_5

    moved = ctrl.move_AI()
    assert moved, "Human move in AI mode should return True"
    assert model.board[1][1]["value"] == 1, "Cell 5 should have human X"

    # AI should have made its response move (an 'O')
    o_count = sum(1 for row in model.board for tile in row if tile["value"] == -1)
    assert o_count == 1, "Computer AI should have placed one 'O'"

    # Next human move at cell 2 (top-middle: x=450, y=225) since AI took cell 1
    gui.pygame.mouse.get_pos = lambda: (450, 225)
    moved = ctrl.move_AI()
    assert moved
    assert model.board[0][1]["value"] == 1, "Cell 2 should have human X"
    o_count = sum(1 for row in model.board for tile in row if tile["value"] == -1)
    assert o_count == 2, "Computer AI should have placed second 'O'"

    # Clicking occupied cell should return False
    gui.pygame.mouse.get_pos = lambda: (450, 375)
    moved = ctrl.move_AI()
    assert not moved, "Clicking occupied cell should not perform a move"

    # Test Player vs Player mode
    ctrl_pvp = Controller(Model(), gui, agent)
    ctrl_pvp.ai = False
    gui.pygame.mouse.get_pos = lambda: (300, 225) # Cell 1
    assert ctrl_pvp.move()
    ctrl_pvp.player = not ctrl_pvp.player
    assert ctrl_pvp.model.board[0][0]["value"] == 1 # X

    gui.pygame.mouse.get_pos = lambda: (450, 375) # Cell 5
    assert ctrl_pvp.move()
    ctrl_pvp.player = not ctrl_pvp.player
    assert ctrl_pvp.model.board[1][1]["value"] == -1 # O
    print("  -> Controller PvP and PvC simulation: PASSED")

    # Restore mouse get_pos
    gui.pygame.mouse.get_pos = original_get_pos

    # Test End-Game scenarios and Winner Detection
    print("Testing End-Game detection and winner states...")

    # 1. Human Win scenario in move_AI (ensure no crash with move -1!)
    ctrl_hwin = Controller(Model(), gui, agent)
    ctrl_hwin.ai = True
    ctrl_hwin.model.move('X', 1)
    ctrl_hwin.model.move('O', 4)
    ctrl_hwin.model.move('X', 2)
    ctrl_hwin.model.move('O', 5)
    # Human plays winning move at 3
    gui.pygame.mouse.get_pos = lambda: (600, 225) # Cell 3
    moved = ctrl_hwin.move_AI()
    assert moved
    assert ctrl_hwin.model.gameOver()
    assert ctrl_hwin.model.score() == 10
    print("  -> Human Win in AI mode handled cleanly (no crash): PASSED")

    # 2. Computer Win scenario
    ctrl_cwin = Controller(Model(), gui, agent)
    ctrl_cwin.ai = True
    ctrl_cwin.model.move('O', 4)
    ctrl_cwin.model.move('X', 1)
    ctrl_cwin.model.move('O', 5)
    ctrl_cwin.model.move('X', 2)
    # Human plays at 9, AI should take 6 to win!
    gui.pygame.mouse.get_pos = lambda: (600, 525) # Cell 9
    moved = ctrl_cwin.move_AI()
    assert moved
    assert ctrl_cwin.model.gameOver()
    assert ctrl_cwin.model.score() == -10
    print("  -> Computer Win detected correctly: PASSED")

    # 3. Draw scenario
    ctrl_draw = Controller(Model(), gui, agent)
    ctrl_draw.ai = True
    # Fill up to 8 moves without win
    moves = [('X', 1), ('O', 2), ('X', 3), ('O', 5), ('X', 4), ('O', 6), ('X', 8), ('O', 7)]
    for p, pos in moves:
        ctrl_draw.model.move(p, pos)
    # Final move by human at cell 9 (bottom-right: 600, 525)
    gui.pygame.mouse.get_pos = lambda: (600, 525)
    moved = ctrl_draw.move_AI()
    assert moved
    assert ctrl_draw.model.gameOver()
    assert ctrl_draw.model.score() == 0
    print("  -> Draw detected correctly: PASSED")

    # 4. Test In-Game Menu and Restart navigation
    assert gui.game_btn_menu_rect.collidepoint((85, 45))
    assert gui.game_btn_restart_rect.collidepoint((815, 45))
    print("  -> In-Game Navigation (Menu, Restart): PASSED")

    gui.pygame.mouse.get_pos = original_get_pos
    print("All automated tests completed successfully!")

if __name__ == '__main__':
    test_model()
    test_minimax()
    test_gui_and_controller()
