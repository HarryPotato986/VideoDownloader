from pytubefix import YouTube, Playlist
import ffmpeg


def Download(link="https://www.youtube.com/watch?v=OpelfZhK2N8",highResolution = False, SAVE_PATH = "videos"):

    #SAVE_PATH = "videos" #where it saves

    #link = "https://www.youtube.com/watch?v=OpelfZhK2N8"

    try:
        yt = YouTube(link) #load video
    except:
        print("Connection Error") #to handle exception
        return False

    if highResolution:
        #stream = yt.streams.get_highest_resolution() #chooses highest res it can get
        video = getBestVideo(yt)
        audio = getBestAudio(yt)
    else:
        stream = yt.streams.get_lowest_resolution() #chooses lowest res it can get

    try:
        video.download(output_path="working-files", filename="video.mp4") #downloads video
        audio.download(output_path="working-files", filename="audio.mp4") #downloads audio

        input_video = ffmpeg.input("working-files/video.mp4")
        input_audio = ffmpeg.input("working-files/audio.mp4")
        output_file = SAVE_PATH + "/" + video.title + ".mp4"

        ffmpeg.output(input_video, input_audio, output_file, vcodec="copy", acodec="copy").run(overwrite_output=True)

    except ffmpeg.Error as e:
        print("Fuck")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Ensure ffmpeg is installed and in your system's PATH.")

    except:
        print("Some Error!")
    print('Task Completed!')

    return True

def getBestVideo(yt):
    #yt = YouTube("https://www.youtube.com/watch?v=MPBVyqdBgLM")

    return yt.streams.filter(adaptive=True, file_extension='mp4', type='video')[0]

def getBestAudio(yt):
    #yt = YouTube("https://www.youtube.com/watch?v=MPBVyqdBgLM")

    return yt.streams.filter(adaptive=True, file_extension='mp4', type='audio')[-1]



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

        for yt in pl.videos:
            audio = getBestAudio(yt)
            filename = audio.title

            try:
                audio.download(output_path=SAVE_PATH,filename=filename + '.mp3')
                print('downloaded ' + filename + '.mp3')
            except:
                print("Some Error!")
                return None

            filenames.append(filename)

        print('Task Completed!')
        print('downloaded ' + playlist_name)
        return filenames

    else:
        try:
            yt = YouTube(link, 'WEB') #load yt
        except:
            print("Connection Error") #to handle exception
            return None

        audio = getBestAudio(yt) #chooses highest bitrate audio
        filename = audio.title

        try:
            audio.download(output_path=SAVE_PATH,filename=filename + '.mp3') #downloads file
        except:
            print("Some Error!")
            return None

        print('Task Completed!')
        print('downloaded ' + filename + '.mp3')
        return filename

#Download(highResolution=True)
#AudioDownload()

#getBestVideo(YouTube("https://www.youtube.com/watch?v=OpelfZhK2N8"))
getBestAudio(YouTube("https://www.youtube.com/watch?v=MPBVyqdBgLM"))