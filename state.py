from dataclasses import dataclass
from typing import Optional


@dataclass
class AppState:
    """A centralized class to manage the application's state."""

    width: int
    height: int
    quality: int
    cpu_render_time: Optional[float] = None
    gpu_render_time: Optional[float] = None
    show_ui: bool = True
