import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget
#from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from pytube import YouTube
import os


class VideoDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        # GUI Setup
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube Video Downloader')
        self.setGeometry(600, 300, 400, 300)
        self.center()

        layout = QVBoxLayout(self)

        self.video_list = QListWidget()
        self.update_video_list()
        layout.addWidget(self.video_list)

        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        self.message_label = QLabel('')
        layout.addWidget(self.message_label)

        self.setLayout(layout)

    def center(self):
        frame = self.frameGeometry()
        center_point = QGuiApplication.primaryScreen().geometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def update_video_list(self):
        if os.path.exists("./video/"):
            videos = os.listdir("./video/")
            self.video_list.clear()
            self.video_list.addItems(videos)

    def download_video(self):
        video_url = self.url_input.text()
        if video_url:
            try:
                yt = YouTube(video_url)
                stream = yt.streams.get_highest_resolution()
                output_path = "./video/"
                stream.download(output_path)
                self.message_label.setText("Video downloaded successfully!")
                self.update_video_list()
            except Exception as e:
                self.message_label.setText(f"Error: {str(e)}")
        else:
            self.message_label.setText("Please enter a valid URL.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoDownloaderApp()
    window.show()
    sys.exit(app.exec())
