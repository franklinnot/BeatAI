import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, YES, END, CENTER, VERTICAL, RIGHT, LEFT, Y, X
from ttkbootstrap.dialogs import Messagebox
from app.domain.dbconfig import get_session
from app.domain.repositories.usuario_repository import usuario_repository
from app.application.use_cases.register_user.register_complete import register_complete
from app.application.use_cases.register_user.register_operacion import (
    register_operacion,
)
from app.application.use_cases.register_user.register_user import register_user
from app.infraestructure.gui.components.add_user_dialog import AddUserDialog
from app.infraestructure.gui.components.edit_user_dialog import EditUserDialog

camera_lock = threading.Lock()


# --- Widget de Popup Personalizado ---
class ProcessingPopup(ttk.Toplevel):
    def __init__(self, parent, title="Procesando...", message="Por favor, espere."):
        super().__init__(master=parent)
        self.title(title)
        self.geometry("300x100")

        parent.update_idletasks()
        x = (
            parent.winfo_x() + (parent.winfo_width() // 2) - (150)
        )  # 150 es la mitad del ancho del popup
        y = (
            parent.winfo_y() + (parent.winfo_height() // 2) - (50)
        )  # 50 es la mitad de la altura
        self.geometry(f"+{x}+{y}")

        self.label = ttk.Label(self, text=message, padding=(20, 10))
        self.label.pack(expand=YES, fill=BOTH)
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        self.update()


class UserView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)
        self.create_widgets()
        self.load_users()

    # create_widgets se mantiene igual
    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=BOTH, expand=YES)

        user_table_frame = ttk.Labelframe(
            main_frame, text="Usuarios Registrados", padding=10
        )
        user_table_frame.pack(fill=BOTH, expand=YES, pady=5)

        cols = ["ID", "DNI", "Nombre", "Email", "Estado", "Creado en"]
        self.user_tree = ttk.Treeview(
            user_table_frame, columns=cols, show="headings", bootstyle="primary"
        )
        for col in cols:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=120, anchor=CENTER)
        self.user_tree.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(
            user_table_frame, orient=VERTICAL, command=self.user_tree.yview
        )
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=10)

        btn_add = ttk.Button(
            button_frame,
            text="👤 Añadir Usuario",
            command=self.add_user,
            bootstyle="success",
        )
        btn_add.pack(side=LEFT, padx=5, expand=True)

        btn_edit = ttk.Button(
            button_frame,
            text="✏️ Editar Usuario",
            command=self.edit_user,
            bootstyle="info",
        )
        btn_edit.pack(side=LEFT, padx=5, expand=True)

        btn_delete = ttk.Button(
            button_frame,
            text="🗑️ Eliminar Usuario",
            command=self.delete_user,
            bootstyle="danger",
        )
        btn_delete.pack(side=LEFT, padx=5, expand=True)

        btn_disable = ttk.Button(
            button_frame,
            text="🚫 Deshabilitar Usuario",
            command=self.disable_user,
            bootstyle="warning",
        )
        btn_disable.pack(side=LEFT, padx=5, expand=True)

        btn_add_op = ttk.Button(
            button_frame,
            text="📸 Registrar Operación",
            command=self.add_operation,
            bootstyle="secondary",
        )
        btn_add_op.pack(side=LEFT, padx=5, expand=True)

        btn_refresh = ttk.Button(
            button_frame,
            text="🔄 Refrescar",
            command=self.load_users,
            bootstyle="primary-outline",
        )
        btn_refresh.pack(side=LEFT, padx=5, expand=True)

    def load_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        with get_session() as db:
            usuarios = usuario_repository.get_all(db, limit=1000)
            for user in usuarios:
                self.user_tree.insert(
                    "",
                    END,
                    values=(
                        user.id,
                        user.dni,
                        user.nombre,
                        user.email,
                        user.estado.value,
                        user.created_at.strftime("%Y-%m-%d %H:%M"),
                    ),
                )

    def add_user(self):
        dialog = AddUserDialog(self.winfo_toplevel())
        dialog.wait_window()

        if dialog.result:
            user_data, capture_samples = dialog.result

            if capture_samples:
                popup = ProcessingPopup(
                    self.winfo_toplevel(),
                    message="Capturando muestras...\nMire a la cámara.",
                )
                thread = threading.Thread(
                    target=self._execute_full_registration, args=(user_data, popup)
                )
                thread.start()
            else:
                self._execute_user_only_registration(user_data)

    # --- NUEVOS MÉTODOS PARA MANEJAR RESPUESTAS DE HILOS ---
    def _on_registration_complete(self, result, popup):
        """Esta función SÍ se ejecuta en el hilo principal de la GUI."""
        if popup.winfo_exists():
            popup.destroy()

        if result:
            self.load_users()
            Messagebox.ok("Usuario y muestras registrados con éxito.", "Éxito")
        else:
            Messagebox.show_error(
                "No se pudo registrar al usuario. Verifique la consola.", "Error"
            )

    def _on_operation_complete(self, result, popup):
        """Esta función SÍ se ejecuta en el hilo principal de la GUI."""
        if popup.winfo_exists():
            popup.destroy()

        if result and result.total_muestras > 0:
            Messagebox.ok(
                f"Nueva operación registrada con {result.total_muestras} muestras.",
                "Éxito",
            )
        else:
            Messagebox.show_error("No se pudo registrar la operación.", "Error")

    def _on_error(self, error, popup):
        """Maneja errores inesperados desde un hilo."""
        if popup.winfo_exists():
            popup.destroy()
        Messagebox.show_error(f"Ocurrió un error inesperado: {error}", "Error Crítico")

    # --- MÉTODOS DE HILO MODIFICADOS ---
    def _execute_full_registration(self, user_data, popup):
        """Esta función se ejecuta en un hilo separado."""
        try:
            with get_session() as db:
                result = register_complete(db, **user_data)
            # Pide al hilo principal que ejecute la función de finalización
            self.after(0, self._on_registration_complete, result, popup)
        except Exception as e:
            # Pide al hilo principal que muestre el error
            self.after(0, self._on_error, e, popup)

    def _execute_user_only_registration(self, user_data):
        # Este no usa hilo, así que puede modificar la GUI directamente
        try:
            with get_session() as db:
                user_info = {k: v for k, v in user_data.items() if k != "show_preview"}
                new_user = register_user(db, **user_info)

            if new_user:
                self.load_users()
                Messagebox.ok("Usuario registrado con éxito (sin muestras).", "Éxito")
            else:
                Messagebox.show_error(
                    "El usuario no pudo ser registrado.", "Error de Registro"
                )
        except Exception as e:
            Messagebox.show_error(f"Ocurrió un error: {e}", "Error")


    def edit_user(self):
        if not self.user_tree.selection():
            Messagebox.show_warning(
                "Por favor, seleccione un usuario para editar.", "Selección requerida"
            )
            return

        selected_item = self.user_tree.selection()[0]
        values = self.user_tree.item(selected_item, "values")
        user_id = int(values[0])
        current_dni, current_nombre, current_email = values[1], values[2], values[3]

        dialog = EditUserDialog(
            self.winfo_toplevel(),
            {"dni": current_dni, "nombre": current_nombre, "email": current_email},
        )
        dialog.wait_window()

        if dialog.result:
            try:
                with get_session() as db:
                    user = usuario_repository.get_by_id(db, user_id)
                    if not user:
                        Messagebox.show_error("Usuario no encontrado.", "Error")
                        return

                    # Validar que no haya conflictos
                    if (
                        usuario_repository.get_by_dni(db, dialog.result["dni"])
                        and user.dni != dialog.result["dni"]
                    ):
                        Messagebox.show_error("Ya existe un usuario con ese DNI.", "Error")
                        return
                    if (
                        usuario_repository.get_by_email(db, dialog.result["email"])
                        and user.email != dialog.result["email"]
                    ):
                        Messagebox.show_error(
                            "Ya existe un usuario con ese email.", "Error"
                        )
                        return

                    updated = usuario_repository.update(db, user, dialog.result)
                    if updated:
                        Messagebox.ok("Usuario actualizado con éxito.", "Éxito")
                        self.load_users()
                    else:
                        Messagebox.show_error("No se pudo actualizar el usuario.", "Error")
            except Exception as e:
                Messagebox.show_error(f"Error al editar: {e}", "Error")

    def disable_user(self):
        if not self.user_tree.selection():
            Messagebox.show_warning(
                "Por favor, seleccione un usuario.", "Selección requerida"
            )
            return

        selected_item = self.user_tree.selection()[0]
        user_id = int(self.user_tree.item(selected_item, "values")[0])
        user_name = self.user_tree.item(selected_item, "values")[2]

        confirm = Messagebox.yesno(
            f"¿Deshabilitar al usuario '{user_name}'?\n(Esta acción no elimina datos, solo los oculta.)",
            "Deshabilitar Usuario",
        )

        if confirm == "Yes":
            try:
                with get_session() as db:
                    usuario_repository.disable(db, id=user_id)
                Messagebox.ok("Usuario deshabilitado correctamente.", "Éxito")
                self.load_users()
            except Exception as e:
                Messagebox.show_error(f"No se pudo deshabilitar: {e}", "Error")

    def delete_user(self):
        if not self.user_tree.selection():
            return Messagebox.show_warning(
                "Por favor, seleccione un usuario.", "Selección requerida"
            )

        selected_item = self.user_tree.selection()[0]
        user_id = self.user_tree.item(selected_item, "values")[0]
        user_name = self.user_tree.item(selected_item, "values")[2]
        confirm = Messagebox.yesno(f"¿Eliminar al usuario '{user_name}'?", "Confirmar")

        if confirm == "Yes":
            try:
                with get_session() as db:
                    usuario_repository.delete(db, id=int(user_id))
                Messagebox.ok("Usuario eliminado.", "Éxito")
                self.load_users()
            except Exception as e:
                Messagebox.show_error(f"No se pudo eliminar: {e}", "Error")

    def add_operation(self):
        if not self.user_tree.selection():
            return Messagebox.show_warning(
                "Por favor, seleccione un usuario.", "Selección requerida"
            )

        selected_item = self.user_tree.selection()[0]
        user_id = int(self.user_tree.item(selected_item, "values")[0])
        user_name = self.user_tree.item(selected_item, "values")[2]

        if (
            Messagebox.yesno(f"Iniciar captura para '{user_name}'?", "Nueva Operación")
            == "Yes"
        ):
            popup = ProcessingPopup(
                self.winfo_toplevel(), message="Iniciando captura...\nMire a la cámara."
            )
            thread = threading.Thread(
                target=self._execute_add_operation, args=(user_id, popup)
            )
            thread.start()

    # def _execute_add_operation(self, user_id, popup):
    #     """Esta función se ejecuta en un hilo separado."""
    #     try:
    #         with get_session() as db:
    #             result = register_operacion(db, usuario_id=user_id, show_preview=False)
    #         # Pide al hilo principal que ejecute la función de finalización
    #         self.after(0, self._on_operation_complete, result, popup)
    #     except Exception as e:
    #         # Pide al hilo principal que muestre el error
    #         self.after(0, self._on_error, e, popup)

    def _execute_add_operation(self, user_id, popup):
        try:
            with camera_lock:
                with get_session() as db:
                    result = register_operacion(
                        db, usuario_id=user_id, show_preview=False
                    )
                self.after(0, self._on_operation_complete, result, popup)
        except Exception as e:
            self.after(0, self._on_error, e, popup)
