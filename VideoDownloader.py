from pytubefix import YouTube, Playlist
from pytubefix.exceptions import MembersOnly
import ffmpeg
import os, shutil
import zipfile


def Download(link="https://www.youtube.com/watch?v=OpelfZhK2N8",resolution="worst", bitrate="worst", save_path = "videos"):

    #SAVE_PATH = "videos" #where it saves

    #link = "https://www.youtube.com/watch?v=OpelfZhK2N8"

    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    temp_path = save_path + "/temp"
    if not os.path.isdir(temp_path):
        os.mkdir(temp_path)

    if "playlist?list" in link:
        try:
            pl = Playlist(link) #load playlist
        except:
            print("YouTube Connection Error!!!") #to handle exception
            return ["Can't Connect to YouTube!!! Please try again."]
        
        zip_path = temp_path + "/files-to-zip"
        if not os.path.isdir(zip_path):
            os.mkdir(zip_path)

        playlist_name = pl.title
        filenames = []

        for yt in pl.videos:
            try:
                video = getVideo(yt, resolution)
                audio = getAudio(yt, bitrate)
                file_name = video.title

                video.download(output_path=temp_path,filename=file_name + '-video.mp4')
                audio.download(output_path=temp_path,filename=file_name + '-audio.mp4')
                print('downloaded ' + file_name + '.mp4')

                input_video = ffmpeg.input(f"{temp_path}/{file_name}-video.mp4")
                input_audio = ffmpeg.input(f"{temp_path}/{file_name}-audio.mp4")
                output_file = f"{zip_path}/{file_name}.mp4"

                ffmpeg.output(input_video, input_audio, output_file, vcodec="copy", acodec="copy").run(overwrite_output=True)

                filenames.append(output_file)
            except ffmpeg.Error as e:
                print(f"Error merging audio and video files for {file_name}!!!")
                return [f"Error merging audio and video files for {file_name}!!! Please try again."]
            except FileNotFoundError:
                print("Error: ffmpeg not found. Ensure ffmpeg is installed and in your system's PATH.")
                return ["Unknown ffmpeg Error!?!?!"]
            except MembersOnly:
                print(f"Can't download members only videos!!!")
                return [f"Unable to download. {video.title} is a members only video!!!"]
            except:
                print("Some Error!")
                return ["Unknown Error!?!?!"]
            
        zip_file_name = f"{playlist_name}.zip"
        zip_file_path = f"{save_path}/{zip_file_name}"

        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip:
                for file in filenames:
                    if os.path.exists(file):
                        zip.write(file, os.path.basename(file)) # Add the file to the ZIP archive
                        print(f"Added {file} to {zip_file_name}")
                    else:
                        print(f"Error: {file} not found.")

            print(f"\nSuccessfully created {zip_file_name}")

        except Exception as e:
            print("Failed to make zip!!!")
            return("Failed to make a zip file for your playlist!!!")

            
        shutil.rmtree(temp_path)

        print('Task Completed!')
        return [zip_file_path, zip_file_name]

    else:
        try:
            yt = YouTube(link) #load video
        except:
            print("YouTube Connection Error!!!") #to handle exception
            return ["Can't Connect to YouTube!!! Please try again."]

        try:
            video = getVideo(yt, resolution)
            audio = getAudio(yt, bitrate)

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
        except MembersOnly:
                print(f"Can't download members only videos!!!")
                return [f"Unable to download. {video.title} is a members only video!!!"]
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


def AudioDownload(link="https://www.youtube.com/watch?v=OpelfZhK2N8", bitrate = "worst", save_path="temp-folder"):
    #link = "https://www.youtube.com/playlist?list=PL5H87eryjA0B5vi_nQA5fMXyk1QE_eRnz"

    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    if "playlist?list" in link:
        try:
            pl = Playlist(link) #load playlist
        except:
            print("YouTube Connection Error!!!") #to handle exception
            return ["Can't Connect to YouTube!!! Please try again."]
        
        zip_path = save_path + "/files-to-zip"
        if not os.path.isdir(zip_path):
            os.mkdir(zip_path)

        playlist_name = pl.title
        filenames = []

        for yt in pl.videos:
            try:
                audio = getAudio(yt, bitrate)
                file_name = audio.title

                audio.download(output_path=zip_path,filename=file_name + '.mp3')
                print('downloaded ' + file_name + '.mp3')

                filenames.append(f"{zip_path}/{file_name}.mp3")
            except MembersOnly:
                print(f"Can't download members only videos!!!")
                return [f"Unable to download. {audio.title} is a members only video!!!"]
            except:
                print("Some Error!")
                return ["Unknown Error!?!?!"]
            
        zip_file_name = f"{playlist_name}.zip"
        zip_file_path = f"{save_path}/{zip_file_name}"

        try:
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip:
                for file in filenames:
                    if os.path.exists(file):
                        zip.write(file, os.path.basename(file)) # Add the file to the ZIP archive
                        print(f"Added {file} to {zip_file_name}")
                    else:
                        print(f"Error: {file} not found.")

            print(f"\nSuccessfully created {zip_file_name}")

        except Exception as e:
            print("Failed to make zip!!!")
            return("Failed to make a zip file for your playlist!!!")

            
        shutil.rmtree(zip_path)

        print('Task Completed!')
        return [zip_file_path, zip_file_name]

    else:
        try:
            yt = YouTube(link) #load video
        except:
            print("YouTube Connection Error!!!") #to handle exception
            return ["Can't Connect to YouTube!!! Please try again."]

        try:
            audio = getAudio(yt, bitrate)
            file_name = audio.title + ".mp3"

            audio.download(output_path=save_path, filename=file_name) #downloads audio
        except MembersOnly:
                print(f"Can't download members only videos!!!")
                return [f"Unable to download. {audio.title} is a members only video!!!"]
        except:
            print("Some Error!")
            return ["Unknown Error!?!?!"]

        print('Task Completed!')
        return [f"{save_path}/{file_name}", file_name]
    


def streamTest(link):
    yt = YouTube(link)
    print(yt.streams.filter(adaptive=True, file_extension='mp4', type='audio'))




#Download(save_path="working-files/test", resolution="720p", bitrate="best")
#streamTest("https://www.youtube.com/watch?v=zoq0tAKpLBI")
#streamTest("https://www.youtube.com/watch?v=OpelfZhK2N8")
