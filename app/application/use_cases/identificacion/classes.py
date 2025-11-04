class ValidacionBase:

    def __init__(
        self,
        success: bool,
        duration: float | None = None,
        b64: str | None = None,
    ) -> None:
        self.success = success
        self.duration = duration
        self.b64 = b64


class ValidacionIdentidad(ValidacionBase):

    def __init__(
        self,
        success: bool,
        duration: float | None = None,
        b64: str | None = None,
        user_id: int | None = None,
        pr_embedding: bool = False,
        pr_landmarks: bool = False,
    ) -> None:
        super().__init__(success, duration, b64)
        self.user_id = user_id
        self.pr_embedding = pr_embedding
        self.pr_landmarks = pr_landmarks


class ValidacionVida(ValidacionBase):

    def __init__(
        self,
        success: bool,
        duration: float | None = None,
        b64: str | None = None,
    ) -> None:
        super().__init__(success, duration, b64)
