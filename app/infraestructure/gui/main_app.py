import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.infraestructure.gui.views.user_view import UserView
from app.infraestructure.gui.views.bitacora_view import BitacoraView


class App(ttk.Window):
    def __init__(self):
        super().__init__(
            themename="litera",
            title="BeatAI - Panel de Administración",
            size=(1000, 600),
        )
        self.place_window_center()

        # Crear el contenedor de pestañas (Notebook)
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Crear las pestañas individuales
        user_frame = UserView(notebook)
        bitacora_frame = BitacoraView(notebook)

        # Añadir las pestañas al Notebook
        notebook.add(user_frame, text="Gestión de Usuarios")
        notebook.add(bitacora_frame, text="Bitácora de Operaciones")
