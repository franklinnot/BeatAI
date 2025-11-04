import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app.domain.dbconfig import get_session
from app.domain.repositories.bitacora_repository import bitacora_repository
from app.domain.repositories.usuario_repository import usuario_repository


class BitacoraView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)

        self.create_widgets()
        self.load_logs()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=BOTH, expand=YES)

        # --- Tabla de Bitácora ---
        table_frame = ttk.Labelframe(
            main_frame, text="Registros de la Bitácora", padding=10
        )
        table_frame.pack(fill=BOTH, expand=YES, pady=5)

        cols = [
            "DNI",
            "Usuario",
            "Pr. Vida",
            "Pr. Identificación",
            "Fecha",
        ]
        self.log_tree = ttk.Treeview(
            table_frame, columns=cols, show="headings", bootstyle="info"
        )
        for col in cols:
            self.log_tree.heading(col, text=col)
            self.log_tree.column(col, width=120, anchor=CENTER)
        self.log_tree.pack(side=LEFT, fill=BOTH, expand=YES)

        scrollbar = ttk.Scrollbar(
            table_frame, orient=VERTICAL, command=self.log_tree.yview
        )
        self.log_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # --- Botón de Refrescar ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=10)

        btn_refresh = ttk.Button(
            button_frame,
            text="🔄 Refrescar",
            command=self.load_logs,
            bootstyle="primary-outline",
        )
        btn_refresh.pack(side=RIGHT, padx=5)

    def load_logs(self):
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)

        with get_session() as db:
            logs = bitacora_repository.get_all(db, limit=1000)
            for log in logs:
                id_usuario = log.usuario_id

                dni = "-"
                nombre = "-"

                if id_usuario:
                    usuario = usuario_repository.get_by_id(db, id_usuario)
                    if usuario:
                        dni = usuario.dni
                        nombre = usuario.nombre

                self.log_tree.insert(
                    "",
                    END,
                    values=(
                        dni,
                        nombre,
                        "✅" if log.pr_vida else "❌",
                        "✅" if log.pr_embeddings or log.pr_landmarks else "❌",
                        log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )
