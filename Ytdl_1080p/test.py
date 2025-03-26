from pytube import YouTube
from urllib.error import HTTPError

try:
    yt = YouTube("https://www.youtube.com/watch?v=k4yPRETjvvw")
    print(f"Downloading: {yt.title}")
    # rest of your download code
except HTTPError as e:
    print(f"YouTube API request failed: {e}")
    print("This might be due to an outdated pytube version. Try: pip install --upgrade pytube")
except Exception as e:
    print(f"An error occurred: {e}")