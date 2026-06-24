from __future__ import annotations

from dataclasses import dataclass, field
import math


@dataclass(frozen=True)
class RacingDecision:
    action: str = "IDLE"
    angle_deg: float = 0.0
    pressed_keys: set[str] = field(default_factory=set)
    hands_detected: int = 0
    left_wrist: tuple[int, int] | None = None
    right_wrist: tuple[int, int] | None = None


class RacingLogic:
    def __init__(self, racing_config: dict, key_config: dict) -> None:
        self.racing_config = racing_config
        self.key_config = key_config

    def decide(self, wrists: list[tuple[int, int]], frame_size: tuple[int, int]) -> RacingDecision:
        hands_detected = len(wrists)
        if hands_detected != 2:
            return RacingDecision(hands_detected=hands_detected)

        width, height = frame_size
        left_wrist, right_wrist = sorted(wrists, key=lambda point: point[0])
        dx = right_wrist[0] - left_wrist[0]
        dy = right_wrist[1] - left_wrist[1]
        angle_deg = math.degrees(math.atan2(dy, dx))

        boost_line = height * float(self.racing_config["boost_zone_ratio"])
        drift_line = height * float(self.racing_config["drift_zone_ratio"])
        steer_threshold = float(self.racing_config["steer_threshold"])
        drift_threshold = float(self.racing_config["drift_steer_threshold"])

        if left_wrist[1] < boost_line and right_wrist[1] < boost_line:
            base_action = "BOOST"
            desired_keys = {self.key_config["boost"]}
            threshold = steer_threshold
        elif left_wrist[1] > drift_line and right_wrist[1] > drift_line:
            base_action = "DRIFT"
            desired_keys = {self.key_config["drift"]}
            threshold = drift_threshold
        else:
            base_action = "GO"
            desired_keys = {self.key_config["forward"]}
            threshold = steer_threshold

        action = base_action
        if angle_deg < -threshold:
            desired_keys.add(self.key_config["left"])
            action = "DRIFT_LEFT" if base_action == "DRIFT" else "LEFT"
        elif angle_deg > threshold:
            desired_keys.add(self.key_config["right"])
            action = "DRIFT_RIGHT" if base_action == "DRIFT" else "RIGHT"

        return RacingDecision(
            action=action,
            angle_deg=angle_deg,
            pressed_keys=desired_keys,
            hands_detected=hands_detected,
            left_wrist=left_wrist,
            right_wrist=right_wrist,
        )
