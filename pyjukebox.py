#!/usr/bin/env python

import os
import subprocess
import threading
import time
import yaml
import glob

config = yaml.safe_load(open(os.path.dirname(os.path.abspath(__file__)) + "/config.yml"))
tmp_directory = os.path.dirname(os.path.abspath(__file__)) + "/tmp"
last_song_file_location = tmp_directory + "/lastsong.txt"

def download_loop():
    while getattr(download_thread, "do_run", True):
        subprocess.run(["youtube-dl", "--no-overwrites", "--ignore-errors", "--extract-audio", "--audio-quality=0", "--audio-format=" + config["audio_format"], "--yes-playlist", "--output", tmp_directory + "/%(playlist_index)s.%(ext)s", "--download-archive", tmp_directory + "/downloaded.txt", config["playlist_url"]])
        time.sleep(config["playlist_update_rate"])

def player_loop():
    time.sleep(15)
    # These conditions check if the song from the last session should be played.
    if config["restore_last_session"] is True:
        if os.path.isfile(last_song_file_location) is True:
            with open(last_song_file_location, 'r') as last_song_file: 
                counter = int(last_song_file.readline())
        else:
            counter = 0
    elif config["restore_last_session"] is False:
        counter = 0
    while True:
        songs = sorted(glob.glob(tmp_directory + "/*." + config["audio_format"]))
        # This is just for checking if MPV should run with the GUI.
        if config["gui_enabled"] is True:
            try:
                command = ["mpv", songs[counter], "--player-operation-mode=pseudo-gui"]
            except IndexError:
                print("Playlist finished!")
                exit()
        else:
            try:
                command = ["mpv", songs[counter], "--player-operation-mode=cplayer"]
            except IndexError:
                print("Playlist finished!")
                exit()
        subprocess.run(command)
        counter += 1
        if config["restore_last_session"] is True:
            with open(last_song_file_location, 'w') as last_song_file:
                last_song_file.write(str(counter))

download_thread = threading.Thread(target=download_loop, args=())
player_thread = threading.Thread(target=player_loop, args=())

download_thread.start()
player_thread.start()

player_thread.join()
download_thread.do_run = False
download_thread.join()
