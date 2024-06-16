import cv2
import time

def check_webcam_fps():
    cap = cv2.VideoCapture(0)  # Mở webcam (0 là chỉ số của webcam mặc định)
    if not cap.isOpened():
        print("Error opening webcam")
        return

    num_frames = 120  # Số lượng khung hình để tính FPS
    print("Capturing {0} frames".format(num_frames))

    start = time.time()

    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print("Error capturing frame")
            break

    end = time.time()

    # Tính toán FPS
    seconds = end - start
    fps = num_frames / seconds

    print("Time taken : {0} seconds".format(seconds))
    print("Estimated frames per second : {0}".format(fps))

    cap.release()
    cv2.destroyAllWindows()

check_webcam_fps()
