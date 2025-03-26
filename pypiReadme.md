# git repo
<p>https://github.com/Tanish0907/yt-downloader-python_script-<p>

```markdown
# YouTube Downloader (Python Package)

A cross-platform YouTube video/audio downloader with quality options.

## Installation

1. Install FFmpeg:

   **Linux**:
   ```bash
   sudo apt install ffmpeg
   ```

   **Windows/macOS**:  
   Download from [ffmpeg.org](https://ffmpeg.org/) and add to PATH

2. Install the package:
   ```bash
   pip install yt-downloader
   ```

## Basic Usage

```bash
yt-download --video "URL" [--quality 720|1080|best]
yt-download --audio "URL"
yt-download --playlist "URL"
```

## Features

- Multiple quality options (720p, 1080p, best available)
- Audio extraction (MP3)
- Playlist support
- Cross-platform (Windows/macOS/Linux)

## Notes

- Downloads save to `./video_downloaded/`
- Clear this folder between downloads to avoid errors
- Requires Python 3.8+

## Troubleshooting

If you get FFmpeg errors:
1. Verify installation with `ffmpeg -version`
2. Ensure it's in your system PATH
```

Key points:
1. Removed clone/git instructions since it's a pip package
2. Simplified FFmpeg instructions
3. Added clear pip install command
4. Basic usage shows package entry point (`yt-download`)
5. Kept essential troubleshooting info
6. Removed redundant information

