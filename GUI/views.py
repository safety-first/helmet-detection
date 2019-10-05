#!/usr/bin/env python

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import cv2
import sys

class MainApp(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.video_size = QSize(671, 321)
        self.setup_ui()

    def setup_ui(self):
        """Initialize widgets."""

        # buttons created
        self.startButton = QPushButton("Start Streaming")
        self.quitButton = QPushButton("Quit")

        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        # layout for widgets
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.startButton)
        self.main_layout.addWidget(self.quitButton)

        self.setLayout(self.main_layout)

        self.startButton.clicked.connect(self.setup_camera)
        self.quitButton.clicked.connect(self.close)

    def setup_camera(self):
        """Initialize camera."""

        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget."""
        
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())
