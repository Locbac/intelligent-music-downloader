from argparse import ArgumentParser, Namespace
import argparse
import subprocess
import re

parser = argparse.ArgumentParser()
parser.add_argument("user_input", help="Song search term, url, etc.")
args: Namespace = parser.parse_args()


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

    # General URl
    url_pattern = r"https?://(?:www\.)?\w+\.\w+(/\S*)?"
    if re.match(url_pattern, user_input):
        return "General URL"

    # Search term
    return "Search Term"


user_input = input_type = check_input(args.user_input)

if input_type == "Spotify URL":
    command = " ".join(["spotdl", user_input])
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    print(output)  # Print the output
elif input_type == "General URL":
    command = [
        "yt-dlp",
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
        "mp3",
        user_input,
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    print(output)  # Print the output
else:
    which_tool = input(
        "No URL was provided, which tool do you want to search for a song with? (spotdl,ytdlp)?: "
    )
    if which_tool == "spotdl":
        command = ["spotdl", user_input]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout
        print(output)  # Print the output
    elif which_tool == "ytdlp":
        command = ["yt-dlp", "ytsearch10:", user_input, "--get-id", "--get-title"]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()
        print(output)  # Print the output

        lines = output.split("\n")

        for i, line in enumerate(lines):
            print(f"{i+1}. {line}")
        selected_number = int(input("Which video do you want to download?: "))
        if 1 <= selected_number <= len(lines):
            selected_video = lines[selected_number - 1].split()[0]
            command = [
                "yt-dlp",
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
                "mp3",
                selected_video,
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            output = result.stdout
            print(output)  # Print the output
        else:
            print("Invalid selection.")

