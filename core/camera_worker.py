from __future__ import annotations

from dataclasses import dataclass, field
import threading
import time
from typing import Callable

import cv2

from core.hand_tracker import HandTracker
from core.hud_renderer import HudRenderer
from core.input_manager import InputManager
from core.racing_logic import RacingDecision, RacingLogic


@dataclass
class CameraStatus:
    running: bool = False
    paused: bool = False
    error: str = ""
    action: str = "IDLE"
    hands_detected: int = 0
    angle_deg: float = 0.0
    fps: float = 0.0
    pressed_keys: set[str] = field(default_factory=set)
    camera_index: int = 0
    width: int = 640
    height: int = 480


class CameraWorker:
    def __init__(
        self,
        config: dict,
        input_manager: InputManager,
        on_frame: Callable[[object, CameraStatus], None],
        on_status: Callable[[CameraStatus], None],
    ) -> None:
        self.config = config
        self.input_manager = input_manager
        self.on_frame = on_frame
        self.on_status = on_status
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            self._pause_event.clear()
            return
        self._stop_event.clear()
        self._pause_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def pause(self) -> None:
        self._pause_event.set()
        self.input_manager.release_all()

    def resume(self) -> None:
        self._pause_event.clear()

    def stop(self) -> None:
        self._stop_event.set()
        self._pause_event.clear()
        self.input_manager.release_all()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._thread = None

    def emergency_stop(self) -> None:
        self.input_manager.release_all()

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def is_paused(self) -> bool:
        return self._pause_event.is_set()

    def _run(self) -> None:
        camera_config = self.config["camera"]
        camera_index = int(camera_config["index"])
        width = int(camera_config["width"])
        height = int(camera_config["height"])
        status = CameraStatus(True, False, "", camera_index=camera_index, width=width, height=height)
        cap = cv2.VideoCapture(camera_index)
        tracker: HandTracker | None = None

        try:
            if not cap.isOpened():
                status.error = f"Cannot open camera index {camera_index}"
                status.running = False
                self.on_status(status)
                return

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            tracker = HandTracker(show_landmarks=bool(self.config["hud"].get("show_landmarks", True)))
            logic = RacingLogic(self.config["racing"], self.config["keys"])
            hud = HudRenderer(self.config)
            last_time = time.perf_counter()

            while not self._stop_event.is_set():
                ok, frame = cap.read()
                if not ok:
                    status.error = "Cannot read frame from camera"
                    self.on_status(status)
                    time.sleep(0.2)
                    continue

                frame = cv2.flip(frame, 1)
                tracking = tracker.process(frame)
                frame_h, frame_w, _ = frame.shape
                decision = logic.decide(tracking.wrists, (frame_w, frame_h))
                now = time.perf_counter()
                fps = 1.0 / max(now - last_time, 0.001)
                last_time = now

                if self._pause_event.is_set():
                    self.input_manager.release_all()
                    decision = RacingDecision(hands_detected=len(tracking.wrists))
                    paused = True
                else:
                    self.input_manager.set_pressed_keys(decision.pressed_keys)
                    paused = False

                status = CameraStatus(
                    running=True,
                    paused=paused,
                    action="PAUSED" if paused else decision.action,
                    hands_detected=decision.hands_detected,
                    angle_deg=decision.angle_deg,
                    fps=fps,
                    pressed_keys=self.input_manager.get_pressed_keys(),
                    camera_index=camera_index,
                    width=frame_w,
                    height=frame_h,
                )
                rendered = hud.render(frame, tracking, decision, fps)
                self.on_frame(rendered, status)
        except Exception as exc:
            status.error = str(exc)
            status.running = False
            self.on_status(status)
        finally:
            self.input_manager.release_all()
            if tracker:
                tracker.close()
            cap.release()
            status.running = False
            status.paused = False
            status.pressed_keys = set()
            self.on_status(status)
