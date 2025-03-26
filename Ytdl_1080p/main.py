# from pytube import YouTube,Search
# import pytube.contrib.playlist as pl
# import os
# import ffmpeg
# import shutil
# from concurrent.futures import ThreadPoolExecutor
# from multiprocessing.dummy import Pool as ThreadPool
# import click
# import pandas
# from rich import print
# from rich.table import Table
# import getpass
# global x
# global vid_dict
# download_folder="./video_downloaded/"
# pool=ThreadPoolExecutor(2)
# if not os.path.exists(download_folder):
#     os.mkdir("./video_downloaded")

    
# def combine(vid_path,audio_path,source_path):
#     output_path=download_folder
#     vids=[]
#     audio=[]
#     for file_path in os.listdir(vid_path):
#         # check if current file_path is a file
#         if os.path.isfile(os.path.join(vid_path, file_path)):
#             # add filename to list
#             vids.append(os.path.join(vid_path, file_path))
#     for file_path in os.listdir(audio_path):
#         # check if current file_path is a file
#         if os.path.isfile(os.path.join(audio_path, file_path)):
#             # add filename to list
#             audio.append(os.path.join(audio_path, file_path))
#     for i in range(len(vids)):
#         audio_input_file = audio[i]
#         video_input_file = vids[i]
#         output_file =  vids[i].split('/')[-1]
#         # subprocess.run(f"ffmpeg -i {video_input_file} -i {audio_input_file} -c:v copy -c:a aac {output_file}",shell=True)
#         # Load the audio and video streams
#         audio_stream = ffmpeg.input(audio_input_file)
#         video_stream = ffmpeg.input(video_input_file)

#         # Merge the audio and video streams
#         ffmpeg.output(video_stream, audio_stream, output_file, vcodec='copy', acodec='aac', strict='experimental').run()

#         # Run the FFmpeg command
#         file=f"./{output_file}"
#         destination=output_path
#         shutil.move(file,destination)
#         os.remove(vids[i])
#         os.remove(audio[i])
#     os.rmdir(source_path+".mp3")
#     os.rmdir(source_path)
    


# def vid(s,path=None):
    
#     video = YouTube(s)
#     if path==None:
#         path = "./"+video.title+"/"
#         os.makedirs(path)
#     print("title of video:", video.title)
#     print("length of video:", format(video.length/60, ".2f"), "minutes")
#     print("no of views:", video.views)
#     vid = video.streams.filter(res="1080p")
#     try:
#         test=vid[0]
#         print("downloading 1080p")
#         vid=video.streams.filter(res="1080p").first()
#     except:
#         print("1080p not available downloading 720p instead!!!")
#         vid=video.streams.filter(res="720p").first()
#         vid.download(path)
#         print("video-downloaded")
#         shutil.move(path,download_folder)
#         return("done")

#     audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()
#     try:
#         vid_thread=pool.submit(vid.download,path)
#         audio_thread=pool.submit(audio.download,path+".mp3")
#         # vid.download(path)
#         # audio.download(path+".mp3")
#     except:
#         pass
#     print(vid_thread.result(),audio_thread.result())
#     if vid_thread.done() and audio_thread.done():
#         combine(path,path+".mp3",path)
        

# def plst(s):
#     global path
#     playlist = pl.Playlist(s)
#     path = "./"+playlist.title+"/"
#     os.makedirs(path)
#     print("title of playlist:", playlist.title)
#     print("no of videos:", playlist.length)
#     video = playlist.video_urls
#     for i in video:
#         print("".center(50, "-"))
#         vid(i,path)

# def music(s):
#     video = YouTube(s)
#     path = "./"+video.title+"/"
#     n=1
#     if video.title in os.listdir("./video_downloaded"):
#         path = "./"+video.title+f"({n})/"
#         n=n+1
#     os.makedirs(path)
#     print("title of video:", video.title)
#     print("length of video:", format(video.length/60, ".2f"), "minutes")
#     print("no of views:", video.views)
#     audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()
#     audio.download(path)
#     shutil.move(path,"./video_downloaded")
# def music_plst(s):
#     playlist = pl.Playlist(s)
#     print("title of playlist:", playlist.title)
#     print("no of videos:", playlist.length)
#     video = playlist.video_urls
#     for i in video:
#         print("".center(50, "-"))
#         music(i)
# def table_print(dataframe: pandas.DataFrame):
#     table = Table(title="list of videos")
#     table.add_column("ID", justify="right", style="purple", no_wrap=True)
#     table.add_column("Title", style="magenta")
#     table.add_column("Length", justify="right", style="red", no_wrap=True)
#     table.add_column("Link", justify="right", style="blue", no_wrap=True)
#     for i in range(len(dataframe)):
#         table.add_row(dataframe.loc[i,"ID"],dataframe.loc[i,"Title"],dataframe.loc[i,"Length"],dataframe.loc[i,"Link"])
#     print(table)
# vid_dict={'ID':[],"Title":[],"Length":[],"Link":[]}  
# def get_vid_info(i):
#     video = i
#     vid_dict['ID'].append(str(video.video_id))
#     vid_dict['Title'].append(str(video.title))
#     vid_dict['Length'].append(str(format(video.length/60, ".2f")))
#     vid_dict['Link'].append(f"[link={video.watch_url}]LINK[/link]")

# @click.command()
# @click.option("--search", help="search")
# @click.option("--download_video", help="download video")
# @click.option("--download_music", help="download music")

# def main(search=None, download_video=None,download_music=None, info=None):
#     downloads_folder="./video_downloaded"
#     user=getpass.getuser()
#     downloads=f"/home/{user}/Downloads"
#     if download_folder in os.listdir(f'/home/{user}/Downloads'):
#         os.rmdir(f"home/{user}/Downloads/video_downloaded")
#     if search!=None:
#         res=Search(search).results
#         pool=ThreadPool(10)
#         pool.map(get_vid_info,res)
#         pool.close()
#         pool.join()
#         df=pandas.DataFrame(vid_dict)
#         table_print(df)
#     elif download_video!=None:
#         link = download_video
#         if ("list=" in link):
#             plst(link)
#             shutil.move(downloads_folder,downloads)
#             print("finished".center(50, "-"))
#         else:
#             vid(link)
#             shutil.move(downloads_folder,downloads)
#             print("finished".center(50, "-"))
#     elif download_music!=None:
#         link = download_music
#         if ("list=" in link):
#             music_plst(link)
#             shutil.move(downloads_folder,downloads)
#             print("finished".center(50, "-"))
#         else:
#             music(link)
#             shutil.move(downloads_folder,downloads)
#             print("finished".center(50, "-"))

# if __name__ == "__main__":
#     main()
#new code 
import yt_dlp
import os
import shutil
import sys
from rich import print
from rich.progress import Progress
import click
import ffmpeg

# Cross-platform configuration
DOWNLOAD_FOLDER = os.path.join(".", "video_downloaded")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    """Remove invalid characters from filenames across different OSes"""
    if sys.platform == "win32":
        # Windows has more restricted filename characters
        invalid_chars = '<>:"/\\|?*'
    else:
        invalid_chars = '/'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_video(url, quality='best'):
    ydl_opts = {
        'format': f'bv*[height<={quality}]+ba/b[height<={quality}]' if quality != 'best' else 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'restrictfilenames': True,  # Helps with cross-platform filename compatibility
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Sanitize the filename for the current platform
            safe_title = sanitize_filename(info['title'])
            video_file = os.path.join(DOWNLOAD_FOLDER, f"{safe_title}.mp4")
            
            # Handle case where extension might be different
            if not os.path.exists(video_file):
                # Try to find the actual downloaded file
                for f in os.listdir(DOWNLOAD_FOLDER):
                    if f.startswith(safe_title):
                        video_file = os.path.join(DOWNLOAD_FOLDER, f)
                        break
            
            print(f"\n[green]Download complete: {info['title']}[/green]")
            return video_file
    except Exception as e:
        print(f"[red]Error downloading {url}: {e}[/red]")
        return None

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"[cyan]Downloading... {percent} at {speed}, ETA: {eta}[/cyan]", end='\r')
    elif d['status'] == 'finished':
        print("\n[green]Processing video...[/green]")

def download_playlist(url, quality='best'):
    ydl_opts = {
        'format': f'bv*[height<={quality}]+ba/b[height<={quality}]' if quality != 'best' else 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(playlist_index)s - %(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'yes_playlist': True,
        'restrictfilenames': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print(f"\n[green]Playlist download complete: {info['title']}[/green]")
            return True
    except Exception as e:
        print(f"[red]Error downloading playlist {url}: {e}[/red]")
        return False

def download_audio(url):
    audio_folder = os.path.join(DOWNLOAD_FOLDER, ".mp3")
    os.makedirs(audio_folder, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(audio_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'quiet': True,
        'restrictfilenames': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            safe_title = sanitize_filename(info['title'])
            audio_file = os.path.join(audio_folder, f"{safe_title}.mp3")
            
            # Handle case where extension might be different
            if not os.path.exists(audio_file):
                for f in os.listdir(audio_folder):
                    if f.startswith(safe_title) and f.endswith('.mp3'):
                        audio_file = os.path.join(audio_folder, f)
                        break
            
            print(f"\n[green]Audio download complete: {info['title']}[/green]")
            return audio_file
    except Exception as e:
        print(f"[red]Error downloading audio {url}: {e}[/red]")
        return None
    
def combine(vid_path, audio_path, output_path):
    try:
        # Get video and audio files with case-insensitive matching (important for macOS)
        video_files = [f for f in os.listdir(vid_path) if f.lower().endswith('.mp4')]
        audio_files = [f for f in os.listdir(audio_path) if f.lower().endswith('.mp3')]
        
        if not video_files or not audio_files:
            print("[red]No video or audio files found to combine[/red]")
            return
            
        # Sort files to ensure they match
        video_files.sort()
        audio_files.sort()
        
        # Find matching pairs based on filenames (without extensions)
        video_base = os.path.splitext(video_files[0])[0]
        audio_base = os.path.splitext(audio_files[0])[0]
        
        # Use the first matching pair
        video_file = os.path.join(vid_path, video_files[0])
        audio_file = os.path.join(audio_path, audio_files[0])
        
        output_file = os.path.join(output_path, f"{video_base}_combined.mp4")
        
        print(f"[yellow]Combining {video_file} with {audio_file}...[/yellow]")
        
        # Load the audio and video streams
        video_stream = ffmpeg.input(video_file)
        audio_stream = ffmpeg.input(audio_file)
        
        # Merge the audio and video streams
        ffmpeg.output(
            video_stream, 
            audio_stream, 
            output_file, 
            vcodec='copy', 
            acodec='aac', 
            strict='experimental'
        ).run(overwrite_output=True)
        
        print(f"[green]Successfully created: {output_file}[/green]")
        
        # Clean up - handle permission errors on Windows
        try:
            os.remove(video_file)
            os.remove(audio_file)
        except PermissionError as pe:
            print(f"[yellow]Warning: Could not delete temporary files due to permissions: {pe}[/yellow]")
        
        print("finished".center(50, "-"))
        
    except Exception as e:
        print(f"[red]Error combining files: {e}[/red]")

@click.command()
@click.option("--video", help="Download a single video")
@click.option("--playlist", help="Download a playlist")
@click.option("--audio", help="Download audio only")
@click.option("--quality", default="1080", help="Video quality (e.g., 720, 1080, best)")
def main(video=None, playlist=None, audio=None, quality="best"):
    try:
        if video:
            print(f"[yellow]Downloading video: {video}[/yellow]")
            video_file = download_video(video, quality)
            
            if video_file and (quality == "1080" or quality == "best"):
                print(f"[yellow]Downloading audio for: {video}[/yellow]")
                audio_file = download_audio(video)
                
                if audio_file:
                    combine(
                        DOWNLOAD_FOLDER,
                        os.path.join(DOWNLOAD_FOLDER, ".mp3"),
                        DOWNLOAD_FOLDER
                    )
                    
        elif playlist:
            print(f"[yellow]Downloading playlist: {playlist}[/yellow]")
            download_playlist(playlist, quality)
        elif audio:
            print(f"[yellow]Downloading audio: {audio}[/yellow]")
            download_audio(audio)
        else:
            print("[red]No download option specified[/red]")
            print("[blue]Usage: python script.py --video URL [--quality 720|1080|best][/blue]")
    except KeyboardInterrupt:
        print("\n[red]Operation cancelled by user[/red]")
    except Exception as e:
        print(f"[red]Unexpected error: {e}[/red]")

if __name__ == "__main__":
    main()