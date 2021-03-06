# pyjukebox
This is a very quickly programmed script for downloading, playing and watching (like the command `watch`) a YouTube playlist.

## Requirements
1. `youtube-dl`
1. `mpv`
1. Some disk space
1. A working internet connection

## Usage
1. Create a YouTube playlist that you (and your friends) can edit
1. Paste the playlist URL to the config file
1. Start pyjukebox with `python pyjukebox.py`
1. Every time a new song is added to the playlist, pyjukebox will download it and play it.

## Controls
 - Songs can be skipped by closing the `mpv` window (or pressing `q` in console mode)
 - Program is terminated by pressing `Ctrl` + `C`

## Configuration
The configuration options are very simple.

`playlist_url` - This is the URL to your playlist.  
`playlist_update_rate` - How often we check for new songs (in seconds).  
`gui_enabled` - Should `mpv` show its GUI?  
`restore_last_session` - Remember what song was last played?  
`audio_format` - What audio format should be used for storing the songs. Most YT videos use `opus`, so using `opus` here usually avoids transcoding (thus saving some battery and lowering CPU usage).

## Other notes / known issues
 - The script gets confused when removing songs from the playlist. Please don't do that... (ノ_<。)
 - Don't delete the tmp directory. Please don't...
 - The tmp directory **has to be cleaned** each time you change the playlist.
 - There is a 15 second delay before attempting to play the first song. This is so that it works even on slow(er) machines and internet connections.