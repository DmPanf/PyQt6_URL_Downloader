import youtube_dl

ydl_opts = {'outtmpl': './video/%(title)s.%(ext)s'}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://youtu.be/vWq-mIxvH3k'])
