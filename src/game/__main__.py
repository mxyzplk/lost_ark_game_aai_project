import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.tkinter_gui import GameGUI

def main():
    gui = GameGUI()
    gui.run()

if __name__ == "__main__":
    main()