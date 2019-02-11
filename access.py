#!/usr/bin/env python3

from threading import Thread
import os
import subprocess
import sys
import signal
import time

current_os = None
player_path = None
player_flags = "--video-on-top --no-video-title-show"
video_path = "assets/video.mp4"
failed_attempts = 0


# Thread object used to play the video
class VideoPlayer(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		time.sleep(3)
		subprocess.run(player_path + " " + player_flags + " " + video_path + " &> /dev/null", shell=True)


# Handles CTRL + C signal gracefully
def signal_handler(sig, frame):
	sys.exit(0)


# Makes sure that we are inside a supported OS, then configure local variables accordingly
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
	signal.signal(signal.SIGINT, signal_handler)


# Sets all paths to the right video player depending on the OS
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


# Execute sudo command with all the given parameters from the user
def execute_sudo():
	sudo_args = ""
	for arg in sys.argv[1:]:
		sudo_args += arg + " "
	result = subprocess.run("sudo " + sudo_args, shell=True)
	if result.returncode == 1:  # sudo has not completed successfully (i.e. wrong password given)
		global failed_attempts
		failed_attempts += 1


# Prints message on the terminal and starts the video player
def print_message():
	print("\naccess: PERMISSION DENIED.", end="")
	time.sleep(1)
	print("...and...")
	time.sleep(1)
	video_thread = VideoPlayer()
	video_thread.daemon = True
	video_thread.start()
	while True:
		print("YOU DIDN'T SAY THE MAGIC WORD!")
		time.sleep(0.05)


def main():
	configure_platform()
	set_path()
	execute_sudo()
	if failed_attempts > 0:
		print_message()


if __name__ == "__main__":
	main()
