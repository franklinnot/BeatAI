class ValidacionBase:
    def __init__(self, success: bool, duration: float | None = None) -> None:
        self.success = success
        self.duration = duration