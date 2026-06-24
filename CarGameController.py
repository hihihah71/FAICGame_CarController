# import math
# import keyinput
# import cv2
# import mediapipe as mp
# import os
# # from imutils.video import VideoStream


# # game_path = r"C:\Program Files (x86)\GameTop.com\Off-road Super Racing\game-shell.exe"


# def game():
#     # os.startfile(game_path)
#     mp_drawing = mp.solutions.drawing_utils
#     mp_drawing_styles = mp.solutions.drawing_styles
#     mp_hands = mp.solutions.hands

#     font = cv2.FONT_HERSHEY_SIMPLEX
#     # 0 For webcam input:
#     cap = cv2.VideoCapture(0)
#     # cap = VideoStream(src=0).start()

#     with mp_hands.Hands(
#             model_complexity=0,
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5) as hands:
#         while cap.isOpened():
#             success, image = cap.read()

#             if not success:
#                 print("Ignoring empty camera frame.")
#                 # If loading a video, use 'break' instead of 'continue'.
#                 continue

#             # To improve performance, optionally mark the image as not writeable to
#             image.flags.writeable = False
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             image = cv2.resize(image, (520, 420))
#             results = hands.process(image)
#             imageHeight, imageWidth, _ = image.shape

#             # Draw the hand annotations on the image.
#             image.flags.writeable = True
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#             co = []
#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     mp_drawing.draw_landmarks(
#                         image,
#                         hand_landmarks,
#                         mp_hands.HAND_CONNECTIONS,
#                         mp_drawing_styles.get_default_hand_landmarks_style(),
#                         mp_drawing_styles.get_default_hand_connections_style())
#                     for point in mp_hands.HandLandmark:
#                         if str(point) == "HandLandmark.WRIST":
#                             normalizedLandmark = hand_landmarks.landmark[point]
#                             pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
#                                                                                                    normalizedLandmark.y,
#                                                                                                    imageWidth,
#                                                                                                    imageHeight)
#                             try:
#                                 co.append(list(pixelCoordinatesLandmark))
#                             except:
#                                 continue

#             if len(co) == 2:
#                 xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
#                 radius = 150
#                 try:
#                     m = (co[1][1] - co[0][1]) / (co[1][0] - co[0][0])
#                 except:
#                     continue
#                 a = 1 + m ** 2
#                 b = -2 * xm - 2 * co[0][0] * (m ** 2) + 2 * m * co[0][1] - 2 * m * ym
#                 c = xm ** 2 + (m ** 2) * (co[0][0] ** 2) + co[0][1] ** 2 + ym ** 2 - 2 * co[0][1] * ym - 2 * co[0][1] * \
#                     co[0][
#                         0] * m + 2 * m * ym * co[0][0] - 22500
#                 xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
#                 xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
#                 ya = m * (xa - co[0][0]) + co[0][1]
#                 yb = m * (xb - co[0][0]) + co[0][1]
#                 if m != 0:
#                     ap = 1 + ((-1 / m) ** 2)
#                     bp = -2 * xm - 2 * xm * ((-1 / m) ** 2) + 2 * (-1 / m) * ym - 2 * (-1 / m) * ym
#                     cp = xm ** 2 + ((-1 / m) ** 2) * (xm ** 2) + ym ** 2 + ym ** 2 - 2 * ym * ym - 2 * ym * xm * (
#                             -1 / m) + 2 * (-1 / m) * ym * xm - 22500
#                     try:
#                         xap = (-bp + (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
#                         xbp = (-bp - (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
#                         yap = (-1 / m) * (xap - xm) + ym
#                         ybp = (-1 / m) * (xbp - xm) + ym

#                     except:
#                         continue

#                 cv2.circle(img=image, center=(int(xm), int(ym)), radius=radius, color=(195, 255, 62), thickness=15)

#                 l = (int(math.sqrt((co[0][0] - co[1][0]) ** 2 * (co[0][1] - co[1][1]) ** 2)) - 150) // 2
#                 cv2.line(image, (int(xa), int(ya)), (int(xb), int(yb)), (195, 255, 62), 20)

#                 # Drift
#                 drift = False
#                 # Both hands are at the top of the frame
#                 vertical_top_threshold = int(imageHeight / 2)
#                 if co[0][1] < vertical_top_threshold and co[1][1] < vertical_top_threshold:
#                     print("Nitro.")
#                     keyinput.press_key('space')
#                 else:
#                     keyinput.release_key('space')

#                 #Nitro
#                 #Both hands are at the bottom of the frame
#                 vertical_threshold = int(2 * imageHeight / 3)
#                 if co[0][1] > vertical_threshold and co[1][1] > vertical_threshold:
#                     print("Drift")
#                     drift = True
#                     keyinput.release_key('space')
#                     keyinput.press_key('s')
                    
                


#                 if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 85:  ### 65 -------- 65 changed
#                     print("Turn left.")
#                     if drift == False:
#                         keyinput.release_key('s')
#                     keyinput.release_key('d')
#                     keyinput.press_key('a')

#                     cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)


#                 elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 85:  ### 65 -------- 65
#                     print("Turn left.")
#                     if drift == False:
#                         keyinput.release_key('s')
#                     keyinput.release_key('d')
#                     keyinput.press_key('a')

#                     cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)


#                 elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 85:  ### 65 -------- 65
#                     print("Turn right.")
#                     if drift == False:
#                         keyinput.release_key('s')
#                     keyinput.release_key('a')
#                     keyinput.press_key('d')

#                     cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

#                 elif co[1][0] > co[0][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 85:  ### 65 -------- 65
#                     print("Turn right.")
#                     if drift == False:
#                         keyinput.release_key('s')
#                     keyinput.release_key('a')
#                     keyinput.press_key('d')

#                     cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

#                 else:
#                     if drift == False:
#                         print("keeping straight")
#                         keyinput.release_key('s')
#                         keyinput.release_key('a')
#                         keyinput.release_key('d')
#                         keyinput.press_key('w')

#                     drift = False
#                     if ybp > yap:
#                         cv2.line(image, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)
#                     else:
#                         cv2.line(image, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

#             # if len(co) == 1:
#             #     print("keeping back")
#             #     keyinput.release_key('a')
#             #     keyinput.release_key('d')
#             #     keyinput.release_key('space')
#             #     keyinput.press_key('s')


#             elif len(co) == 0:
#                 keyinput.release_key('a')
#                 keyinput.release_key('d')
#                 keyinput.release_key('space')
#                 keyinput.release_key('s')


#             cv2.imshow("FAIC Game", cv2.flip(image, 1))
#             # cv2.moveWindow("Detector", 0, imageHeight + 200)
#             cv2.setWindowProperty("FAIC Game", cv2.WND_PROP_TOPMOST, 1)

#             # Flip the image horizontally for a selfie-view display.
#             if cv2.waitKey(5) & 0xFF == ord('q'):
#                 break
#     cap.release()


import math
import keyinput
import cv2
import mediapipe as mp
from SteeringWheelDisplay import SteeringWheelDisplay

# Kích thước khung hình
FRAME_W = 640
FRAME_H = 480

def game():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    # Bộ hiển thị vô lăng
    wheel_display = SteeringWheelDisplay(center=(FRAME_W // 2, FRAME_H // 2), radius=130)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=2
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            h, w, _ = image.shape

            wrists = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    nx = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                    ny = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                    px, py = int(nx * w), int(ny * h)
                    wrists.append((px, py))
                    cv2.circle(image, (px, py), 8, (255, 200, 0), -1)

            #Khi nhận biết được hai tay trên màn hình, chương trình bắt đầu
            if len(wrists) == 2:
                # Lấy hai cổ tay
                wrists = sorted(wrists, key=lambda p: p[0])
                left_wrist, right_wrist = wrists[0], wrists[1]

                dx = right_wrist[0] - left_wrist[0]
                dy = right_wrist[1] - left_wrist[1]
                angle_deg = math.degrees(math.atan2(dy, dx))

                # Vẽ vô lăng lớn ở giữa màn hình
                image = wheel_display.draw(image, angle_deg)

                
                BOOST_THRESHOLD = h * 0.25
                DRIFT_THRESHOLD = h * 0.70
                ACTION = ''
                #Boost (hai tay trên cao)
                if left_wrist[1] < BOOST_THRESHOLD and right_wrist[1] < BOOST_THRESHOLD:
                    ACTION = 'BOOST'
                    # keyinput.press_key('space'),
                    # keyinput.release_key('s')
                    # cv2.putText(image, "BOOST!", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                # Drift (hai tay thấp)
                elif left_wrist[1] > DRIFT_THRESHOLD and right_wrist[1] > DRIFT_THRESHOLD:
                    ACTION = 'DRIFT'
                    # keyinput.press_key('s')
                    # cv2.putText(image, "DRIFT", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                else:
                    ACTION = 'GO'
                    keyinput.release_key('s')
                    
                if ACTION == 'BOOST':
                    keyinput.press_key('space')
                    keyinput.release_key('w')
                    if angle_deg < -15:
                        keyinput.press_key('a')
                        keyinput.release_key('d')
                    elif angle_deg > 15:
                        keyinput.press_key('d')
                        keyinput.release_key('a')
                    else:
                        keyinput.release_key('a')
                        keyinput.release_key('d')
                elif ACTION == 'DRIFT':
                    keyinput.press_key('s')
                    if angle_deg < -5:
                        keyinput.press_key('a')
                        keyinput.release_key('d')
                    elif angle_deg > 5:
                        keyinput.press_key('d')
                        keyinput.release_key('a')
                    else:
                        keyinput.release_key('a')
                        keyinput.release_key('d')
                elif ACTION == 'GO':
                    keyinput.press_key('w')
                    if angle_deg < -15:
                        keyinput.press_key('a')
                        keyinput.release_key('d')
                    elif angle_deg > 15:
                        keyinput.press_key('d')
                        keyinput.release_key('a')
                    else:
                        keyinput.release_key('a')
                        keyinput.release_key('d')
                
                overlay = image.copy()
                #Tạo boost zone
                boost_color = (0, 255, 0) if ACTION == 'BOOST' else (0, 100, 0)
                cv2. rectangle (
                    overlay,
                    (0, 0),
                    (w, int(BOOST_THRESHOLD)),
                    boost_color,
                    -1
                )
                #Tạo drift zone
                drift_color = (0, 0, 255) if ACTION == 'DRIFT' else (0, 0, 255)
                cv2.rectangle (
                    overlay,
                    (0, int(DRIFT_THRESHOLD)),
                    (w, h),
                    drift_color,
                    -1
                )

                #Gì đó quên mất
                image = cv2.addWeighted(overlay, 0.2, image, 0.8, 0)
                
                #Vẽ khung
                cv2.rectangle(image, (0, 0), (w, int(BOOST_THRESHOLD)), (0, 255, 0), 3)
                cv2.rectangle(image, (0, int(DRIFT_THRESHOLD)), (w, h), (0, 0, 255), 3)
                
                #Chú thích vùng
                cv2.putText(
                    image,
                    'BOOST ZONE',
                    (10, int(BOOST_THRESHOLD)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                )
                cv2.putText(
                    image,
                    'DRIFT ZONE',
                    (10, int(DRIFT_THRESHOLD)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
                )
            
            #Khi hai tay biến mất khỏi màn hình, dừng toàn bộ hành động     
            else:
                keyinput.release_key('a')
                keyinput.release_key('d')
                keyinput.release_key('s')
                keyinput.release_key('space')

            cv2.imshow("FAIC Game", image)
            cv2.setWindowProperty("FAIC Game", cv2.WND_PROP_TOPMOST, 1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
