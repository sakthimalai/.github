import cv2
import os
from ultralytics import YOLO
import numpy as np
from PIL import Image


class Model:
    def __init__(self) -> None:
        self.ld = YOLO('./assets/best.pt')
        self.mouth = YOLO('./assets/mouth.pt')
        self.frame_iterator = 0
        self.lumpy_skin_count = 0
        self.mouth_disease_count = 0

    def compute_disease(self, image):
        if self.frame_iterator % 20 == 0:
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Convert the grayscale image to a PIL Image
            pil_image = Image.fromarray(gray_image)

            # Pass the grayscale image to the lumpy YOLO model
            lump_results = self.ld(pil_image, verbose=False, show=False)

            # Pass the original BGR image to the mouth YOLO model
            mouth_results = self.mouth(image, verbose=False, classes=[1], show = False)

            # Process lumpy skin detection results
            lumpy_skin_detected = self.process_yolo_results(lump_results, self.ld.names, 0.5)
            self.lumpy_skin_count += len(lumpy_skin_detected)

            # Process mouth disease detection results
            mouth_disease_detected = self.process_yolo_results(mouth_results, self.mouth.names, 0.3)
            self.mouth_disease_count += len(mouth_disease_detected)

            self.frame_iterator += 1

            return lumpy_skin_detected, mouth_disease_detected
        else:
            self.frame_iterator += 1
            return False, False
        
    def reset_counts(self):
        self.lumpy_skin_count = 0
        self.mouth_disease_count = 0

    def process_yolo_results(self, results, class_names, confidence_threshold):
        detected_classes = []
        for result in results:
            boxes = result.boxes.cpu().numpy()
            xyxy = boxes.xyxy
            cors = np.array(xyxy)
            clas = boxes.cls
            conf = boxes.conf

        for c in conf:
            if c > confidence_threshold:
                class_index = int(clas[0])
                class_name = class_names[class_index]
                detected_classes.append(class_name)
                break  # Break out of the loop once a confident detection is found

            
        return detected_classes

    # def print_disease_counts(self):
    #     print(f"Lumpy Skin Disease Count: {self.lumpy_skin_count}")
    #     print(f"Mouth Disease Count: {self.mouth_disease_count}")
