import sys
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFileDialog,   
)
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon, QColor, QLinearGradient
from PyQt5.QtCore import QThread, pyqtSignal
from model import Model
from mongo import MongoDBManager
from datetime import datetime
from drive import DriveUploader
from PIL import Image
import time

class LedIndicator(QWidget):
    def __init__(self, label_text):
        super().__init__()

        self.label = QLabel(label_text)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.side_length = 10  # Reduced the size of the indicators
        self.led_radius = 9  # Reduced the radius of the indicators
        self.setMinimumSize(self.led_radius * 2, self.led_radius * 2)
        #self.status = False  # Initial status
        self.color = "#FFFFFF"
        
    def set_status(self, status):
        self.status = status
        if self.status:
            self.color = "#FF6347"  # Set color to red if disease is detected
        else:
            self.color = "#32CD32"  # Set color to green if no disease is detected
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(self.color)))
        painter.drawEllipse(self.rect().center(), self.led_radius, self.led_radius)


class VideoViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

        # Connect button click event
        self.pushButton.clicked.connect(self.choose_video)
        self.askAiButton.clicked.connect(self.askai)

        # Video processing variables
        self.video_path = None
        self.video_thread = None
        self.model = Model()
        self.mongo = MongoDBManager()
        self.drive =  DriveUploader()

    def setupUi(self):
        self.setObjectName("UVA")
        self.resize(877, 686)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 851, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("VeneerW01-Two")
        font.setPointSize(34)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        # Adjusted geometry for videoFrame and progressBar
        self.videoFrame = QtWidgets.QLabel(self)
        self.videoFrame.setGeometry(QtCore.QRect(10, 100, 441, 531))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.videoFrame.setFont(font)
        self.videoFrame.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.videoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoFrame.setObjectName("videoFrame")
        
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(10, 640, 481, 23))
        font = QtGui.QFont()
        font.setBold(False)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
    
        # Adjusted geometry for pushButton
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(520, 623, 300, 40)) 
        #self.pushButton.setGeometry(QtCore.QRect(10, 640, 441, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        # Set button color, text color, border radius, and hover effect
        self.pushButton.setStyleSheet(
            "QPushButton { background-color: #04D939; color: white; border-radius: 10px; border: 2px solid #04D939; }"
            "QPushButton:hover { background-color: transparent; color: #04D939; border: 2px solid #04D939; }"
        )
        
        self.askAiButton = QtWidgets.QPushButton(self)
        self.askAiButton.setGeometry(QtCore.QRect(520, 570, 300, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        self.askAiButton.setFont(font)
        self.askAiButton.setObjectName("askAiButton")
        self.askAiButton.setStyleSheet(
            "QPushButton { background-color: white; color: black; border-radius: 10px; border: 2px solid white; }"
            "QPushButton:hover { background-color: transparent; color: white; border: 2px solid white; }"
        )
        self.askAiButton.setText("Ask AI")
        
        
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(610, 340, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet("color: white;")

        # Adding colored circles before disease names
        self.circle_indicator_1 = LedIndicator("Lumpy Skin Disease")
        #self.circle_indicator_1.setFixedWidth(10)
        
        self.circle_indicator_1.setGeometry(QtCore.QRect(580, 350, 20, 20))
        #self.circle_indicator_1.setFixedSize(10,20)
        #self.circle_indicator_1.set_status(False)
        self.circle_indicator_1.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")# Initial status
        self.circle_indicator_1.setParent(self)  # Set VideoViewer as the parent

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(610, 390, 200, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet("color: white;")

        # Adding colored circles before disease names
        self.circle_indicator_2 = LedIndicator("Mouth Disease")
        self.circle_indicator_2.setGeometry(QtCore.QRect(580, 400, 20, 20))
        #self.circle_indicator_2.set_status(False)
        self.circle_indicator_2.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")  # Initial status
        self.circle_indicator_2.setParent(self)  # Set VideoViewer as the parent

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "UVA"))
        self.label.setText(_translate("Dialog", "UNISYS VETERINARY ASSISTANT"))
        self.pushButton.setText(_translate("Dialog", "Upload Video"))
        self.label_2.setText(_translate("Dialog", "Lumpy Skin Disease"))
        self.label_3.setText(_translate("Dialog", "Mouth Disease"))

    def choose_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi *.mkv)")
        file_dialog.setOptions(options)

        if file_dialog.exec_() == QFileDialog.Accepted:
            self.video_path = file_dialog.selectedFiles()[0]
            self.start_video_processing()
            
    def askai(self):
        # Define the website link
        website_link = "https://uvaveterinaryassistant.streamlit.app/"  # Replace this with your desired website link

        # Open the website in the default web browser
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(website_link))

    def start_video_processing(self):
        if self.video_path:
            self.video_thread = VideoProcessingThread(self.video_path,self.mongo,self.model,self.drive)
            self.video_thread.progress_updated.connect(self.progress_updated)
            self.video_thread.frame_processed.connect(self.update_video_frame)
            self.video_thread.disease_detected_updated.connect(self.disease_detected_updated)
            self.video_thread.start()

    def progress_updated(self, progress_value):
        self.progressBar.setValue(progress_value)

    def update_video_frame(self, qimage):
        # Resize the image to fit the QLabel
        pixmap = QPixmap.fromImage(qimage)
        pixmap = pixmap.scaled(self.videoFrame.size(), QtCore.Qt.KeepAspectRatio)

        # Calculate the position to center the pixmap within the videoFrame
        x = (self.videoFrame.width() - pixmap.width()) / 2
        y = (self.videoFrame.height() - pixmap.height()) / 2

        # Set the position of the pixmap
        self.videoFrame.setPixmap(pixmap)
        self.videoFrame.setAlignment(QtCore.Qt.AlignCenter)
        self.videoFrame.setContentsMargins(int(x), int(y), int(x), int(y))

    def disease_detected_updated(self, is_lumpy_skin, is_mouth_disease):
        self.circle_indicator_1.set_status(is_lumpy_skin)
        self.circle_indicator_2.set_status(is_mouth_disease)

class VideoProcessingThread(QThread):
    frame_processed = pyqtSignal(QImage)
    progress_updated = pyqtSignal(int)
    disease_detected_updated = pyqtSignal(bool, bool)

    def __init__(self, video_path, mongo, model, drive):
        super().__init__()
        self.video_path = video_path
        # Add model initialization here
        self.model = model
        self.mongo = mongo
        self.drive = drive
        self.lumpyid = '1oa5WRfR_g9LXvy1Lw3Lnh8AxUL-T42Lk'
        self.mouthid = '1QS1ilEB_Zyeux5z00-sJPqM4s5xUrvBU'
        self.ll = []
        self.mm = []
        self.lc = 0
        self.mc = 0
        
        

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frame = 0
        start_time = time.time()
        

        while True:
            ret, frame = cap.read()
            if ret:
                current_frame += 1
                progress_value = int((current_frame / total_frames) * 100)
                self.progress_updated.emit(progress_value)

                index = self.model.compute_disease(frame)

                if index is not None and len(index) >= 2:
                    if index[0] == ['Brown_lumpy']:               
                        self.ll.append(frame)               #storing frames of disease to save in drive 
                    if index[1] == ['Mouth Disease Infected']:
                        #print(index[1])
                        self.mm.append(frame)
                        
                    #This is for indicator purpose
                    if self.model.lumpy_skin_count > self.model.mouth_disease_count:
                        self.disease_detected_updated.emit(True, False)
                    elif self.model.mouth_disease_count > self.model.lumpy_skin_count:
                        self.disease_detected_updated.emit(False, True)
                    else:
                        self.disease_detected_updated.emit(False, False)
                # Convert frame to QImage for PyQt compatibility
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channels = rgb_image.shape
                bytes_per_line = channels * width
                qimage = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.frame_processed.emit(qimage)
                # Calculate time taken to process the frame
                end_time = time.time()
                time_taken = end_time - start_time

                # Adjust the delay based on the time taken to process the frame
                fps = cap.get(cv2.CAP_PROP_FPS)
                delay = max(1 / fps - time_taken, 0)  # Ensure delay is non-negative
                time.sleep(delay)

                start_time = time.time()  # Update start time for the next frame
            else:
                # Add logic for end of video processing
                # self.model.print_disease_counts()
                selected_frames = 2
                
                #this is for the indicator and image uploading to drive
                if self.model.lumpy_skin_count > self.model.mouth_disease_count:
                    self.disease_detected_updated.emit(True, False)  #indicator
                    
                    for image_data in self.ll:
                        if selected_frames == 0:
                            break
                        image = Image.fromarray(image_data)     #converting to PIL image format from numpy array
                        self.drive.upload_image_to_drive(image, self.lumpyid)
                        selected_frames-=1                     #Uploading the image to drive
                    self.lc += 1
                    
                elif self.model.mouth_disease_count > self.model.lumpy_skin_count:
                    self.disease_detected_updated.emit(False, True)  #indicator
                    for image_data in self.mm:
                        if selected_frames == 0:
                            break
                        image = Image.fromarray(image_data)
                        self.drive.upload_image_to_drive(image, self.mouthid)
                        selected_frames-=1
                    self.mc += 1
                    
                else:
                    self.disease_detected_updated.emit(False, False)
                    
                current_date = datetime.now().date()
                current_date_str = current_date.isoformat()
                    
                disease_details = {
                'date': current_date_str,
                'lumpy_skin_count': self.lc,
                'mouth_disease_count': self.mc }
                
                self.mongo.insert_document(disease_details)
                self.model.reset_counts()
                cap.release()
                break
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = VideoViewer()
    palette = QtGui.QPalette()
    background_image = QPixmap("assets/1594429_11593.jpg")  # Replace "background_image.jpg" with your image file path
    background_image = background_image.scaled(window.size(), QtCore.Qt.IgnoreAspectRatio)    
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(background_image))
        


    # palette.setColor(
    #     QtGui.QPalette.Window, QtGui.QColor("black")
    # )  # Dark blue background
    palette.setColor(
        QtGui.QPalette.WindowText, QtGui.QColor("#0FD343")
    )  # Neon blue text
    palette.setColor(
        QtGui.QPalette.ButtonText, QtGui.QColor("#014f15")
    )  # Dark blue button text
    window.setPalette(palette)
    window.show()
    sys.exit(app.exec_())



