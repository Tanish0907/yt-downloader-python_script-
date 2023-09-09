from pytube import YouTube
import pytube.contrib.playlist as pl
import sys
import os
import ffmpeg
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor
global x
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
        exit()

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


# def search(s):
#     global x, lk
#     search = Search(s)
#     lk = []
#     x=0
#     for i in search.results:
#         lk.append(f"https://www.youtube.com/watch?v={i.video_id}")
#     l = len(lk)
#     if x > 0:
#         lk.clear()
#         search.get_next_results()
#         for i in search.results:
#             lk.append(f"https://www.youtube.com/watch?v={i.video_id}")
#         for i in range(0, l-1):
#             lk.pop(i)
#             # print("test",lk[i])
#         lk.pop()
#     count = 0
#     print("search results".center(50, "-"))
#     for i in lk:
#         try:
#             v = YouTube(i)
#             print(count, v.title)
#             count = count+1
#         except:
#             pass
#     print("done".center(50, "-"))

#     x = x+1


# def s2():
#     dall = input(
#         "press r to search or y to download all (AFTER SEARCHING!!)or n to exit or enter the number of video to download:")
#     if dall == "y":
#         for i in lk:
#             vid(i)
#             print("finished".center(50, "-"))
#         exit()
#     elif dall == "n":
#         exit()
#     elif dall == "r":
#         search(sys.argv[2])
#         s2()
#     else:
#         dall = int(dall)
#         vid(lk[dall])
#         print("finished".center(50, "-"))
#         exit()



def main():
    if sys.argv[1] == "-l":
        link = input("enter link of vid/plst:")
        if ("list=" in link):
            plst(link)
            print("finished".center(50, "-"))
        else:
            vid(link)
            
            print("finished".center(50, "-"))
    elif sys.argv[1]=="-m":
        link = input("enter link of music plst/vid:")
        if ("list=" in link):
            music_plst(link)
            print("finished".center(50, "-"))
        else:
            music(link)
            print("finished".center(50, "-"))
        


if __name__ == "__main__":
    main()
