# BeatAI

# Crear entorno virtual con anaconda
conda create --prefix ./.venv python=3.10 -y

# Activar el entorno virtual
conda activate ./.venv

# Comandos para instalar dependencias:
- dlib y opencv
conda install -c conda-forge dlib opencv -y

- mediapipe con face-recognition
pip install mediapipe face-recognition

- SQLAlchemy
pip install SQLAlchemy

# Guardar dependencias de pip
pip freeze > requirements.txt

# Como instalar dlib
https://www.geeksforgeeks.org/python/how-to-install-dlib-library-for-python-in-windows-10/