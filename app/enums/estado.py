from enum import Enum


class Estado(str, Enum):
    """
    Define los estados posibles para los registros en la base de datos.
    """

    HABILITADO = "Habilitado"
    DESHABILITADO = "Deshabilitado"
