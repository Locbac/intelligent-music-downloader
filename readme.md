# IMD (Intelligent Music Downloader)
#### Video Demo:  https://youtu.be/itixvAOxhvY
#### Description: Downloads from spotify and other sources quickly.


## Prerequisites
- Python3
  - https://www.python.org/downloads/
  - For windows: `winget install python.Python.3.12`
- SPOTDL V3.x
  - `pip install spotdl`
- YT-DLP
  - `pip install yt-dlp`


## Main Functions
- Download:
  - Spotdl
  - Ytdlp

- Search:
  - Spotdl
  - Ytdlp

- Format:
  - mp3
  - m4a
  - wav
  - ogg


- How to use it:
```
$ imd [URL (spotify or any site supported by ytdlp)] [format]
$ imd [Search Term] [format]
```
- Change the path of your spotdl and yt-dlp in main.py.
```python
#### Replace the \ with \\ in path names

spotdl_path = "A:\\Apps\\Programs\\Python\\Python312\\Scripts\\spotdl.exe"
ytdlp_path = "A:\\Apps\\Programs\\Python\\Python312\\Scripts\\yt-dlp.exe"

```

- Change the path of where main.py is located and add imd.bat to path in windows.
```batch
@echo off
setlocal
python "A:\Projects\Music Downloader\main.py" %*
```

## How it works
- It's a wrapper for spotdl and ytdlp to make it quicker to use, downloads metadata and album covers, as well as allows only one main command-line argument, from where it will go through and let you choose to search or to download and from where.

- If you input a spotify url, you will get the full functionality of spotdl with that one url.
  - Download:
    - Artists
    - Albums
    - Songs
    - Playlists

- If you input a URL other than spotify, it will download with yt-dlp with the best quality available, outputting to mp3 with the least compression possible (higher quality).
