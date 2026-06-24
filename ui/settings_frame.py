from __future__ import annotations

import copy
from tkinter import messagebox

import customtkinter as ctk

from core.config_manager import DEFAULT_CONFIG, ConfigManager
from ui.theme import BezelFrame, COLORS, button_style, font, mono


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, app, config_manager: ConfigManager, config: dict) -> None:
        super().__init__(master, fg_color=COLORS["bg"])
        self.app = app
        self.config_manager = config_manager
        self.config = copy.deepcopy(config)
        self.entries: dict[str, ctk.CTkEntry] = {}
        self.switches: dict[str, ctk.CTkSwitch] = {}

        panel = BezelFrame(self, width=680, height=620)
        panel.place(relx=0.5, rely=0.5, anchor="center")
        panel.pack_propagate(False)
        panel_body = panel.inner

        header = ctk.CTkFrame(panel_body, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 12))
        title_group = ctk.CTkFrame(header, fg_color="transparent")
        title_group.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(title_group, text="Settings", text_color=COLORS["text"], font=font(31, "bold"), anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_group, text="camera and gesture tuning", text_color=COLORS["muted"], font=mono(12), anchor="w").pack(anchor="w", pady=(2, 0))
        ctk.CTkButton(header, text="Back to Home", width=132, height=38, font=font(13, "bold"), command=app.show_home, **button_style("secondary")).pack(side="right")

        form = ctk.CTkScrollableFrame(panel_body, fg_color="transparent", scrollbar_button_color=COLORS["border"], scrollbar_button_hover_color=COLORS["cyan_dark"])
        form.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        self._entry(form, "Camera index", "camera.index")
        self._entry(form, "Camera width", "camera.width")
        self._entry(form, "Camera height", "camera.height")
        self._entry(form, "Steering threshold", "racing.steer_threshold")
        self._entry(form, "Drift steering threshold", "racing.drift_steer_threshold")
        self._entry(form, "Boost zone ratio", "racing.boost_zone_ratio")
        self._entry(form, "Drift zone ratio", "racing.drift_zone_ratio")
        self._switch(form, "Show landmarks", "hud.show_landmarks")
        self._switch(form, "Show FPS", "hud.show_fps")

        buttons = ctk.CTkFrame(panel_body, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(10, 20))
        ctk.CTkButton(buttons, text="Save", height=42, font=font(14, "bold"), command=self.save, **button_style("primary")).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ctk.CTkButton(buttons, text="Reset default", height=42, font=font(14, "bold"), command=self.reset_default, **button_style("secondary")).pack(side="left", expand=True, fill="x", padx=8)
        ctk.CTkButton(buttons, text="Back to Home", height=42, font=font(14, "bold"), command=app.show_home, **button_style("secondary")).pack(side="left", expand=True, fill="x", padx=(8, 0))

    def _entry(self, parent, label: str, path: str) -> None:
        row = ctk.CTkFrame(parent, fg_color=COLORS["panel_alt"], border_width=1, border_color=COLORS["border_soft"], corner_radius=10)
        row.pack(fill="x", pady=5)
        ctk.CTkLabel(row, text=label, width=230, anchor="w", text_color=COLORS["muted"], font=font(13, "bold")).pack(side="left", padx=(14, 6), pady=8)
        entry = ctk.CTkEntry(row, fg_color=COLORS["panel_inner"], border_color=COLORS["border"], text_color=COLORS["text"], font=mono(13))
        entry.insert(0, str(self._get_path(path)))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=8)
        self.entries[path] = entry

    def _switch(self, parent, label: str, path: str) -> None:
        switch = ctk.CTkSwitch(
            parent,
            text=label,
            text_color=COLORS["text"],
            font=font(13, "bold"),
            fg_color=COLORS["panel_alt"],
            progress_color=COLORS["cyan_dark"],
            button_color=COLORS["text"],
            button_hover_color=COLORS["cyan"],
        )
        if bool(self._get_path(path)):
            switch.select()
        switch.pack(anchor="w", pady=8, padx=6)
        self.switches[path] = switch

    def save(self) -> None:
        try:
            for path, entry in self.entries.items():
                old_value = self._get_path(path)
                raw = entry.get().strip()
                if isinstance(old_value, int):
                    value = int(raw)
                elif isinstance(old_value, float):
                    value = float(raw)
                else:
                    value = raw
                self._set_path(path, value)

            for path, switch in self.switches.items():
                self._set_path(path, bool(switch.get()))

            self.config_manager.save(self.config)
            messagebox.showinfo("Settings saved", "Config saved to config.json. Restart camera to apply camera changes.")
        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc))

    def reset_default(self) -> None:
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        self.config_manager.save(self.config)
        self.app.show_settings()

    def _get_path(self, path: str):
        data = self.config
        for part in path.split("."):
            data = data[part]
        return data

    def _set_path(self, path: str, value) -> None:
        data = self.config
        parts = path.split(".")
        for part in parts[:-1]:
            data = data[part]
        data[parts[-1]] = value
