from pytubefix import YouTube, Playlist
import ffmpeg
import os


def Download(link="https://www.youtube.com/watch?v=OpelfZhK2N8",resolution="worst", bitrate="worst", save_path = "videos"):

    #SAVE_PATH = "videos" #where it saves

    #link = "https://www.youtube.com/watch?v=OpelfZhK2N8"

    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    temp_path = save_path + "/temp"
    if not os.path.isdir(temp_path):
        os.mkdir(temp_path)

    try:
        yt = YouTube(link) #load video
    except:
        print("YouTube Connection Error!!!") #to handle exception
        return ["Can't Connect to YouTube!!! Please try again."]

    video = getVideo(yt, resolution)
    audio = getAudio(yt, bitrate)

    try:
        video.download(output_path=temp_path, filename="video.mp4") #downloads video
        audio.download(output_path=temp_path, filename="audio.mp4") #downloads audio

        file_name = video.title + ".mp4"
        input_video = ffmpeg.input(temp_path + "/video.mp4")
        input_audio = ffmpeg.input(temp_path + "/audio.mp4")
        output_file = save_path + "/" + file_name

        ffmpeg.output(input_video, input_audio, output_file, vcodec="copy", acodec="copy").run(overwrite_output=True)

    except ffmpeg.Error as e:
        print("Error merging audio and video files!!!")
        return ["Error merging audio and video files!!! Please try again."]
    except FileNotFoundError:
        print("Error: ffmpeg not found. Ensure ffmpeg is installed and in your system's PATH.")
        return ["Unknown ffmpeg Error!?!?!"]

    except:
        print("Some Error!")
        return ["Unknown Error!?!?!"]
    
    os.remove(temp_path + "/video.mp4")
    os.remove(temp_path + "/audio.mp4")
    os.rmdir(temp_path)

    print('Task Completed!')
    return [output_file, file_name]

def getVideo(yt, res):
    if res == "best":
        streams = yt.streams.filter(adaptive=True, file_extension='mp4', type='video')
        if len(streams) > 0:
            return streams[0]
    elif res == "worst":
        streams = yt.streams.filter(adaptive=True, file_extension='mp4', type='video')
        if len(streams) > 0:
            return streams[-1]
    else:
        streams = yt.streams.filter(adaptive=True, file_extension='mp4', type='video', res=res)
        if len(streams) > 0:
            return streams[0]
        
    return None

def getAudio(yt, abr):
    if abr == "best":
        streams = yt.streams.filter(adaptive=True, file_extension='mp4', type='audio')
        if len(streams) > 0:
            return streams[-1]
    elif abr == "worst":
        streams = yt.streams.filter(adaptive=True, file_extension='mp4', type='audio')
        if len(streams) > 0:
            return streams[0]
    else:
        streams = yt.streams.filter(adaptive=True, file_extension='mp4', type='audio', abr=abr)
        if len(streams) > 0:
            return streams[0]
        
    return None


def AudioDownload(link="https://www.youtube.com/watch?v=OpelfZhK2N8", bitrate = "worst", save_path="C:/Users/gmeis/Downloads"):
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
            audio = getAudio(yt, bitrate)
            filename = audio.title

            try:
                audio.download(output_path=save_path,filename=filename + '.mp3')
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

        audio = getAudio(yt, bitrate) #chooses highest bitrate audio
        filename = audio.title

        try:
            audio.download(output_path=save_path,filename=filename + '.mp3') #downloads file
        except:
            print("Some Error!")
            return None

        print('Task Completed!')
        print('downloaded ' + filename + '.mp3')
        return filename



#Download(save_path="working-files/test", resolution="720p", bitrate="best")
