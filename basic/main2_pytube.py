# PyTube (https://pytube.io/en/latest/) — для быстрой загрузки видео с YouTube
from pytube import YouTube

def download_best_mp4_video(link):
    yt = YouTube(link)
    best_video = yt.streams.filter(progressive=True, file_extension='mp4') \
        .order_by('resolution').desc().first()
    best_video.download()

my_link = 'https://youtu.be/...'
#YouTube(my_link).streams.first().download() # .3gpp
download_best_mp4_video(my_link)
