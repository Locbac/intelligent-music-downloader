from argparse import ArgumentParser, Namespace
import argparse
import subprocess
import re

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
parser.add_argument("user_input", help="Song search term, URL, etc.")
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

    # General URL
    url_pattern = r"https?://(?:www\.)?\w+\.\w+(/\S*)?"
    if re.match(url_pattern, user_input):
        return "General URL"

    # Search term
    return "Search Term"


user_input = args.user_input
input_type = check_input(user_input)


def main():
    if input_type == "Spotify URL":
        command = [spotdl_path, user_input]
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
            "--audio-format",
            "mp3",
            user_input,
        ]

        run_command_no(command)

    else:
        which_tool = input(
            "No URL was provided, which tool do you want to search for a song with? (spotdl, ytdlp)?: "
        )
        if which_tool == "spotdl":
            command = [spotdl_path, user_input]
            run_command_no(command)
        elif which_tool == "ytdlp":
            command = [
                ytdlp_path,
                "ytsearch10:" + user_input,
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
                    "mp3",
                    selected_video,
                ]
                run_command_no(command)
            else:
                print("Invalid selection.")


def run_command_no(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    # Read the output while the command is running
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip(), flush=True)

    # Get the remaining output
    remaining_output = process.communicate()[0]
    if remaining_output:
        print(remaining_output.strip())

    return process.returncode


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
        print(remaining_output.strip())

    return output, process.returncode


main()

