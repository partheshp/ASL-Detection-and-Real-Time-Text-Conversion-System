# Import libraries

import cv2
import numpy as np
import os

# Save Image in directory
def save_image(class_label, count, roi, directory):
    cv2.imwrite(os.path.join(directory, class_label, f"{count}.jpg"), roi)

def main():
    directory = 'ASL_python/Dataset/testingData/'
    minValue = 70
    if not os.path.exists(directory):
        os.makedirs(directory)
    class_labels = ['zero', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for label in class_labels:
        class_directory = os.path.join(directory, label)
        if not os.path.exists(class_directory):
            os.makedirs(class_directory)
    class_counts = {label: len(os.listdir(os.path.join(directory, label))) for label in class_labels}
    key_map = {ord(label[0]): label for label in class_labels}
    cap = cv2.VideoCapture(0)
    interrupt = -1
    while True:
        _, frame = cap.read()
        frame = cv2. flip(frame, 1)
        for label, count in class_counts.items():
            cv2.putText(frame, f"{label.upper()}: {count}", (10, 60+10 * ord(label[0]) - ord('a')), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
        
        x1, y1, x2, y2 = int(0.5 * frame.shape[1]), 10, frame.shape[1] - 10, int(0.5 * frame.shape[1])
        cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)
        roi = frame[y1:y2, x1:x2]
        #prewitts mask
        # Apply Prewitt's mask for edge detection
        prewitt_kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        prewitt_kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        edges_x = cv2.filter2D(roi, -1, prewitt_kernel_x)
        edges_y = cv2.filter2D(roi, -1, prewitt_kernel_y)
        edges = cv2.addWeighted(edges_x, 0.5, edges_y, 0.5, 0)
        # Gaussian blur
        gray = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 2)

        th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        _, test_image = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        test_image = cv2.resize(test_image, (300, 300))
        cv2.imshow("test", test_image)
        cv2.imshow("Frame", frame)
        interrupt = cv2.waitKey(10)
        if interrupt & 0xFF == 27:  # esc key
            break
        elif interrupt & 0xFF in key_map:
            class_label = key_map[interrupt & 0xFF]
            save_image(class_label, class_counts[class_label], test_image, directory)
            class_counts[class_label] += 1
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()