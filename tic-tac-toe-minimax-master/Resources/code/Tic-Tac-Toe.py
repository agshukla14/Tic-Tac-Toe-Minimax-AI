from gui import GuiView
from model import Model
from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
from controller import Controller

def main():
	gui = GuiView()
	model = Model()
	agent = MinimaxAlphaBetaAgent()
	controller = Controller(model, gui, agent)
	controller.run_intro()

if __name__ == '__main__':
	main()
