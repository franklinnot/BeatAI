import sys
import os
from app.infraestructure.gui.main_app import App

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    app = App()
    app.mainloop()
