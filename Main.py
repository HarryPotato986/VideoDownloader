from tkinter import *
from tkinter import ttk, filedialog
from VideoDownloader import Download, AudioDownload

root = Tk()
root.title("YouTube Downloader")
#root.geometry("1280x720")
root.resizable(False,False)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=0)
root.columnconfigure(2, weight=1)
root.rowconfigure(2, weight=0)


def changeSaveLocation():
    folder_selected = filedialog.askdirectory()
    save_location.set(folder_selected)

def startDownload(downloadType, url, savePath):
    if url is not None:
        if downloadType == 'video':
            download = Download(url, True, savePath)
            if download is not None:
                outcome.set("Finished!")
                outcome_label.configure(foreground="green")
            else:
                outcome.set("Failed!")
                outcome_label.configure(foreground="red")
        elif downloadType == 'audio':
            download = AudioDownload(url, savePath)
            if download is not None:
                outcome.set("Finished!")
                outcome_label.configure(foreground="green")
            else:
                outcome.set("Failed!")
                outcome_label.configure(foreground="red")


ttk.Label(root, text="choose save location").grid(column=1, row=0, columnspan=2)
save_location = StringVar()
save_location_entry = ttk.Entry(root, width=100, textvariable=save_location).grid(column=1, row=1, columnspan=2)
ttk.Button(root, text='Browse', command=lambda: changeSaveLocation()).grid(column=3, row=1)

ttk.Label(root, text="paste url").grid(column=1, row=2, columnspan=2)
link = StringVar()
link_entry = ttk.Entry(root, width=100, textvariable=link).grid(column=1, row=3, columnspan=2)

download_type = StringVar()
video = ttk.Radiobutton(root, text='video', variable=download_type, value='video').grid(column=1, row=4, sticky=E)
audio = ttk.Radiobutton(root, text='audio', variable=download_type, value='audio').grid(column=2, row=4, sticky=W)

ttk.Button(root, text='Download', command=lambda: startDownload(download_type.get(),link.get(),save_location.get())).grid(column=1, row=5, columnspan=2)

outcome = StringVar()
outcome_label = ttk.Label(root, textvariable=outcome)
outcome_label.grid(column=1, row=6, columnspan=2)




for child in root.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()


