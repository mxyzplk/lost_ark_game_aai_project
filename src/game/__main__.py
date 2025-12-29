import sys
import os

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.tkinter_gui import GameGUI

def main():
    # Cria e executa a interface gráfica
    gui = GameGUI()
    gui.run()

if __name__ == "__main__":
    main()