import os
import subprocess
import threading
import time
import yaml

config = yaml.safe_load(open(os.path.dirname(os.path.abspath(__file__)) + "/config.yml"))
tmp_directory = os.path.dirname(os.path.abspath(__file__)) + "/tmp"
last_song_file_location = os.path.dirname(os.path.abspath(__file__)) + "/tmp/lastsong.txt"

def download_loop():
    while True:
        subprocess.run(["youtube-dl", "--no-overwrites", "--ignore-errors", "--extract-audio", "--audio-quality=0", "--audio-format=opus", "--yes-playlist", "--output", tmp_directory + "/%(playlist_index)s.%(ext)s", "--download-archive", tmp_directory + "/downloaded.txt", config["playlist_url"]])
        time.sleep(config["playlist_update_rate"])

def player_loop():
    time.sleep(10)
    # These conditions check if the song from the last session should be played.
    if config["restore_last_session"] is True:
        if os.path.isfile(last_song_file_location) is True:
            with open(last_song_file_location, 'r') as last_song_file: 
                counter = int(last_song_file.readline())
        else:
            counter = 1
    elif config["restore_last_session"] is False:
        counter = 1
    while True:
        # This checks if the download is finished.
        if os.path.isfile(tmp_directory + "/" + str(counter) + ".opus") is False:
            attempts = 0
            while attempts < 4 and os.path.isfile(tmp_directory + "/" + str(counter) + ".opus") is False:
                print("Looks like the download hasn't finished yet.")
                print("Sleeping for 5 seconds...")
                time.sleep(5)
                attempts += 1
        # This is just for checking if MPV should run with the GUI.
        if config["gui_enabled"] is True:
            command = ["mpv", tmp_directory + "/" + str(counter) + ".opus", "--player-operation-mode=pseudo-gui"]
        else:
            command = ["mpv", tmp_directory + "/" + str(counter) + ".opus", "--player-operation-mode=cplayer"]
        subprocess.run(command)
        counter += 1
        if config["restore_last_session"] is True:
            with open(last_song_file_location, 'w') as last_song_file:
                last_song_file.write(str(counter))

download_thread = threading.Thread(target=download_loop, args=())
player_thread = threading.Thread(target=player_loop, args=())

download_thread.start()
player_thread.start()
