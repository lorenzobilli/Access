#!/usr/bin/env python3

import os
import subprocess
import sys
import time

current_os = None
player_path = None
player_flags = "--video-on-top --no-video-title-show"
video_path = "assets/video.mp4"
failed = 0


# Make sure that we are inside a supported OS, then configure local variables accordingly
def configure_platform():
	global current_os
	if sys.platform.startswith("win32"):
		print("Access doesn't support Windows as a standard Python program. Please use WSL to execute this program.")
		exit(1)
	elif sys.platform.startswith("darwin"):
		current_os = "macos"
	elif sys.platform.startswith("linux"):
		check_wsl = os.uname()
		if check_wsl[2].__contains__("Microsoft"):      # Check if we are inside a WSL instance
			current_os = "windows"
		else:
			current_os = "linux"
	else:
		print("Unsupported OS")
		exit(1)


def set_path():
	global player_path
	if current_os == "windows":
		player_path = "/mnt/c/Program\\ Files/VideoLAN/VLC/vlc.exe"
	elif current_os == "macos":
		player_path = "vlc"
	elif current_os == "linux":
		player_path = ""
	else:
		print("Unable to set path for an unknown OS")


def execute_sudo():
	sudo_args = ""
	for arg in sys.argv[1:]:
		sudo_args += arg + " "
	result = subprocess.run("sudo " + sudo_args, shell=True)
	if result.returncode == 1:
		global failed
		failed += 1


def main():
	configure_platform()
	set_path()
	execute_sudo()
	if failed > 0:
		quantity = 200
		print("\nPERMISSION DENIED...and.....")
		time.sleep(1)
		while quantity != 0:
			print("YOU DIDN'T SAY THE MAGIC WORD!")
			time.sleep(0.01)
			quantity -= 1
		subprocess.run(player_path + " " + player_flags + " " + video_path + " &> /dev/null", shell=True)


if __name__ == "__main__":
	main()
