import tkinter
import customtkinter
from pytube import YouTube
import threading
import os

DOWNLOAD_FOLDER = "downloaded"

def startDownload():
    try:
        yt_link = link.get()
        print(yt_link)
        finishLabel.configure(text="Downloading...", text_color="white")
        yt = YouTube(yt_link, on_progress_callback=updateProgress)
        print(yt.title)
        print(yt.author)
        print(yt.thumbnail_url)
        title.configure(text=yt.title, text_color="white")
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=DOWNLOAD_FOLDER)
        finishLabel.configure(text="Finished Downloading", text_color="green")
    except Exception as e:
        print(e)
        if "unreachable" in str(e):
            finishLabel.configure(text="Error: YouTube Unreachable", text_color="red")
        elif "private" in str(e):
            finishLabel.configure(text="Error: Video is Private", text_color="red")
        else:
            finishLabel.configure(text="Error Downloading", text_color="red")


def updateProgress(stream, chunk, bytes_remaining):
    size = stream.filesize
    bytes_downloaded = size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / size) * 100
    print(progress.set(float(percentage_of_completion / 100)))
    progress.update()


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
# app.geometry("500x400")
app.title("YouTube Downloader")
app.minsize(500, 300)
app.columnconfigure(0, weight=1)

# title
title = customtkinter.CTkLabel(app, text="Insert YouTube Link", font=("Arial", 12))
title.grid(row=0, column=0, padx=10, pady=10, sticky="EW")

# link
url_var = customtkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.grid(row=1, column=0, padx=10, pady=10, sticky="EW")

# progress bar
progress = customtkinter.CTkProgressBar(app, width=350)
progress.set(0)
progress.grid(row=2, column=0, padx=10, pady=10, sticky="EW")

# button to download
download = customtkinter.CTkButton(app, text="Download", width=350, height=40, command=lambda: threading.Thread(target=startDownload).start())
download.grid(row=3, column=0, padx=10, pady=10, sticky="EW")



# finished downloading
finishLabel = customtkinter.CTkLabel(app, text="", font=("Arial", 20))
finishLabel.grid(row=4, column=0, padx=10, pady=10, sticky="EW")




# run app
app.mainloop()
