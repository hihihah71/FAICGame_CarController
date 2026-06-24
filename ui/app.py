from __future__ import annotations

import customtkinter as ctk

from core.config_manager import ConfigManager
from ui.home_frame import HomeFrame
from ui.racing_frame import RacingFrame
from ui.settings_frame import SettingsFrame
from ui.theme import COLORS


class FAICGameControllerApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("FAIC Game Controller")
        self.geometry("1240x760")
        self.minsize(1040, 640)
        self.configure(fg_color=COLORS["bg"])

        self.config_manager = ConfigManager()
        self.config_data = self.config_manager.ensure_exists()
        self.current_frame: ctk.CTkFrame | None = None

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_home()

    def show_home(self) -> None:
        self._swap_frame(HomeFrame(self, self))

    def show_racing(self) -> None:
        self.config_data = self.config_manager.load()
        self._swap_frame(RacingFrame(self, self, self.config_data))

    def show_settings(self) -> None:
        self.config_data = self.config_manager.load()
        self._swap_frame(SettingsFrame(self, self, self.config_manager, self.config_data))

    def _swap_frame(self, frame: ctk.CTkFrame) -> None:
        if self.current_frame and hasattr(self.current_frame, "cleanup"):
            self.current_frame.cleanup()
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def on_close(self) -> None:
        if self.current_frame and hasattr(self.current_frame, "cleanup"):
            self.current_frame.cleanup()
        self.destroy()


def run_app() -> None:
    app = FAICGameControllerApp()
    app.mainloop()
