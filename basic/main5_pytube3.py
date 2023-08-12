from pytube import YouTube

yt = YouTube('https://youtu.be/...')
stream = yt.streams.get_highest_resolution()
stream.download('./video/')
