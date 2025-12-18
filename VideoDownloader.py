from pytubefix import YouTube, Playlist


def Download(link="https://www.youtube.com/watch?v=OpelfZhK2N8",highResolution=False, SAVE_PATH = "videos"):

    #SAVE_PATH = "videos" #where it saves

    #link = "https://www.youtube.com/watch?v=OpelfZhK2N8"

    try:
        yt = YouTube(link) #load video
    except:
        print("Connection Error") #to handle exception

    if highResolution:
        d_video = yt.streams.get_highest_resolution() #chooses highest res it can get
    elif not highResolution:
        d_video = yt.streams.get_lowest_resolution() #chooses lowest res it can get

    try:
        d_video.download(output_path=SAVE_PATH) #downloads file
    except:
        print("Some Error!")
    print('Task Completed!')

    return True


def AudioDownload(link="https://www.youtube.com/watch?v=OpelfZhK2N8", savePath="C:/Users/gmeis/Downloads"):

    SAVE_PATH = savePath #where it saves

    #link = "https://www.youtube.com/playlist?list=PL5H87eryjA0B5vi_nQA5fMXyk1QE_eRnz"

    if "playlist?list" in link:
        try:
            pl = Playlist(link, 'WEB') #load playlist
        except:
            print("Connection Error") #to handle exception
            return None

        playlist_name = pl.title
        filenames = [playlist_name]

        for video in pl.videos:
            d_video = video.streams.get_audio_only()
            filename = d_video.title

            # checking if the file exists is slower than redownloading it
            # if not os.path.exists("audios/" + filename + ".mp4"):
            #     try:
            #         d_video.download(output_path=SAVE_PATH,filename=filename + '.mp4')
            #         print('downloaded ' + filename + '.mp4')
            #     except:
            #         print("Some Error!")
            #         return None
            # else:
            #     print(filename + '.mp4 already downloaded')

            try:
                d_video.download(output_path=SAVE_PATH,filename=filename + '.mp4')
                print('downloaded ' + filename + '.mp4')
            except:
                print("Some Error!")
                return None

            filenames.append(filename)

        print('Task Completed!')
        print('downloaded ' + playlist_name)
        return filenames

    else:
        try:
            yt = YouTube(link, 'WEB') #load video
        except:
            print("Connection Error") #to handle exception
            return None

        d_video = yt.streams.get_audio_only() #chooses highest bitrate audio
        filename = d_video.title

        # checking if the file exists is slower than redownloading it
        # if not os.path.exists("audios/" + filename + ".mp4"):
        #     try:
        #         d_video.download(output_path=SAVE_PATH,filename=filename + '.mp4') #downloads file
        #     except:
        #         print("Some Error!")
        #         return None
        # else:
        #     print(filename + '.mp4 already downloaded')

        try:
            d_video.download(output_path=SAVE_PATH,filename=filename + '.mp4') #downloads file
        except:
            print("Some Error!")
            return None

        print('Task Completed!')
        print('downloaded ' + filename + '.mp4')
        return filename

#Download(highResolution=True)
#AudioDownload()