import sys
import os

from app.infraestructure.esp32.listen import listen

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    listen()
