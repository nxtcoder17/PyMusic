import os
import vlc
import threading
import time
import random
from flask import session

lock = threading.Lock()
_song = vlc.MediaPlayer()

playing = None
is_paused = False;

songs = []
def fetch_songs ():
    songs.clear()
    def iter_dir (dir):
        for item in os.listdir (dir):
            t_path = os.path.join (dir, item)
            if os.path.isfile (t_path):
                songs.append (t_path)
            # else:
                # iter_dir (t_path)

    iter_dir (os.path.join (os.getenv ('HOME'), 'Music'))
    iter_dir (os.path.join (os.getenv ('HOME'), 'Music/olds'))
    return songs

def write_to_log (song):
    with open ('/tmp/music.log', 'at') as f:
        f.write (song + '\n')


def play_song(song):
    global _song, playing
    lock.acquire()
    _song.stop()
    _song = vlc.MediaPlayer (song)
    playing = song.split('/')[-1]
    _song.play()
    lock.release()
    write_to_log (song)


def currently_playing():
    return playing if playing is not None else "Not Playing"

def pause():
    global _song, is_paused
    is_paused = not is_paused
    _song.pause();

def resume():
    global _song, is_paused
    is_paused = not is_paused
    _song.play()


# Demon Thread to continue the playback after the currently playing song stops as usual
class MyThread (threading.Thread):
    def __init__(self):
        super().__init__()
        print("Thread has started");

    def run(self):
        while True:
            global _song, is_paused
            time.sleep(1)
            print (_song.is_playing() == 0, is_paused)
            if (_song.is_playing() == 0) and (is_paused == False):
                play_song (random.choice (songs))
                # _song.stop()
                # del _song
                # _song = vlc.MediaPlayer (random.choice(songs))
                # _song.play()
            # time.sleep(1)



######################################################
# For Making folder based songs access
######################################################

def fetch_folders(dirs = None, files = False):
    folders = []
    def iter_dir (dir):
        for item in os.listdir (dir):
            t_path = os.path.join (dir, item)
            if os.path.isdir (t_path):
                folders.append (t_path)
            if files and os.path.isfile (t_path):
                folders.append (t_path)

    if not dirs:
        iter_dir (os.path.join (os.getenv ("HOME"), "Music/Albums/Artists"))
    else:
        iter_dir (dirs)

    return folders;
