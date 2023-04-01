from pytube import YouTube, Search
import pytube.contrib.playlist as pl
import sys
import os
import pandas as pd
link = sys.argv[1]


def vid(s):

    video = YouTube(s)
    path = "./"+video.title+"/"
    os.makedirs(path)
    print("title of video:", video.title)
    print("length of video:", format(video.length/60, ".2f"), "minutes")
    print("no of views:", video.views)
    video = video.streams.get_highest_resolution()
    video.download(path)


def plst(s):
    playlist = pl.Playlist(s)
    path = "./"+playlist.title+"/"
    os.makedirs(path)
    print("title of playlist:", playlist.title)
    print("no of videos:", playlist.length)
    print("no of views:", playlist.views)
    video = playlist.video_urls
    for i in video:
        print("".center(50, "-"))
        video = YouTube(i)
        print("title of video:", video.title)
        print("length of video:", format(video.length/60, ".2f"), "minutes")
        print("no of views:", video.views)
        video = video.streams.get_highest_resolution()
        video.download(path)


def search(s):
        search = Search(s)
        for i in range(1,6):
            search.results
            search.get_next_results()
        
        lk=[]
        print("search results".center(50,"-"))
        for i in search.results:
            lk.append(f"https://www.youtube.com/watch?v={i.video_id}")
        count=0
        for i in lk:
            try:
                v=YouTube(i)
                print(count,v.title)
                count=count+1
            except:
                pass
        print("done".center(50,"-"))
        return lk
def main(): 
    if sys.argv[1]=="-s":
        results=search(sys.argv[2])
        dall=input("do you want to download all the results(y/n) or enter the number of vid you want to download:")
        if dall=="y":
            for i in results:
                vid(i)
                print("finished".center(50,"-"))
            exit()
        elif dall=="n":
            exit()
        else:
            dall=int(dall)
            vid(results[dall])
            print("finished".center(50,"-"))
            exit()
    else:
        if ("list=" in link):
            plst(link)
            print("finished".center(50,"-"))
        else:
            vid(link)
            print("finished".center(50,"-"))
if __name__=="__main__":
    main()


