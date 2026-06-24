from __future__ import annotations

import time

import cv2

from core.config_manager import ConfigManager
from core.hand_tracker import HandTracker
from core.hud_renderer import HudRenderer
from core.input_manager import InputManager
from core.racing_logic import RacingLogic


def game() -> None:
    """Legacy OpenCV runner kept for compatibility with older scripts."""
    config = ConfigManager().ensure_exists()
    input_manager = InputManager(config["keys"])
    camera = config["camera"]
    cap = cv2.VideoCapture(int(camera["index"]))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(camera["width"]))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(camera["height"]))

    tracker = HandTracker(show_landmarks=bool(config["hud"].get("show_landmarks", True)))
    logic = RacingLogic(config["racing"], config["keys"])
    hud = HudRenderer(config)
    last_time = time.perf_counter()

    try:
        if not cap.isOpened():
            print(f"Cannot open camera index {camera['index']}")
            return

        while cap.isOpened():
            ok, frame = cap.read()
            if not ok:
                continue

            frame = cv2.flip(frame, 1)
            tracking = tracker.process(frame)
            height, width, _ = frame.shape
            decision = logic.decide(tracking.wrists, (width, height))
            input_manager.set_pressed_keys(decision.pressed_keys)

            now = time.perf_counter()
            fps = 1.0 / max(now - last_time, 0.001)
            last_time = now
            rendered = hud.render(frame, tracking, decision, fps)
            cv2.imshow("FAIC Game", rendered)
            cv2.setWindowProperty("FAIC Game", cv2.WND_PROP_TOPMOST, 1)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        input_manager.release_all()
        tracker.close()
        cap.release()
        cv2.destroyAllWindows()
