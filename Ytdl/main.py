from pytube import YouTube,Search
import pytube.contrib.playlist as pl
import os
import ffmpeg
import shutil
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
import click
import pandas
from rich import print
from rich.table import Table
import getpass
global x
global vid_dict
download_folder="./video_downloaded/"
pool=ThreadPoolExecutor(2)
if not os.path.exists(download_folder):
    os.mkdir("./video_downloaded")

    
def combine(vid_path,audio_path,source_path):
    output_path=download_folder
    vids=[]
    audio=[]
    for file_path in os.listdir(vid_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(vid_path, file_path)):
            # add filename to list
            vids.append(os.path.join(vid_path, file_path))
    for file_path in os.listdir(audio_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(audio_path, file_path)):
            # add filename to list
            audio.append(os.path.join(audio_path, file_path))
    for i in range(len(vids)):
        audio_input_file = audio[i]
        video_input_file = vids[i]
        output_file =  vids[i].split('/')[-1]
        # subprocess.run(f"ffmpeg -i {video_input_file} -i {audio_input_file} -c:v copy -c:a aac {output_file}",shell=True)
        # Load the audio and video streams
        audio_stream = ffmpeg.input(audio_input_file)
        video_stream = ffmpeg.input(video_input_file)

        # Merge the audio and video streams
        ffmpeg.output(video_stream, audio_stream, output_file, vcodec='copy', acodec='aac', strict='experimental').run()

        # Run the FFmpeg command
        file=f"./{output_file}"
        destination=output_path
        shutil.move(file,destination)
        os.remove(vids[i])
        os.remove(audio[i])
    os.rmdir(source_path+".mp3")
    os.rmdir(source_path)
    


def vid(s,path=None):
    
    video = YouTube(s)
    if path==None:
        path = "./"+video.title+"/"
        os.makedirs(path)
    print("title of video:", video.title)
    print("length of video:", format(video.length/60, ".2f"), "minutes")
    print("no of views:", video.views)
    vid = video.streams.filter(res="1080p")
    try:
        test=vid[0]
        print("downloading 1080p")
        vid=video.streams.filter(res="1080p").first()
    except:
        print("1080p not available downloading 720p instead!!!")
        vid=video.streams.filter(res="720p").first()
        vid.download(path)
        print("video-downloaded")
        shutil.move(path,download_folder)
        return("done")

    audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()
    try:
        vid_thread=pool.submit(vid.download,path)
        audio_thread=pool.submit(audio.download,path+".mp3")
        # vid.download(path)
        # audio.download(path+".mp3")
    except:
        pass
    print(vid_thread.result(),audio_thread.result())
    if vid_thread.done() and audio_thread.done():
        combine(path,path+".mp3",path)
        

def plst(s):
    global path
    playlist = pl.Playlist(s)
    path = "./"+playlist.title+"/"
    os.makedirs(path)
    print("title of playlist:", playlist.title)
    print("no of videos:", playlist.length)
    video = playlist.video_urls
    for i in video:
        print("".center(50, "-"))
        vid(i,path)

def music(s):
    video = YouTube(s)
    path = "./"+video.title+"/"
    os.makedirs(path)
    print("title of video:", video.title)
    print("length of video:", format(video.length/60, ".2f"), "minutes")
    print("no of views:", video.views)
    audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()
    audio.download(path)

def music_plst(s):
    playlist = pl.Playlist(s)

    path = "./"+playlist.title+"/"
    os.makedirs(path)
    print("title of playlist:", playlist.title)
    print("no of videos:", playlist.length)
    video = playlist.video_urls
    for i in video:
        print("".center(50, "-"))
        video = YouTube(i)
        print("title of video:", video.title)
        print("length of video:", format(video.length/60, ".2f"), "minutes")
        print("no of views:", video.views)
        audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()

        try:
            audio.download(path)
        except:
            pass
def table_print(dataframe: pandas.DataFrame):
    table = Table(title="list of videos")
    table.add_column("ID", justify="right", style="purple", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Length", justify="right", style="red", no_wrap=True)
    table.add_column("Link", justify="right", style="blue", no_wrap=True)
    for i in range(len(dataframe)):
        table.add_row(dataframe.loc[i,"ID"],dataframe.loc[i,"Title"],dataframe.loc[i,"Length"],dataframe.loc[i,"Link"])
    print(table)
vid_dict={'ID':[],"Title":[],"Length":[],"Link":[]}  
def get_vid_info(i):
    video = i
    vid_dict['ID'].append(str(video.video_id))
    vid_dict['Title'].append(str(video.title))
    vid_dict['Length'].append(str(format(video.length/60, ".2f")))
    vid_dict['Link'].append(f"[link={video.watch_url}]LINK[/link]")

@click.command()
@click.option("--search", help="search")
@click.option("--download_video", help="download video")
@click.option("--download_music", help="download music")

def main(search=None, download_video=None,download_music=None, info=None):
    downloads_folder="./video_downloaded"
    user=getpass.getuser()
    if search!=None:
        res=Search(search).results
        pool=ThreadPool(10)
        pool.map(get_vid_info,res)
        pool.close()
        pool.join()
        df=pandas.DataFrame(vid_dict)
        table_print(df)
    elif download_video!=None:
        link = download_video
        if ("list=" in link):
            plst(link)
            shutil.move(downloads_folder,f"/home/{user}/Downloads")
            print("finished".center(50, "-"))
        else:
            vid(link)
            shutil.move(downloads_folder,f"/home/{user}/Downloads")
            print("finished".center(50, "-"))
    elif download_music!=None:
        link = download_music
        if ("list=" in link):
            music_plst(link)
            shutil.move(downloads_folder,f"/home/{user}/Downloads")
            print("finished".center(50, "-"))
        else:
            music(link)
            shutil.move(downloads_folder,f"/home/{user}/Downloads")
            print("finished".center(50, "-"))

if __name__ == "__main__":
    main()
