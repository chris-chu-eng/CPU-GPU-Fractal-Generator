class AppState:
    """A centralized class to manage the application's state."""

    def __init__(self, width: int, height: int, quality: int):
        self.width = width
        self.height = height
        self.quality = quality
