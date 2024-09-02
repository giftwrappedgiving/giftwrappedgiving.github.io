import subprocess


def execute_command(command):
    print("execute command", command)
    result = subprocess.run(command)

    if result.returncode == 0:
        print("Successful! ", command)
    else:
        print("Failed: ", command)


def execute_commands(commands):
    for command in commands:
        execute_command(command)
