# Youtube downloader

Copy/paste a youtube video in the GUI, click download!

![Youtube Downloader](./images/youtube-downloader-1.png)

![Youtube Downloader](./images/youtube-downloader-2.png)

![Youtube Downloader](./images/explorer.png)

## Run script

```python
python youtube-downloader.py
```

## Create standalone installer

```python
pyinstaller --onefile --windowed  youtube-downloader.py

pyinstaller --onefile --windowed --icon=favicon.ico youtube-downloader.py
```
