from pytube import YouTube

# Specify the URL of the YouTube video
video_url = "https://youtu.be/vWq-mIxvH3k"

# Create a YouTube object
yt = YouTube(video_url)

# Select the highest resolution stream
stream = yt.streams.get_highest_resolution()

# Define the output path for the downloaded video
output_path = "./video/"

# Download the video
stream.download(output_path)

print("Video downloaded successfully!")
