import subprocess


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )

    output = ""

    # Read the output while the command is running
    for line in process.stdout():
        line = line.strip()
        output += line + "\n"

    # Get the remaining output
    remaining_output = process.communicate()[0]
    if remaining_output:
        output += remaining_output.strip() + "\n"
        print(remaining_output.strip())

    return output, process.returncode


def main():
    command = ["A:\\bin\\MSYS2\\usr\\bin\\ls.exe"]
    output, return_code = run_command(command)
    print(output)
    print(return_code)


main()

