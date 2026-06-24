from __future__ import annotations

import customtkinter as ctk

from ui.theme import BezelFrame, COLORS, button_style, font, mono


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, app) -> None:
        super().__init__(master, fg_color=COLORS["bg"])
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        shell = BezelFrame(self, width=760, height=430)
        shell.grid(row=0, column=0, padx=42, pady=42)
        shell.pack_propagate(False)
        container = shell.inner

        eyebrow = ctk.CTkLabel(
            container,
            text="TECHFEST DEMO CONTROLLER",
            text_color=COLORS["cyan"],
            font=mono(12, "bold"),
        )
        eyebrow.pack(pady=(40, 12))
        title = ctk.CTkLabel(
            container,
            text="FAIC Game Controller",
            text_color=COLORS["text"],
            font=font(44, "bold"),
        )
        title.pack(pady=(0, 8))

        subtitle = ctk.CTkLabel(
            container,
            text="Webcam-based racing controller",
            text_color=COLORS["muted"],
            font=font(17),
        )
        subtitle.pack(pady=(0, 28))

        ctk.CTkButton(container, text="Racing Controller", width=280, height=48, font=font(15, "bold"), command=app.show_racing, **button_style("primary")).pack(pady=7)
        ctk.CTkButton(container, text="Settings", width=280, height=48, font=font(15, "bold"), command=app.show_settings, **button_style("secondary")).pack(pady=7)
        ctk.CTkButton(container, text="Exit", width=280, height=48, font=font(15, "bold"), command=app.on_close, **button_style("danger")).pack(pady=(22, 0))
