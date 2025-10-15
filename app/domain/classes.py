from dataclasses import dataclass


@dataclass
class OperacionResultado:
    id: int
    total_muestras: int
    duracion: float


@dataclass
class BitacoraTemporal:
    id: int
    pr_vida: bool
    duracion_total: float
    duracion_spoofing: float
    created_at: str = ""
