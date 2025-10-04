class ValidacionBase:
    def __init__(self, success: bool, duration: float | None = None) -> None:
        self.success = success
        self.duration = duration


class ValidacionIdentidad(ValidacionBase):
    def __init__(
        self,
        success: bool,
        duration: float | None = None,
        user_id: int | None = None,
        pr_embedding: bool = False,
        pr_landmarks: bool = False,
        b64: str | None = None,
    ) -> None:
        super().__init__(success, duration)
        self.user_id = user_id
        self.pr_embedding = pr_embedding
        self.pr_landmarks = pr_landmarks
        self.b64 = b64


class ValidacionVida(ValidacionBase):
    def __init__(self, success: bool, duration: float | None = None) -> None:
        super().__init__(success, duration)
