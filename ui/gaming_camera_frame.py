from __future__ import annotations

import customtkinter as ctk

from ui.theme import COLORS, font


class GamingCameraFrame(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color="#050914", corner_radius=14)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top = self._make_canvas(height=44)
        self.left = self._make_canvas(width=42)
        self.right = self._make_canvas(width=42)
        self.bottom = self._make_canvas(height=70)

        self.top.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.left.grid(row=1, column=0, sticky="ns")
        self.right.grid(row=1, column=2, sticky="ns")
        self.bottom.grid(row=2, column=0, columnspan=3, sticky="ew")

        self.preview_label = ctk.CTkLabel(
            self,
            text="Camera preview\nPress Start",
            text_color=COLORS["muted"],
            fg_color="#070b12",
            corner_radius=4,
            font=font(18, "bold"),
        )
        self.preview_label.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)

        self.top.bind("<Configure>", lambda _event: self._draw_top())
        self.left.bind("<Configure>", lambda _event: self._draw_side(self.left, "left"))
        self.right.bind("<Configure>", lambda _event: self._draw_side(self.right, "right"))
        self.bottom.bind("<Configure>", lambda _event: self._draw_bottom())

    def set_preview(self, image, text: str = "") -> None:
        self.preview_label.configure(image=image, text=text)

    def clear_preview(self, text: str) -> None:
        self.preview_label.configure(image=None, text=text)

    def _make_canvas(self, width: int | None = None, height: int | None = None) -> ctk.CTkCanvas:
        options = {"highlightthickness": 0, "bd": 0, "bg": "#050914"}
        if width is not None:
            options["width"] = width
        if height is not None:
            options["height"] = height
        return ctk.CTkCanvas(self, **options)

    def _draw_top(self) -> None:
        canvas = self.top
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 140:
            return

        red = "#ef233c"
        black = "#050505"
        graphite = "#1b2230"
        metal = "#2a3445"
        cyan = "#38bdf8"
        y = h - 9
        cut = 36

        canvas.create_polygon(0, 0, 72, 0, 58, 13, 18, 13, 18, h, 0, h, fill=black, outline=metal)
        canvas.create_polygon(w, 0, w - 72, 0, w - 58, 13, w - 18, 13, w - 18, h, w, h, fill=black, outline=metal)
        canvas.create_line(cut, y, w - cut, y, fill=black, width=12, capstyle="round")
        canvas.create_line(cut, y, w - cut, y, fill=red, width=3, capstyle="round")
        canvas.create_line(7, h, cut, y, fill=black, width=12, capstyle="round")
        canvas.create_line(w - 7, h, w - cut, y, fill=black, width=12, capstyle="round")
        canvas.create_line(20, 15, 57, 15, fill=red, width=4, capstyle="round")
        canvas.create_line(w - 57, 15, w - 20, 15, fill=red, width=4, capstyle="round")

        for x in (78, w // 2 - 72, w // 2 + 28, w - 128):
            canvas.create_polygon(x, y - 11, x + 52, y - 11, x + 42, y - 2, x + 8, y - 2, fill=graphite, outline=red)
            canvas.create_line(x + 12, y - 7, x + 39, y - 7, fill="#ff4558", width=1)
        canvas.create_line(w // 2 - 92, y - 18, w // 2 + 92, y - 18, fill=metal, width=2)
        canvas.create_line(w // 2 - 62, y - 18, w // 2 + 62, y - 18, fill=cyan, width=1)

        for x in (28, w - 28):
            canvas.create_oval(x - 4, 5, x + 4, 13, fill="#0b1018", outline=metal)
            canvas.create_oval(x - 2, 7, x + 2, 11, fill=red, outline="")

    def _draw_side(self, canvas: ctk.CTkCanvas, side: str) -> None:
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if h < 120:
            return

        red = "#ef233c"
        black = "#050505"
        graphite = "#151b26"
        metal = "#2a3445"
        x = w - 9 if side == "left" else 9
        accent_x = x - 9 if side == "left" else x + 9
        outer_x = 5 if side == "left" else w - 5

        canvas.create_line(x, 0, x, h, fill=black, width=12, capstyle="round")
        canvas.create_line(x, 12, x, h - 12, fill=red, width=2)
        canvas.create_line(outer_x, 18, outer_x, h - 18, fill=metal, width=1)
        for y in (34, h // 2 - 46, h - 118):
            canvas.create_polygon(
                min(x, accent_x) - 4, y,
                max(x, accent_x) + 4, y + 8,
                max(x, accent_x) + 4, y + 54,
                min(x, accent_x) - 4, y + 62,
                fill=graphite,
                outline=red,
                width=1,
            )
            canvas.create_line(accent_x, y + 12, accent_x, y + 48, fill=red, width=3, capstyle="round")
            canvas.create_line(outer_x, y + 17, outer_x, y + 42, fill="#38bdf8", width=1)

        for y in (14, h - 22):
            canvas.create_oval(outer_x - 4, y - 4, outer_x + 4, y + 4, fill="#0b1018", outline=metal)

    def _draw_bottom(self) -> None:
        canvas = self.bottom
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 180:
            return

        red = "#ef233c"
        black = "#050505"
        graphite = "#1b2230"
        metal = "#2a3445"
        cyan = "#38bdf8"
        y = 9
        tab_w = min(240, max(150, w // 4))
        x0 = (w - tab_w) // 2
        x1 = x0 + tab_w

        canvas.create_polygon(0, 0, 18, 0, 18, h - 16, 58, h - 16, 72, h, 0, h, fill=black, outline=metal)
        canvas.create_polygon(w, 0, w - 18, 0, w - 18, h - 16, w - 58, h - 16, w - 72, h, w, h, fill=black, outline=metal)
        canvas.create_line(34, y, x0 - 28, y, fill=black, width=12, capstyle="round")
        canvas.create_line(x1 + 28, y, w - 34, y, fill=black, width=12, capstyle="round")
        canvas.create_line(30, y, x0 - 24, y, fill=red, width=3, capstyle="round")
        canvas.create_line(x1 + 24, y, w - 30, y, fill=red, width=3, capstyle="round")
        canvas.create_line(18, h - 18, 54, h - 18, fill=red, width=4, capstyle="round")
        canvas.create_line(w - 54, h - 18, w - 18, h - 18, fill=red, width=4, capstyle="round")

        plate = [
            x0 - 26, y,
            x0 + 12, h - 10,
            x1 - 12, h - 10,
            x1 + 26, y,
        ]
        canvas.create_polygon(*plate, fill=black, outline=metal, width=3)
        canvas.create_polygon(x0 + 12, h - 31, x1 - 12, h - 31, x1 - 28, h - 18, x0 + 28, h - 18, fill=graphite, outline="#101827")
        canvas.create_line(x0 + 30, h - 14, x1 - 30, h - 14, fill=red, width=3)
        canvas.create_line(x0 + 56, h - 23, x1 - 56, h - 23, fill=cyan, width=1)

        for x in (62, w - 122):
            canvas.create_polygon(x, y - 5, x + 62, y - 5, x + 51, y + 6, x + 9, y + 6, fill=graphite, outline=red)
            canvas.create_line(x + 16, y, x + 46, y, fill="#ff4558", width=1)

        for x in (28, w - 28):
            canvas.create_oval(x - 4, h - 31, x + 4, h - 23, fill="#0b1018", outline=metal)
