import cv2
import os
import time
import testing_caption_generator
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['192.168.88.246:9092'],  # Địa chỉ Kafka broker của bạn
    value_serializer=lambda v: v.encode('utf-8')  # Tuỳ chọn serializer cho chuỗi văn bản
)

def extract_key_frames_from_webcam(
    output_folder, interval_seconds=2, caption_display_duration=5
):
    cap = cv2.VideoCapture(0)  # Mở webcam (0 là chỉ số của webcam mặc định)
    if not cap.isOpened():
        print("Error opening webcam")
        return

    frame_count = 0
    frames = []
    current_caption = ""
    caption_frames_remaining = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: FPS is 0")
        cap.release()
        cv2.destroyAllWindows()
        return

    interval_frames = int(interval_seconds * fps)
    caption_display_frames = int(caption_display_duration * fps)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Mỗi interval_seconds giây lưu một khung hình
        if frame_count % interval_frames == 0:
            frames.append(frame)
            output_path = f"{output_folder}/frame_{len(frames)-1}.jpg"
            cv2.imwrite(output_path, frame)
            caption_to_kafka = testing_caption_generator.caption_image(output_path)
            producer.send('test-topic', value=caption_to_kafka)
            # print(f"Saved {output_path}")

            # Gọi hàm caption_image và lấy kết quả caption
            try:
                current_caption = caption_to_kafka
            except Exception as e:
                current_caption = f"Error generating caption: {e}"
                print(current_caption)

            # Đặt số khung hình còn lại để hiển thị caption
            caption_frames_remaining = caption_display_frames

        # Hiển thị caption nếu còn thời gian
        if caption_frames_remaining > 0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            color = (0, 0, 255)
            thickness = 1
            text_size, _ = cv2.getTextSize(current_caption, font, font_scale, thickness)
            text_x = 10  # Vị trí x của text
            text_y = frame.shape[0] - 10  # Vị trí y của text

            frame_with_caption = cv2.putText(
                frame,
                current_caption,
                (text_x, text_y),
                font,
                font_scale,
                color,
                thickness,
                cv2.LINE_AA,
            )
            cv2.imshow("Webcam", frame_with_caption)

            caption_frames_remaining -= 1
        else:
            cv2.imshow("Webcam", frame)

        frame_count += 1
        # print(f"Processed frame {frame_count}")

        # Chờ nhấn 'q' để thoát
        if cv2.waitKey(2) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Stopped capturing frames from webcam.")


def extract_key_frames_from_video(
    video_path, output_folder, interval_seconds=2, caption_display_duration=5
):
    cap = cv2.VideoCapture(video_path)  # Mở video từ đường dẫn
    if not cap.isOpened():
        print("Error opening video file")
        return

    frame_count = 0
    frames = []
    current_caption = ""
    caption_frames_remaining = 0

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: FPS is 0")
        cap.release()
        cv2.destroyAllWindows()
        return

    interval_frames = int(interval_seconds * fps)
    caption_display_frames = int(caption_display_duration * fps)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % interval_frames == 0:
            frames.append(frame)
            output_path = f"{output_folder}/frame_{len(frames)-1}.jpg"
            cv2.imwrite(output_path, frame)
            caption_to_kafka = testing_caption_generator.caption_image(output_path)
            producer.send('test-topic', value=caption_to_kafka)

            try:
                current_caption = caption_to_kafka
            except Exception as e:
                current_caption = f"Error generating caption: {e}"
                print(current_caption)

            caption_frames_remaining = caption_display_frames

        if caption_frames_remaining > 0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.7
            color = (0, 0, 255)
            thickness = 1
            text_size, _ = cv2.getTextSize(current_caption, font, font_scale, thickness)
            text_x = 10
            text_y = frame.shape[0] - 10
            frame_with_caption = cv2.putText(
                frame,
                current_caption,
                (text_x, text_y),
                font,
                font_scale,
                color,
                thickness,
                cv2.LINE_AA,
            )
            cv2.imshow("Video", frame_with_caption)

            caption_frames_remaining -= 1
        else:
            cv2.imshow("Video", frame)

        frame_count += 1

        if cv2.waitKey(2) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    producer.flush()
    producer.close()
    print("Stopped capturing frames from video.")



# # Example usage
output_folder = "result"
video_path = "TestVidMain.mp4"
extract_key_frames_from_webcam(output_folder)
# extract_key_frames_from_video(video_path, output_folder)
