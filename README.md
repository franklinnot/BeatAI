TODO PARA WINDOWS

# Crear entorno virtual con anaconda
conda create --prefix ./.venv python=3.10

# Activar el entorno virtual
cond activate ./.venv

# Comandos para instalar dependencias:
- dlib
conda install -c conda-forge dlib
- face-recognition
pip install face-recognition
- mediapipe
pip install mediapipe
- opencv para capturar imagenes de la camara y procesarlas
pip install opencv-python
- pandas, para guardar datos estructurados en csv o migrar a una bd
pip install pandas

pip install --upgrade numpy==1.26.4
conda install -c conda-forge zlib
conda install -c conda-forge -y zlib-wapi


# Como instalar dlib
https://www.geeksforgeeks.org/python/how-to-install-dlib-library-for-python-in-windows-10/


__init___.py
bitacora.py
database.py
face_detector.py
face_features.py
liveness.py
usuario.py