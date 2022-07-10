import numpy as np
import cv2

frame = np.full((150, 150, 3), 255, dtype="uint8")
cv2.circle(frame, (75, 75), 60, [0, 0, 0], -1, cv2.LINE_AA)
cv2.circle(frame, (75, 75), 35, [255, 255, 255], -1, cv2.LINE_AA)
cv2.imwrite("o-image.png", frame)

frame = np.full((100, 100, 3), 255, dtype="uint8")
cv2.circle(frame, (50, 50), 40, [0, 0, 0], -1, cv2.LINE_AA)
cv2.circle(frame, (50, 50), 23, [255, 255, 255], -1, cv2.LINE_AA)
cv2.imwrite("o-image-small.png", frame)
