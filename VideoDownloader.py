from pytube import YouTube


def Download(link="https://www.youtube.com/watch?v=OpelfZhK2N8", highResolution=False, savePath="videos"):

    SAVE_PATH = savePath #where it saves

    #link = "https://www.youtube.com/watch?v=OpelfZhK2N8"

    try:
        yt = YouTube(link) #load video
    except:
        print("Connection Error") #to handle exception
        return None

    if highResolution:
        d_video = yt.streams.get_highest_resolution() #chooses highest res it can get
    else:
        d_video = yt.streams.get_lowest_resolution() #chooses lowest res it can get

    filename = d_video.title

    try:
        d_video.download(output_path=SAVE_PATH,filename=filename + '.mp4') #downloads file
    except:
        print("Some Error!")
        return None

    print('Task Completed!')
    print('downloaded ' + filename)
    return filename


def AudioDownload(link="https://www.youtube.com/watch?v=OpelfZhK2N8", savePath="audios"):

    SAVE_PATH = savePath #where it saves

    #link = "https://www.youtube.com/watch?v=OpelfZhK2N8"

    try:
        yt = YouTube(link) #load video
    except:
        print("Connection Error") #to handle exception
        return None

    d_video = yt.streams.get_audio_only() #chooses highest bitrate audio
    filename = d_video.title

    try:
        d_video.download(output_path=SAVE_PATH,filename=filename + '.mp3') #downloads file
    except:
        print("Some Error!")
        return None

    print('Task Completed!')
    print('downloaded ' + filename)
    return filename

#Download(highResolution=True)
#AudioDownload()
