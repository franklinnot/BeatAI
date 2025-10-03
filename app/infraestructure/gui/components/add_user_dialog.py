import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, YES, LEFT, W
from ttkbootstrap.dialogs import Messagebox


class AddUserDialog(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(master=parent, title="Añadir Nuevo Usuario")
        self.geometry("450x300")
        self.result = None  # Almacenará una tupla: (datos_usuario, capturar_muestras)
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        # Campos del formulario
        ttk.Label(frame, text="DNI:").grid(row=0, column=0, padx=5, pady=10, sticky=W)
        self.dni_entry = ttk.Entry(frame, width=30)
        self.dni_entry.grid(row=0, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Nombre Completo:").grid(
            row=1, column=0, padx=5, pady=10, sticky=W
        )
        self.nombre_entry = ttk.Entry(frame, width=30)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, padx=5, pady=10, sticky=W)
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=10)

        # Checkbox para mostrar vista previa
        self.show_preview_var = ttk.BooleanVar(value=False)
        preview_check = ttk.Checkbutton(
            frame,
            text="Mostrar vista previa de la cámara durante la captura",
            variable=self.show_preview_var,
            bootstyle="primary",
        )
        # preview_check.grid(row=3, column=0, columnspan=2, pady=10, sticky=W)

        # Botones de acción
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        btn_save_only = ttk.Button(
            button_frame,
            text="Guardar Usuario",
            command=self.on_save_only,
            bootstyle="secondary",
        )
        btn_save_only.pack(side=LEFT, padx=10)

        btn_save_capture = ttk.Button(
            button_frame,
            text="Guardar y Capturar",
            command=self.on_save_and_capture,
            bootstyle="success",
        )
        btn_save_capture.pack(side=LEFT, padx=10)

        btn_cancel = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.destroy,
            bootstyle="light-outline",
        )
        btn_cancel.pack(side=LEFT, padx=10)

        self.dni_entry.focus_set()

    def _get_form_data(self):
        dni = self.dni_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()

        if not all([dni, nombre, email]):
            Messagebox.show_warning(
                "Todos los campos son obligatorios.", "Datos incompletos", parent=self
            )
            return None

        return {
            "dni": dni,
            "nombre": nombre,
            "email": email,
            "show_preview": self.show_preview_var.get(),
        }

    def on_save_only(self):
        data = self._get_form_data()
        if data:
            self.result = (data, False)  # (datos, False para no capturar)
            self.destroy()

    def on_save_and_capture(self):
        data = self._get_form_data()
        if data:
            self.result = (data, True)  # (datos, True para capturar)
            self.destroy()
