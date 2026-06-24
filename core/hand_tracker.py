from __future__ import annotations

from dataclasses import dataclass

import cv2
import mediapipe as mp


@dataclass
class HandTrackingResult:
    wrists: list[tuple[int, int]]
    landmarks: object | None
    connections: object | None


class HandTracker:
    def __init__(self, show_landmarks: bool = True) -> None:
        self.show_landmarks = show_landmarks
        self.mp_hands = mp.solutions.hands
        self._hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=2,
        )

    def process(self, frame_bgr) -> HandTrackingResult:
        height, width, _ = frame_bgr.shape
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb)

        wrists: list[tuple[int, int]] = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                wrists.append((int(wrist.x * width), int(wrist.y * height)))

        return HandTrackingResult(
            wrists=wrists,
            landmarks=results.multi_hand_landmarks if self.show_landmarks else None,
            connections=self.mp_hands.HAND_CONNECTIONS,
        )

    def close(self) -> None:
        self._hands.close()
