from pytube import YouTube
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
download_path = config['DOWNLOAD']['path']


def progress_bar(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining)/stream.filesize)*100
    print(f"♻️  Скачивается: {stream.default_filename}... ✳️  {current:.1f}% готово", end='\r')


def download_best_mp4_video(link):
    yt = YouTube(link, on_progress_callback=progress_bar)
    print(f"🎦 Видео для скачивания: {yt.title}")

    best_video = yt.streams.filter(progressive=True, file_extension='mp4') \
        .order_by('resolution').desc().first()
    #best_video.download()
    best_video.download(output_path=download_path)
    print(f"\n✅ Скачивание {yt.title} завершено!")


def is_valid_youtube_url(url):
    if "youtube.com" in url or "youtu.be" in url:
        return True
    return False

my_url = input("🌐 Введите ссылку на YouTube видео: ")


if is_valid_youtube_url(my_url):
    download_best_mp4_video(my_url)
else:
    print("🔞 Пожалуйста, введите корректную ссылку на YouTube видео.")
