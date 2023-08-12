import yt_dlp

ydl_opts = {'outtmpl': './video/%(title)s.%(ext)s'}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://youtu.be/...'])
