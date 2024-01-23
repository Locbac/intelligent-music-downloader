# IMD (Intelligent Music Downloader)
#### Video Demo:  https://youtu.be/itixvAOxhvY
#### Description: Downloads from spotify and other sources quickly.

## Main Functions
- Download:
  - Spotdl
  - Ytdlp

- Search:
  - Spotdl
  - Ytdlp


- How to use it:
```
$ py imd.py [URL (spotify or any site supported by ytdlp)]
$ py imd.py [Search Term]
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
