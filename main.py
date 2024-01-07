from argparse import ArgumentParser, Namespace
import subprocess
import re


def search_spotdl(search_term):
    command = ['spotdl', search_term]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout

    # Find url
    match = re.search(r'https?://[^\s/$.?#].[^\s]*', output)
    if match:
        return match.group(0)

    return None

def download_music(url):
    command = ['yt-dlp', '-f', '251/140/bestaudio', '--embed-thumbnail', '--add-metadata', '-o', "%(title)s.%(ext)s", '-ciw', '-x', '--audio-quality', '0', '--audio-format', 'mp3', url]
    subprocess.run(command)

def main():
    parser = ArgumentParser()
    parser.add_argument("search_term", help="Song name, url, playlist url, etc.")
    args: Namespace = parser.parse_args()

    # spot search
    song_url = search_spotdl(search_term)

    if song_url is None:
        print('Song found on Spotify:)
        user_input = input('Is this the correct song? (y/n): ')
        if user_input.lower() == 'y':
            download_music(song_url)
        else:
            print('Trying with yt-dlp...')
            download_music(search_term)

if __name__ == '__main__':
    main()
