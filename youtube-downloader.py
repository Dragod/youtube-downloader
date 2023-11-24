import tkinter
import customtkinter
from pytube import YouTube
import time
import os
import subprocess

prev_bytes_remaining = None
prev_time = None

def startDownload():
    # Call the cleanup function at the beginning of each download
    delete_old_videos()
    finished.configure(text="")
    progress_label.pack()
    progress.pack()
    speed_label.pack()

    global prev_bytes_remaining, prev_time
    prev_bytes_remaining = None
    prev_time = time.time()

    ytLink = url.get().strip()
    if not ytLink:
        speed_label.pack_forget()
        progress_label.pack_forget()
        progress.pack_forget()
        finished.configure(text="Please insert a YouTube video URL", text_color="red")
        return
    try:
        # Show progress bar and label before starting the download
        progress_label.pack()
        progress.pack()
        speed_label.pack()

        ytLink = url.get()
        ytObject = YouTube(ytLink, on_progress_callback=download_progress)
        ytStream = ytObject.streams.get_highest_resolution()

        finished.update()

        # Disable the input widget for the duration of the download
        url.configure(state='disabled')
        download.configure(state="disabled")

        # Locate system Downloads folder and create 'youtube-download' directory if does not already exist
        downloads_dir = os.path.join(os.path.expanduser("~"), 'Downloads')
        youtube_download_dir = os.path.join(downloads_dir, 'youtube-download')
        os.makedirs(youtube_download_dir, exist_ok=True)

        url_var.set('')

        # Convert the length in seconds to the format HH:MM:SS
        hours, remainder = divmod(ytObject.length, 3600)
        minutes, seconds = divmod(remainder, 60)
        video_length = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

        video_title.configure(text="Title", anchor="nw", font=("Arial", 18))
        video_title_var.configure(text=ytObject.title, anchor="nw", wraplength=340, justify="left")
        video_author.configure(text="Author", anchor="nw", font=("Arial", 18))
        video_author_var.configure(text=ytObject.author, anchor="nw")
        video_duration_title.configure(text="Length", anchor="nw", font=("Arial", 18))
        video_duration_var.configure(text=video_length, anchor="nw")

        ytStream.download(output_path=youtube_download_dir)

    except:
        finished.configure(text="Error downloading the video, please make sure it's a valid YouTube URL", text_color="red")
        return
    finally:

        download.configure(state="normal")
        url.configure(state='normal')

        # Hide progress bar and label after the download is finished
        speed_label.pack_forget()
        progress_label.pack_forget()
        progress.pack_forget()

def download_progress(stream, chunk, bytes_remaining):
    global prev_bytes_remaining, prev_time
    if prev_bytes_remaining is not None:
        # Calculate download speed in bytes per second
        delta_bytes = prev_bytes_remaining - bytes_remaining
        delta_time = time.time() - prev_time
        speed = delta_bytes / delta_time
        # Convert to MB
        speed = speed / (1024 * 1024)
        speed_label.configure(text = "{:.2f} MB/sec".format(speed), anchor="ne")
        speed_label.update()

    prev_bytes_remaining = bytes_remaining
    prev_time = time.time()

    totalSize = stream.filesize
    bytesDownloaded = totalSize - bytes_remaining
    percent = (bytesDownloaded / totalSize) * 100
    completion = str(int(percent))  # Convert to int to remove the decimal point
    progress_label.configure(text=completion + "%")
    progress.update()

    # Update the progress bar to show the current progress
    progress.set(float(percent) / 100)  # Divide by 100 to get a value between 0 and 1

def delete_old_videos():
    # path to the folder
    download_dir = os.path.join(os.path.expanduser("~"), 'Downloads', 'youtube-download')

    # current time minus 24 hours (time.time() returns time in seconds)
    time_24_hours_ago = time.time() - 24*60*60

    if os.path.exists(download_dir):
        for filename in os.listdir(download_dir):
            file = os.path.join(download_dir, filename)

            # if the video file has not been modified in the last 24 hours
            if os.path.getmtime(file) < time_24_hours_ago:
                os.remove(file)

def open_download_dir():
    # Locate system Downloads folder and create 'youtube-download' directory if does not already exist
    downloads_dir = os.path.join(os.path.expanduser("~"), 'Downloads')
    youtube_download_dir = os.path.join(downloads_dir, 'youtube-download')
    os.makedirs(youtube_download_dir, exist_ok=True)

    # Check OS to determine the command to use
    if os.name == 'nt':  # For windows
        os.startfile(youtube_download_dir)
    elif os.name == 'posix':  # For MacOS, Linux, and Unix
        subprocess.run(['open', youtube_download_dir])

def initialize_app():
    # Create global variables for widgets that need to be accessed outside this function
    global url, download, finished, progress_label, progress, speed_label, url_var, video_title, video_title_var, video_author, video_author_var, video_title_var, video_duration_title, video_duration_var

    # System settings
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    # App frame
    app = customtkinter.CTk()
    frame = tkinter.Frame(app)
    frame.pack(pady=10)
    WIDTH = 370
    HEIGHT = 450

    x = int((app.winfo_screenwidth() / 2) - (WIDTH / 2))
    y = int((app.winfo_screenheight() / 2) - (HEIGHT / 2))

    app.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
    #app.geometry("700x300")
    app.title("YouTube Downloader")
    app.iconbitmap("favicon.ico")

    url_var = tkinter.StringVar()

    # Add ui elements
    title = customtkinter.CTkLabel(app, text="Insert a YouTube video URL", font=("Arial", 16))
    title.pack(padx=10, pady=0, anchor="nw")

    # URL input
    url = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
    url.pack(padx=10, pady=0, anchor="nw")

    # Finished download label
    finished = customtkinter.CTkLabel(app, text="")
    finished.pack(padx=10, pady=0, anchor="nw")

    # Download button
    download = customtkinter.CTkButton(app, text="Download", command=startDownload)
    download.pack(padx=10, pady=10, anchor="nw")

    # Add the button to open the video download directory
    button = customtkinter.CTkButton(app, text="Open download directory", command=open_download_dir)
    button.place(x=170, y=120)
    # button.pack(padx=10, pady=5, anchor="nw")

    # Progress bar label
    progress_label = customtkinter.CTkLabel(app, text="0%")
    progress_label.pack(padx=10, pady=0, anchor="nw")

    # Progress bar
    progress = customtkinter.CTkProgressBar(app, width=350)
    progress.set(0)
    progress.pack(padx=10, pady=5, anchor="nw")

    # Add a label to show download speed
    speed_label = customtkinter.CTkLabel(app, text="0 MB/sec", anchor="ne")
    speed_label.pack(padx=10, pady=10, anchor="nw")

    # Add label for video title
    video_title = customtkinter.CTkLabel(app, text="Title", font=("Arial", 18))
    video_title.pack(padx=10, pady=0, anchor="nw")

    # Add label for video title var
    video_title_var = customtkinter.CTkLabel(app, text="--")
    video_title_var.pack(padx=10, pady=5, anchor="nw")

    # Add label for video author
    video_author = customtkinter.CTkLabel(app, text="Author", font=("Arial", 18))
    video_author.pack(padx=10, pady=0, anchor="nw")

    # Add label for video author var
    video_author_var = customtkinter.CTkLabel(app, text="--")
    video_author_var.pack(padx=10, pady=5, anchor="nw")

    # Add label for video duration title
    video_duration_title = customtkinter.CTkLabel(app, text="Length", font=("Arial", 18))
    video_duration_title.pack(padx=10, pady=0, anchor="nw")

    # Add label for video duration var
    video_duration_var = customtkinter.CTkLabel(app, text="--")
    video_duration_var.pack(padx=10, pady=5, anchor="nw")

    # Hide progress bar and label initially
    progress_label.pack_forget()
    progress.pack_forget()
    speed_label.pack_forget()

    # Run the app
    app.mainloop()

initialize_app()