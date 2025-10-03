import ttkbootstrap as ttk
from ttkbootstrap.constants import W, BOTH, YES
from ttkbootstrap.dialogs import Messagebox


class EditUserDialog(ttk.Toplevel):
    def __init__(self, parent, user_data):
        super().__init__(master=parent, title="Editar Usuario")
        self.geometry("450x250")
        self.result = None
        self.user_data = user_data
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=BOTH, expand=YES)

        ttk.Label(frame, text="DNI:").grid(row=0, column=0, padx=5, pady=10, sticky=W)
        self.dni_entry = ttk.Entry(frame, width=30)
        self.dni_entry.insert(0, self.user_data["dni"])
        self.dni_entry.grid(row=0, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Nombre Completo:").grid(
            row=1, column=0, padx=5, pady=10, sticky=W
        )
        self.nombre_entry = ttk.Entry(frame, width=30)
        self.nombre_entry.insert(0, self.user_data["nombre"])
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=10)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, padx=5, pady=10, sticky=W)
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.insert(0, self.user_data["email"])
        self.email_entry.grid(row=2, column=1, padx=5, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        btn_save = ttk.Button(
            button_frame,
            text="Guardar Cambios",
            command=self.on_save,
            bootstyle="primary",
        )
        btn_save.pack(side="left", padx=10)

        btn_cancel = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.destroy,
            bootstyle="light-outline",
        )
        btn_cancel.pack(side="left", padx=10)

    def _validate(self):
        dni = self.dni_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        email = self.email_entry.get().strip()

        if not all([dni, nombre, email]):
            Messagebox.show_warning("Todos los campos son obligatorios.", parent=self)
            return None
        return {"dni": dni, "nombre": nombre, "email": email}

    def on_save(self):
        data = self._validate()
        if data:
            self.result = data
            self.destroy()
