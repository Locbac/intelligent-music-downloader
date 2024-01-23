import argparse
from os import write
import re
import subprocess
import sys
from argparse import ArgumentParser, Namespace

###############################################
#
#
#
#           CONFIGGGGGGGGGGG
#
#
#
#
#
###############################################


#### Replace the \ with \\ in path names

spotdl_path = "A:\\Apps\\Programs\\Python\\Python312\\Scripts\\spotdl.exe"
ytdlp_path = "A:\\Apps\\Programs\\Python\\Python312\\Scripts\\yt-dlp.exe"


###############################################

parser = argparse.ArgumentParser()
parser.add_argument(
    "user_input",
    nargs="+",
    help="Song search term, URL, etc.",
)
parser.add_argument(
    "--format",
    "-f",
    choices=["mp3", "wav", "ogg", "m4a"],
    default="mp3",
    help="Output format",
)
parser.add_argument(
    "--link",
    "-wl",
    action="store_true",
    dest="wl",
    help="Creates a link to the original downloaded song with yt-dlp",
)
parser.add_argument(
    "--ext-dl",
    "-ed",
    action="store_true",
    dest="ed",
    help="Uses an external downloader, aria2c",
)
args = parser.parse_args()


def check_input(user_input):
    pattern1 = r"https://open\.spotify\.com/.*"
    pattern2 = r"open\.spotify\.com/.*"
    pattern3 = r"spotify\.com/.*"

    if (
        re.match(pattern1, user_input)
        or re.match(pattern2, user_input)
        or re.match(pattern3, user_input)
    ):
        return "Spotify URL"

    # General URL
    url_pattern = r"https?://(?:www\.)?\w+\.\w+(/\S*)?"
    if re.match(url_pattern, user_input):
        return "General URL"

    # Search term
    return "Search Term"


user_input = args.user_input
# input_type = check_input(user_input)


def multi_url(user_input):
    return len(user_input.split()) > 1


def main():
    # urls = user_input.split()
    # if multi_url(user_input):
    #     for url in urls:
    #         download_url(url)
    # else:
    #     download_url(user_input)
    # print(f"{user_input}")
    for url in user_input:
        download_url(url)


def run_command_no(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
    )

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip(), flush=True)

    rc = process.poll()

    return rc


def run_command_wo(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    output = ""

    # Read the output while the command is running
    for line in process.stdout:
        line = line.strip()
        output += line + "\n"

    # Get the remaining output
    remaining_output = process.communicate()[0]
    if remaining_output:
        output += remaining_output.strip() + "\n"
        print(remaining_output.strip(), flush=True)

    return output, process.returncode


def download_url(url):
    input_type = check_input(url)
    format = args.format
    # writelink = args.link or args.wl
    writelink = args.wl
    extdl = args.ed
    if input_type == "Spotify URL":
        command = [spotdl_path, url]
        run_command_no(command)

    elif input_type == "General URL":
        command = [
            ytdlp_path,
            "-f",
            "251/140/bestaudio",
            "--embed-thumbnail",
            "--add-metadata",
            "-o",
            "%(title)s.%(ext)s",
            "-ciw",
            "-x",
            "--audio-quality",
            "0",
            "--write-link",
            "--audio-format",
            format,
            url,
        ]
        if writelink:
            command.extend(["--write-link"])
        if extdl:
            command.extend(
                [
                    "--external-downloader",
                    "aria2c",
                    "--external-downloader-args",
                    "-x 16 -s 16",
                ]
            )

        run_command_no(command)

    else:
        while True:
            which_tool = input(
                "No URL was provided, which tool do you want to search for a song with? (spotdl, ytdlp)?: "
            )
            if which_tool is None:
                continue
            elif which_tool == "spotdl":
                break
            elif which_tool == "ytdlp":
                break
            else:
                continue
        if which_tool == "spotdl":
            command = [spotdl_path, url]
            run_command_no(command)
        elif which_tool == "ytdlp":
            command = [
                ytdlp_path,
                "ytsearch10:" + url,
                "--get-id",
                "--get-title",
            ]

            output, return_code = run_command_wo(command)

            lines = output.split("\n")

            for i, line in enumerate(lines):
                print(f"{i+1}. {line}")
            selected_number = int(input("Which video do you want to download?: "))
            if 1 <= selected_number <= len(lines):
                selected_video = lines[selected_number - 1].split()[0]
                command = [
                    ytdlp_path,
                    "-f",
                    "251/140/bestaudio",
                    "--embed-thumbnail",
                    "--add-metadata",
                    "-o",
                    "%(title)s.%(ext)s",
                    "-ciw",
                    "-x",
                    "--audio-quality",
                    "0",
                    "--audio-format",
                    format,
                    selected_video,
                ]
                run_command_no(command)
            else:
                print("Invalid selection.")


main()

