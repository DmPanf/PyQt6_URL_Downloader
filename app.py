import os
import sys
import requests
import re
from PyQt6.QtGui import QGuiApplication, QPalette, QColor, QFont
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QLineEdit, QLabel, QListWidget, QTextEdit, QHBoxLayout, QProgressBar)
import yt_dlp # as youtube_dl
from datetime import datetime

def generate_filename(directory, extension):
    i = 1
    while True:
        new_name = os.path.join(directory, f"youtube_{datetime.now().strftime('%Y_%m_%d')}_{i:02}{extension}")
        if not os.path.exists(new_name):
            return new_name
        i += 1

def is_valid_filename(filename):
    # Регулярное выражение для проверки имени файла на наличие недопустимых символов
    return not bool(re.search(r'[<>:"/\\|?*]', filename))

def download_youtube_audio(url, output_path, progress_hook=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'progress_hooks': [progress_hook] if progress_hook else []
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

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
                    output_path = "./video/%(title)s.%(ext)s"
                    self.download_using_ytdlp(video_url)
                    self.message_label.setText(f"Video downloaded successfully to {output_path}!")
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
        if "youtube.com" in video_url or "youtu.be" in video_url:
            try:
                filename = self.generate_filename(video_url)
                output_path = os.path.join("./video/", filename + ".mp3")
                download_youtube_audio(video_url, output_path, self.progress_hook)
                self.message_label.setText("Audio downloaded successfully!")
                self.update_video_list()
            except Exception as e:
                self.message_label.setText(f"Error: {str(e)}")
        else:
            self.message_label.setText("Audio download is only supported for YouTube links.")


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


    def download_using_ytdlp(self, url):
        output_directory = "./video/"
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        ydl_opts = {
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_extension = info_dict.get('ext', 'mp4')

            if video_title and not is_valid_filename(video_title):
                # Если имя файла недействительно, генерируем новое
                new_filename = generate_filename(output_directory, "." + video_extension)
                ydl_opts['outtmpl'] = new_filename

            ydl.download([url])


    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # d['total_bytes'] может быть None в некоторых случаях
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            
            if total_bytes is not None:
                progress = d['downloaded_bytes'] / total_bytes * 100
                self.progress_bar.setValue(int(progress))


    def progress_function(self, stream, chunk, file_handle, bytes_remaining):
        size = stream.filesize
        progress = (size - bytes_remaining) / size * 100
        self.progress_bar.setValue(progress)
        QApplication.processEvents()


    def reset_url(self):
        self.url_input.clear()
        self.message_label.clear()  # очищаем поле ошибки
        self.progress_bar.setValue(0)


    def generate_filename(self, video_url):
        # Если это YouTube URL
        if "youtube.com" in video_url or "youtu.be" in video_url:
            # Получаем название видео
            ydl_opts = {'quiet': True, 'skip_download': True, 'force_generic_extractor': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title = info.get('title', None)
        else:
            # Если это какой-то другой URL
            title = video_url.split("/")[-1].split(".")[0]

        # Убираем из названия видео запрещенные символы
        title = re.sub(r"[\/:*?\"<>|]", "", title)

        # Если такой файл уже существует, добавляем текущую дату к названию файла
        if os.path.exists(os.path.join("./video/", title + ".mp4")):
            title += "_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        return title


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoDownloaderApp()
    window.show()
    sys.exit(app.exec())
