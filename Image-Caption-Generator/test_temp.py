import cv2
import os
import numpy as np
import argparse
import time
import testing_caption_generator
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['192.168.88.246:9092'],  # Địa chỉ Kafka broker của bạn
    value_serializer=lambda v: v.encode('utf-8')  # Tuỳ chọn serializer cho chuỗi văn bản
)

def keyframeDetection(threshold):
    cap = cv2.VideoCapture(0)  # Mở kết nối với webcam (số 0 là webcam mặc định)

    keyframePath = 'result'
    if not os.path.exists(keyframePath):
        os.makedirs(keyframePath)

    # Đọc frame đầu tiên
    ret, prev_frame = cap.read()
    cv2.imwrite('result/0.jpg', prev_frame)  # Lưu frame đầu tiên với tên là '0.jpg'
    
    i = 1  # Số thứ tự frame được lưu
    count = 1  # Số lượng frame được lưu, bao gồm cả frame đầu tiên
    last_save_time = time.time()  # Thời gian lưu frame cuối cùng

    while cap.isOpened():
        ret, curr_frame = cap.read()
        if not ret:
            break
        
        diff = cv2.absdiff(curr_frame, prev_frame)
        non_zero_count = np.count_nonzero(diff)

        if non_zero_count > threshold:
            current_time = time.time()
            if current_time - last_save_time >= 3:  # Kiểm tra xem đã đủ 3 giây chưa
                print("Saving Frame number: {}".format(i), end='\r')
                cv2.imwrite('result/{}.jpg'.format(i), curr_frame)
                caption_to_kafka = testing_caption_generator.caption_image('result/{}.jpg'.format(i))
                producer.send('newtopic1', value=caption_to_kafka)
                # print(testing_caption_generator.caption_image('result/{}.jpg'.format(i)))
                count += 1
                last_save_time = current_time  # Cập nhật thời gian lưu frame cuối cùng
        
        prev_frame = curr_frame
        i += 1

        # Hiển thị frame gốc (không cần thiết cho việc trích xuất, chỉ để kiểm tra)
        cv2.imshow("Frame", curr_frame)
        
        # Thoát nếu nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("\nTotal Number of frames saved: {}".format(count))
    producer.flush()
    producer.close()
    cap.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--threshold', type=int, help='Threshold of the image difference', default=785000)
    args = parser.parse_args()

    keyframeDetection(args.threshold)