from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
Long_description = (this_directory / "pypiReadme.md").read_text()
setup(
    author="Tanish",
    author_email="sharmatanish097654@gmail.com",
    description="ytdl is a command line tool to search and download videos in 1080p from yt using the command line.",
    long_description_content_type='text/markdown',
    long_description=Long_description,
    name="yt-download",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "yt-dl",
        "ffmpeg-python",
        "click",
        "rich",
        "pandas" 
    ],
    keywords=["python","ytdl_1080p","ytdl-1080p","ytdl 1080p","1080p","ytdl1080p","youtube","youtube downloader","ytdl","Ytdl","1080p yt downloader","downloader","pytube"],
    entry_points={
        "console_scripts": [
            "ytdl=Ytdl_1080p.main:main",
        ],
    },
)
