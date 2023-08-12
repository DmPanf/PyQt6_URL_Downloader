import os
import sys
import requests
from PyQt6.QtGui import QGuiApplication, QPalette, QColor, QFont
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QLineEdit, QLabel, QListWidget, QTextEdit, QComboBox, QHBoxLayout, QProgressBar)
from pytube import YouTube


class VideoDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        # GUI Setup
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube Video and URL Links Downloader')
        self.setGeometry(600, 400, 790, 390)  # метода setGeometry() устанавливает позицию и размер # self.resize(500, 400)
        self.center()

        # Set Font
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        label = QLabel("⚙️ Список видео файлов:")
        layout.addWidget(label)

        # Lighter Video Files ListWidget
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Base, QColor(28, 28, 28))
        self.video_list = QListWidget()
        self.video_list.setPalette(palette)
        self.video_list.setFixedHeight(250)  # Устанавливаем высоту
        self.update_video_list()
        layout.addWidget(self.video_list)

        # Dark green URL Input Widget
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("URL...")  # добавляем фоновую надпись
        self.url_input.setStyleSheet("background-color: #464646;")
        layout.addWidget(self.url_input)

        self.reset_button = QPushButton('Reset URL', self)
        self.reset_button.setFixedHeight(40)  # Устанавливаем высоту
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #15a049;
                color: white;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
        """)
        self.reset_button.clicked.connect(self.reset_url)
        layout.addWidget(self.reset_button)


        self.download_button = QPushButton('Download File', self)
        self.download_button.setFixedHeight(40)  # Устанавливаем высоту
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #15a049;
                color: white;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
        """)
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        # Download audio button
        self.download_audio_button = QPushButton('Grab Audio', self)
        self.download_audio_button.setFixedHeight(40)  # Устанавливаем высоту
        self.download_audio_button.setStyleSheet("""
            QPushButton {
                background-color: #15a049;
                color: white;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
        """)
        self.download_audio_button.clicked.connect(self.download_audio)

        # Dropdown for Stream Selection
        #self.stream_dropdown = QComboBox(self)
        #self.stream_dropdown.setPlaceholderText("Stream selection...")  # добавляем фоновую надпись
        #layout.addWidget(self.stream_dropdown)

        # Resolution Layout (Dropdown & Button for Stream Selection)
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.setPlaceholderText("Stream selection...")  # добавляем фоновую надпись
        #layout.addWidget(self.resolution_combo)
        self.get_resolutions_button = QPushButton('Get Resolutions', self)
        self.get_resolutions_button.clicked.connect(self.get_available_resolutions)
        #layout.addWidget(self.get_resolutions_button)
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(self.resolution_combo)
        resolution_layout.addWidget(self.get_resolutions_button)
        layout.addLayout(resolution_layout)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.download_audio_button)
        layout.addLayout(button_layout)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # QTextEdit to copy text with modified height and color
        self.message_label = QTextEdit('')
        self.message_label.setPlaceholderText("Вывод информации...")  # добавляем фоновую надпись
        self.message_label.setReadOnly(True)
        self.message_label.setFixedHeight(60)  # Устанавливаем высоту
        self.message_label.setStyleSheet("background-color: #1E1E1E;")  # Темный цвет фона
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
                if "youtube.com" in video_url or "youtu.be" in video_url:
                    selected_stream = self.resolution_combo.currentData()
                    if selected_stream:
                        output_path = "./video/" + selected_stream.title + ".mp4"
                        selected_stream.download(output_path=output_path)
                        self.message_label.setText(f"Video downloaded successfully to {output_path}!")
                    else:
                        self.message_label.setText(f"Please select a resolution first!")
                    self.update_video_list()
                else:
                    # Скачивание файла по обычной ссылке
                    output_path = "./video/" + video_url.split("/")[-1]
                    self.download_file(video_url, output_path)
                    self.message_label.setText(f"File downloaded successfully to {output_path}!")
                
                self.update_video_list()
            except Exception as e:
                self.message_label.setText(f"Error: {str(e)}")
        else:
            self.message_label.setText("Please enter a valid URL.")


    def download_audio(self):
        video_url = self.url_input.text()
        if video_url:
            try:
                yt = YouTube(video_url, on_progress_callback=self.progress_function)
                stream = yt.streams.filter(only_audio=True).first()
                output_path = "./video/"
                stream.download(output_path)
                self.message_label.setText("Audio downloaded successfully!")
                self.update_video_list()
            except Exception as e:
                self.message_label.setText(f"Error: {str(e)}")
        else:
            self.message_label.setText("Please enter a valid URL.")


    def download_file(self, url, output_path):
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            num_blocks = total_size // block_size
            
            with open(output_path, 'wb') as file:
                for block in response.iter_content(block_size):
                    file.write(block)
                    self.progress_bar.setValue(int(self.progress_bar.value() + 1 / num_blocks * 100))


    def progress_function(self, stream, chunk, file_handle, bytes_remaining):
        size = stream.filesize
        progress = (size - bytes_remaining) / size * 100
        self.progress_bar.setValue(progress)
        QApplication.processEvents()

    def get_available_resolutions(self):
        video_url = self.url_input.text()
        if "youtube.com" in video_url or "youtu.be" in video_url:
            try:
                yt = YouTube(video_url)
                streams = yt.streams.filter(progressive=True, file_extension='mp4').all()
                
                self.resolution_combo.clear()
                for stream in streams:
                    self.resolution_combo.addItem(f"{stream.resolution} ({stream.mime_type})", stream)
                
            except Exception as e:
                self.message_label.setText(f"Error: {str(e)}")
        else:
            self.message_label.setText("Please enter a valid YouTube URL.")

    def reset_url(self):
        self.url_input.clear()
        self.message_label.clear()  # очищаем поле ошибки


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoDownloaderApp()
    window.show()
    sys.exit(app.exec())
