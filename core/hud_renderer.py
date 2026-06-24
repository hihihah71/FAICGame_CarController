from __future__ import annotations

import cv2
import mediapipe as mp


TECH_CYAN = (255, 230, 60)
TECH_GREEN = (80, 255, 120)
TECH_ORANGE = (0, 140, 255)
TECH_RED = (40, 60, 255)
TECH_WHITE = (245, 245, 245)
TECH_DARK = (20, 22, 35)


class HudRenderer:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.drawer = mp.solutions.drawing_utils
        self.styles = mp.solutions.drawing_styles
        self.hands = mp.solutions.hands

    def render(self, frame, tracking_result, decision, fps: float):
        height, width, _ = frame.shape
        racing = self.config["racing"]
        show_landmarks = bool(self.config["hud"].get("show_landmarks", True))
        show_fps = bool(self.config["hud"].get("show_fps", True))

        if show_landmarks and tracking_result.landmarks:
            for hand_landmarks in tracking_result.landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    hand_landmarks,
                    tracking_result.connections,
                    self.styles.get_default_hand_landmarks_style(),
                    self.styles.get_default_hand_connections_style(),
                )

        boost_bottom = int(height * float(racing["boost_zone_ratio"]))
        drift_top = int(height * float(racing["drift_zone_ratio"]))
        self._draw_zone(frame, 0, boost_bottom, "BOOST ZONE", TECH_GREEN, decision.action == "BOOST")
        self._draw_zone(frame, drift_top, height, "DRIFT ZONE", TECH_RED, decision.action.startswith("DRIFT"))

        if decision.left_wrist and decision.right_wrist:
            cv2.line(frame, decision.left_wrist, decision.right_wrist, TECH_CYAN, 3, cv2.LINE_AA)
            self._draw_wrist(frame, decision.left_wrist, "L")
            self._draw_wrist(frame, decision.right_wrist, "R")
            self._draw_wheel(frame, decision.angle_deg)

        if decision.hands_detected < 2:
            cv2.putText(frame, "Show both hands to start", (20, height // 2), cv2.FONT_HERSHEY_DUPLEX, 0.8, TECH_ORANGE, 2, cv2.LINE_AA)

        lines = [
            f"Action: {decision.action}",
            f"Angle: {decision.angle_deg: .1f}",
            f"Hands: {decision.hands_detected}/2",
        ]
        if show_fps:
            lines.append(f"FPS: {fps: .1f}")
        self._draw_panel(frame, lines)
        self._draw_keycaps(frame, decision.pressed_keys)
        return frame

    def _draw_zone(self, frame, top: int, bottom: int, label: str, color, active: bool) -> None:
        overlay = frame.copy()
        alpha = 0.25 if active else 0.12
        cv2.rectangle(overlay, (0, top), (frame.shape[1], bottom), color, -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        cv2.rectangle(frame, (8, top + 8), (frame.shape[1] - 8, bottom - 8), color, 2, cv2.LINE_AA)
        cv2.putText(frame, label, (18, top + 34), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2, cv2.LINE_AA)

    def _draw_wrist(self, frame, point: tuple[int, int], label: str) -> None:
        cv2.circle(frame, point, 13, TECH_CYAN, 2, cv2.LINE_AA)
        cv2.circle(frame, point, 5, TECH_WHITE, -1, cv2.LINE_AA)
        cv2.putText(frame, label, (point[0] + 12, point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TECH_WHITE, 1, cv2.LINE_AA)

    def _draw_wheel(self, frame, angle_deg: float) -> None:
        import math

        height, width, _ = frame.shape
        center = (width // 2, int(height * 0.60))
        radius = min(width, height) // 5
        cv2.circle(frame, center, radius, TECH_WHITE, 2, cv2.LINE_AA)
        for offset in (0, 180):
            angle = math.radians(angle_deg + offset)
            end = (int(center[0] + radius * 0.8 * math.cos(angle)), int(center[1] + radius * 0.8 * math.sin(angle)))
            cv2.line(frame, center, end, TECH_CYAN, 4, cv2.LINE_AA)
        cv2.circle(frame, center, radius // 4, TECH_DARK, -1, cv2.LINE_AA)
        cv2.circle(frame, center, radius // 4, TECH_CYAN, 2, cv2.LINE_AA)

    def _draw_panel(self, frame, lines: list[str]) -> None:
        overlay = frame.copy()
        x, y, width = 14, 14, 250
        height = 34 + 26 * len(lines)
        cv2.rectangle(overlay, (x, y), (x + width, y + height), TECH_DARK, -1)
        cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)
        cv2.rectangle(frame, (x, y), (x + width, y + height), TECH_CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, "FAIC TECHFEST", (x + 12, y + 25), cv2.FONT_HERSHEY_DUPLEX, 0.6, TECH_WHITE, 1, cv2.LINE_AA)
        for index, line in enumerate(lines):
            cv2.putText(frame, line, (x + 12, y + 55 + index * 24), cv2.FONT_HERSHEY_SIMPLEX, 0.55, TECH_CYAN, 1, cv2.LINE_AA)

    def _draw_keycaps(self, frame, pressed_keys: set[str]) -> None:
        height, width, _ = frame.shape
        specs = [
            ("W", "w", 42),
            ("A", "a", 42),
            ("S", "s", 42),
            ("D", "d", 42),
            ("SPACE", "space", 86),
        ]
        gap = 8
        total_width = sum(item[2] for item in specs) + gap * (len(specs) - 1)
        x = max(14, width // 2 - total_width // 2)
        y = height - 44

        overlay = frame.copy()
        cv2.rectangle(overlay, (x - 12, y - 10), (x + total_width + 12, y + 38), TECH_DARK, -1)
        cv2.addWeighted(overlay, 0.60, frame, 0.40, 0, frame)

        for label, key, key_width in specs:
            active = key in pressed_keys
            fill = TECH_CYAN if active else (42, 48, 58)
            border = TECH_WHITE if active else (110, 120, 130)
            text = TECH_DARK if active else TECH_WHITE
            cv2.rectangle(frame, (x, y), (x + key_width, y + 30), fill, -1, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + key_width, y + 30), border, 2, cv2.LINE_AA)
            text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            tx = x + (key_width - text_size[0]) // 2
            ty = y + 20
            cv2.putText(frame, label, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.45, text, 1, cv2.LINE_AA)
            x += key_width + gap
