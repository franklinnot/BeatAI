from dataclasses import dataclass


@dataclass
class OperacionResultado:
    id: int
    total_muestras: int
    duracion: float