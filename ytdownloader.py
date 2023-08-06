from pytube import YouTube, Search
import pytube.contrib.playlist as pl
import sys
import os
import moviepy.editor as mp


def vid(s):

    video = YouTube(s)
    print(video)
    global path
    path = "./"+video.title+"/"
    os.makedirs(path)
    print("title of video:", video.title)
    print("length of video:", format(video.length/60, ".2f"), "minutes")
    print("no of views:", video.views)
    video = video.streams.get_highest_resolution()
    video.download(path)


def plst(s):
    playlist = pl.Playlist(s)
    global path
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
        video = video.streams.get_highest_resolution()
        try:
            video.download(path)
        except:
            pass

def music(path):
    os.mkdir("./songs")
    for i in os.listdir(path):
        clip = mp.VideoFileClip(f'{path}/{i}')
        i=i.replace(".mp4",".mp3")
        clip.audio.write_audiofile(f'./songs/{i}')



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
            print("finished".center(50, "-"))
        else:
            vid(link)
            print("finished".center(50, "-"))
    elif sys.argv[1]=="-m":
        link = input("enter link of music plst:")
        if ("list=" in link):
            plst(link)
            music(path)
            print("finished".center(50, "-"))
        else:
            vid(link)
            music(path)
            print("finished".center(50, "-"))
        


if __name__ == "__main__":
    main()
