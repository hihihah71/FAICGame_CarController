from __future__ import annotations

from queue import Empty, Queue

import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

from core.camera_worker import CameraStatus, CameraWorker
from core.input_manager import InputManager
from ui.gaming_camera_frame import GamingCameraFrame
from ui.theme import BezelFrame, COLORS, button_style, font, mono


class RacingFrame(ctk.CTkFrame):
    def __init__(self, master, app, config: dict) -> None:
        super().__init__(master, fg_color=COLORS["bg"])
        self.app = app
        self.config = config
        self.frame_queue: Queue[tuple[object, CameraStatus]] = Queue(maxsize=2)
        self.status = CameraStatus()
        self.input_manager = InputManager(config["keys"])
        self.worker = CameraWorker(config, self.input_manager, self._on_worker_frame, self._on_worker_status)
        self.preview_image = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        preview_shell = BezelFrame(self)
        preview_shell.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        preview_shell.inner.grid_columnconfigure(0, weight=1)
        preview_shell.inner.grid_rowconfigure(1, weight=1)

        preview_header = ctk.CTkFrame(preview_shell.inner, fg_color="transparent")
        preview_header.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 10))
        ctk.CTkLabel(preview_header, text="Live camera", text_color=COLORS["text"], font=font(18, "bold")).pack(side="left")
        self.preview_badge = ctk.CTkLabel(preview_header, text="IDLE", width=86, height=28, fg_color=COLORS["panel_alt"], text_color=COLORS["muted"], corner_radius=7, font=mono(12, "bold"))
        self.preview_badge.pack(side="right")

        self.camera_frame = GamingCameraFrame(preview_shell.inner)
        self.camera_frame.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
        self.preview_label = self.camera_frame.preview_label

        panel = BezelFrame(self, width=360)
        panel.grid(row=0, column=1, sticky="ns", padx=(10, 18), pady=18)
        panel.grid_propagate(False)
        panel.pack_propagate(False)
        panel_body = panel.inner

        ctk.CTkLabel(panel_body, text="Racing Controller", text_color=COLORS["text"], font=font(25, "bold")).pack(pady=(22, 5))
        ctk.CTkLabel(panel_body, text="gesture input telemetry", text_color=COLORS["muted"], font=mono(12)).pack(pady=(0, 16))

        self.status_card = ctk.CTkFrame(panel_body, fg_color=COLORS["panel_alt"], border_width=1, border_color=COLORS["border_soft"], corner_radius=12)
        self.status_card.pack(fill="x", padx=18, pady=(0, 14))
        self.status_label = ctk.CTkLabel(
            self.status_card,
            text="",
            width=292,
            wraplength=292,
            justify="left",
            anchor="w",
            text_color=COLORS["text"],
            font=mono(13),
        )
        self.status_label.pack(fill="x", padx=14, pady=14)

        ctk.CTkButton(panel_body, text="Start", height=42, font=font(14, "bold"), command=self.start, **button_style("primary")).pack(fill="x", padx=18, pady=(8, 7))
        ctk.CTkButton(panel_body, text="Pause / Resume", height=42, font=font(14, "bold"), command=self.pause_resume, **button_style("secondary")).pack(fill="x", padx=18, pady=7)
        ctk.CTkButton(panel_body, text="Stop", height=42, font=font(14, "bold"), command=self.stop, **button_style("secondary")).pack(fill="x", padx=18, pady=7)
        ctk.CTkButton(panel_body, text="Emergency Stop", height=42, font=font(14, "bold"), command=self.emergency_stop, **button_style("danger")).pack(fill="x", padx=18, pady=(7, 18))
        ctk.CTkButton(panel_body, text="Back to Home", height=42, font=font(14, "bold"), command=app.show_home, **button_style("secondary")).pack(fill="x", padx=18, pady=7)

        self.error_label = ctk.CTkLabel(panel_body, text="", text_color=COLORS["amber"], wraplength=296, font=font(13))
        self.error_label.pack(fill="x", padx=18, pady=(18, 0))

        self._update_status_label()
        self.after(30, self._poll_frame_queue)

    def start(self) -> None:
        if self.worker.is_paused():
            self.worker.resume()
        else:
            self.worker.start()

    def pause_resume(self) -> None:
        if self.worker.is_paused():
            self.worker.resume()
        else:
            self.worker.pause()

    def stop(self) -> None:
        self.worker.stop()
        self.camera_frame.clear_preview("Camera preview\nPress Start")
        self.preview_badge.configure(text="IDLE", text_color=COLORS["muted"], fg_color=COLORS["panel_alt"])
        self.preview_image = None

    def emergency_stop(self) -> None:
        self.worker.emergency_stop()

    def cleanup(self) -> None:
        self.worker.stop()

    def _on_worker_frame(self, frame, status: CameraStatus) -> None:
        try:
            if self.frame_queue.full():
                self.frame_queue.get_nowait()
            self.frame_queue.put_nowait((frame, status))
        except Exception:
            pass

    def _on_worker_status(self, status: CameraStatus) -> None:
        self.status = status

    def _poll_frame_queue(self) -> None:
        try:
            while True:
                frame, status = self.frame_queue.get_nowait()
                self.status = status
                self._show_frame(frame)
        except Empty:
            pass

        self._update_status_label()
        self.after(30, self._poll_frame_queue)

    def _show_frame(self, frame) -> None:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        max_w = max(self.preview_label.winfo_width() - 20, 400)
        max_h = max(self.preview_label.winfo_height() - 20, 300)
        image.thumbnail((max_w, max_h), Image.LANCZOS)
        self.preview_image = ImageTk.PhotoImage(image)
        self.camera_frame.set_preview(self.preview_image, "")

    def _update_status_label(self) -> None:
        keys = " ".join(self._format_key(key) for key in sorted(self.status.pressed_keys)) or "-"
        running = "YES" if self.status.running else "NO"
        paused = "YES" if self.status.paused else "NO"
        action = self.status.action.replace("_", " ")
        badge_color = COLORS["green"] if self.status.running and not self.status.paused else COLORS["amber"] if self.status.paused else COLORS["panel_alt"]
        badge_text = "PAUSED" if self.status.paused else "LIVE" if self.status.running else "IDLE"
        text = (
            f"RUN       {running}\n"
            f"PAUSE     {paused}\n"
            f"HANDS     {self.status.hands_detected}/2\n"
            f"ACTION    {action}\n"
            f"KEYS      {keys}\n"
            f"ANGLE     {self.status.angle_deg: .1f}\n"
            f"FPS       {self.status.fps: .1f}\n"
            f"CAM       {self.status.camera_index}\n"
            f"RES       {self.status.width}x{self.status.height}"
        )
        self.status_label.configure(text=text)
        self.preview_badge.configure(text=badge_text, fg_color=badge_color, text_color=COLORS["bg"] if self.status.running or self.status.paused else COLORS["muted"])
        self.error_label.configure(text=self.status.error)

    def _format_key(self, key: str) -> str:
        return "Space" if key == "space" else key.upper()
