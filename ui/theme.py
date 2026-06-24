from __future__ import annotations

import customtkinter as ctk


COLORS = {
    "bg": "#080d16",
    "bg_soft": "#0d1422",
    "panel_outer": "#121b2b",
    "panel_inner": "#0b1220",
    "panel_alt": "#101827",
    "border": "#26364f",
    "border_soft": "#1b2a40",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "subtle": "#64748b",
    "cyan": "#38bdf8",
    "cyan_dark": "#0369a1",
    "amber": "#f59e0b",
    "rose": "#e11d48",
    "green": "#10b981",
}

FONT_FAMILY = "Segoe UI Variable"
MONO_FAMILY = "Cascadia Mono"


def font(size: int, weight: str = "normal", family: str = FONT_FAMILY) -> ctk.CTkFont:
    return ctk.CTkFont(family=family, size=size, weight=weight)


def mono(size: int, weight: str = "normal") -> ctk.CTkFont:
    return font(size, weight, MONO_FAMILY)


def button_style(kind: str = "primary") -> dict:
    styles = {
        "primary": {
            "fg_color": COLORS["cyan_dark"],
            "hover_color": "#075985",
            "text_color": COLORS["text"],
            "border_width": 1,
            "border_color": "#2a83a8",
            "corner_radius": 9,
        },
        "secondary": {
            "fg_color": COLORS["panel_alt"],
            "hover_color": "#172136",
            "text_color": COLORS["text"],
            "border_width": 1,
            "border_color": COLORS["border"],
            "corner_radius": 9,
        },
        "danger": {
            "fg_color": "#991b1b",
            "hover_color": "#7f1d1d",
            "text_color": COLORS["text"],
            "border_width": 1,
            "border_color": "#9f2f3a",
            "corner_radius": 9,
        },
    }
    return styles[kind]


class BezelFrame(ctk.CTkFrame):
    def __init__(self, master, *, width: int | None = None, height: int | None = None, **kwargs) -> None:
        size_options = {}
        if width is not None:
            size_options["width"] = width
        if height is not None:
            size_options["height"] = height

        super().__init__(
            master,
            fg_color=COLORS["panel_outer"],
            border_width=1,
            border_color=COLORS["border"],
            corner_radius=18,
            **size_options,
            **kwargs,
        )
        self.inner = ctk.CTkFrame(
            self,
            fg_color=COLORS["panel_inner"],
            border_width=1,
            border_color=COLORS["border_soft"],
            corner_radius=14,
        )
        self.inner.pack(fill="both", expand=True, padx=7, pady=7)
