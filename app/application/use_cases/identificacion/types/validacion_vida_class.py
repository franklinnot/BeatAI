from app.application.use_cases.identificacion.types.validacion_class import (
    ValidacionBase,
)


class ValidacionVida(ValidacionBase):
    def __init__(self, success: bool, duration: float | None = None) -> None:
        super().__init__(success, duration)
