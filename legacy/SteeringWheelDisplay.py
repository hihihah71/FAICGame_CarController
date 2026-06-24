import cv2
import numpy as np
import math

class SteeringWheelDisplay:
    def __init__(self, center=(100, 100), radius=50):
        self.center = center
        self.radius = radius
        self.alpha = 0.6  # độ trong suốt

    def draw(self, frame, angle_deg):
        """
        Vẽ vô lăng lên frame tại vị trí self.center.
        angle_deg: góc xoay vô lăng (-90 -> 90)
        """
        overlay = frame.copy()
        color = (220, 220, 220)
        thickness = 3

        # Vẽ vòng tròn vô lăng
        cv2.circle(overlay, self.center, self.radius, color, thickness)

        # Hai thanh tay nắm
        for i in range(2):
            angle_rad = math.radians(angle_deg + i * 180)
            x = int(self.center[0] + self.radius * 0.8 * math.cos(angle_rad))
            y = int(self.center[1] + self.radius * 0.8 * math.sin(angle_rad))
            cv2.line(overlay, self.center, (x, y), (0, 255, 255), 4)

        # Nút trung tâm vô lăng
        cv2.circle(overlay, self.center, int(self.radius * 0.3), (255, 255, 255), -1)

        # Pha trộn với frame chính
        frame = cv2.addWeighted(overlay, self.alpha, frame, 1 - self.alpha, 0)

        # text_pos = (self.center[0] - 40, self.center[1] + self.radius + 20)
        # cv2.putText(frame, text_pos,
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        return frame
