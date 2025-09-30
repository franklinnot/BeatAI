from app.application.use_cases.identificacion.types.validacion_class import (
    ValidacionBase,
)


class ValidacionIdentidad(ValidacionBase):
    def __init__(
        self,
        success: bool,
        duration: float | None = None,
        user_id: int | None = None,
        pr_embedding: bool = False,
        pr_landmarks: bool = False,
    ) -> None:
        super().__init__(success, duration)
        self.user_id = user_id
        self.pr_embedding = pr_embedding
        self.pr_landmarks = pr_landmarks
