from pytube import YouTube, Search
import pytube.contrib.playlist as pl
import sys
import os
import moviepy.editor as mp
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

global path

def combine(vid_path,audio_path):
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
        video_clip = VideoFileClip(vids[i])
        audio_clip = AudioFileClip(audio[i])
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(vids[i] + ".mp4")	
        os.remove(vids[i])
        os.remove(audio[i])
    os.rmdir(path+".mp3")
    


def vid(s):

    video = YouTube(s)

    path = "./"+video.title+"/"
    os.makedirs(path)
    print("title of video:", video.title)
    print("length of video:", format(video.length/60, ".2f"), "minutes")
    print("no of views:", video.views)
    vid = video.streams.filter(res="1080p").first()
    audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()
    audio.download(path+".mp3")
    vid.download(path)


def plst(s):
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
        vid = video.streams.filter(res="1080p").first()
        audio=video.streams.filter(mime_type="audio/mp4",abr="128kbps").first()

        try:
            vid.download(path)
            audio.download(path+".mp3")
        except:
            pass

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


def search(s):
    global x, lk
    search = Search(s)
    lk = []

    for i in search.results:
        lk.append(f"https://www.youtube.com/watch?v={i.video_id}")
    l = len(lk)
    if x > 0:
        lk.clear()
        search.get_next_results()
        for i in search.results:
            lk.append(f"https://www.youtube.com/watch?v={i.video_id}")
        for i in range(0, l-1):
            lk.pop(i)
            # print("test",lk[i])
        lk.pop()
    count = 0
    print("search results".center(50, "-"))
    for i in lk:
        try:
            v = YouTube(i)
            print(count, v.title)
            count = count+1
        except:
            pass
    print("done".center(50, "-"))

    x = x+1


def s2():
    dall = input(
        "press r to search or y to download all (AFTER SEARCHING!!)or n to exit or enter the number of video to download:")
    if dall == "y":
        for i in lk:
            vid(i)
            print("finished".center(50, "-"))
        exit()
    elif dall == "n":
        exit()
    elif dall == "r":
        search(sys.argv[2])
        s2()
    else:
        dall = int(dall)
        vid(lk[dall])
        print("finished".center(50, "-"))
        exit()


def main():
    global x
    x = 0
    if sys.argv[1] == "-s":

        s2()
    elif sys.argv[1] == "-l":
        link = input("enter link of vid/plst:")
        if ("list=" in link):
            plst(link)
            combine(path,path+".mp3")
            print("finished".center(50, "-"))
        else:
            vid(link)
            combine(path,path+".mp3")
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
