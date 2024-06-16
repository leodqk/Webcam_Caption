import cv2
import os
import time
import testing_caption_generator

def extract_key_frames_from_webcam(output_folder, num_frames=5, interval_seconds=10):
    cap = cv2.VideoCapture(0)  # Mở webcam (0 là chỉ số của webcam mặc định)
    if not cap.isOpened():
        print("Error opening webcam")
        return

    frame_count = 0
    frames = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Mỗi interval_seconds giây lưu một khung hình
        if frame_count % (interval_seconds * int(cap.get(cv2.CAP_PROP_FPS))) == 0:
            frames.append(frame)
            output_path = f"{output_folder}/frame_{len(frames)-1}.jpg"
            testing_caption_generator.caption_image(output_path)
            # cv2.imwrite(output_path, frame)
            # print(f"Saved {output_path}")

        frame_count += 1

        # Hiển thị video đang quay và chờ nhấn 'q' để thoát
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
output_folder = 'result'
extract_key_frames_from_webcam(output_folder)
