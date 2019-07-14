import os
import vlc
import threading
import time
import random
from flask import session

lock = threading.Lock()
thread_resource = threading.Condition(lock)

_song = vlc.MediaPlayer()

playing = None
is_paused = False;

songs = []
def fetch_songs ():
    songs.clear()
    def iter_dir (dir):
        for item in os.listdir (dir):
            t_path = os.path.join (dir, item)
            if os.path.isfile (t_path) or os.path.islink (t_path):
                songs.append (t_path)
            # else:
                # iter_dir (t_path)

    iter_dir (os.path.join (os.getenv ('HOME'), 'Music'))
    iter_dir (os.path.join (os.getenv ('HOME'), 'Music/olds'))
    songs.sort()
    return songs

def write_to_log (song):
    with open ('/tmp/music.log', 'at') as f:
        f.write (song + '\n')


def play_song(song):
    global _song, playing, is_paused
    lock.acquire()
    _song.stop()
    _song = vlc.MediaPlayer (song)
    playing = song.split('/')[-1]
    is_paused = False       # In case Pause Button is pressed First on the SERVER
    _song.play()
    lock.release()
    write_to_log (song)


def currently_playing():
    return playing if playing is not None else "Not Playing"

def pause(thread):
    global _song, is_paused, thread_resource
    is_paused = not is_paused
    # thread.notify()
    with thread_resource:
        thread_resource.notify()
    _song.pause();

def resume(thread):
    global _song, is_paused, thread_resource
    is_paused = not is_paused
    # thread.notify()
    with thread_resource:
        thread_resource.notfy()
    _song.play()

def next():
    # Play the next song
    """ What i am doing is just stopping the Current Music in Play, 
        so my another thread would automatically pick up that music is not in play, 
        so it will play the next song itself 
    """
    global _song;
    _song.stop();


# Demon Thread to continue the playback after the currently playing song stops as usual
class MyThread (threading.Thread):
    def __init__(self):
        super().__init__()
        print("Thread has started");

    def run(self):
        while True:
            global _song, is_paused, thread_resource
            time.sleep(1)
            print (f"Is Playing ?: {_song.is_playing() == 1} \t Is Paused ?: {is_paused}")
            # print (_song.is_playing() == 0, is_paused)

            if is_paused:
                with thread_resource:
                    thread_resource.wait()

            # if (_song.is_playing() == 0):
            if not _song.is_playing():
                time.sleep(0.25)
                play_song (random.choice (songs))
                # _song.stop()
                # del _song
                # _song = vlc.MediaPlayer (random.choice(songs))
                # _song.play()
            # time.sleep(1)



######################################################
# For Making folder based songs access
######################################################

def fetch_folders(dirs = None, include_files = False):
    folders = []
    files = []
    def iter_dir (dir):
        for item in os.listdir (dir):
            t_path = os.path.join (dir, item)
            if os.path.isdir (t_path):
                folders.append (t_path)
            if include_files and os.path.isfile (t_path):
                files.append (t_path)

    if not dirs:
        iter_dir (os.path.join (os.getenv ("HOME"), "Music/Albums/"))
    else:
        iter_dir (dirs)

    return folders if not include_files else (folders, files)
