from flask import Flask
from flask import render_template, request, redirect
import os
import vlc
import time
import threading
import random

app = Flask (__name__)

song_path = os.path.join (os.getenv ('HOME'), 'Music')
songs_list = []
id = ""
first_request = False
playing = False
thread = None
lock = threading.Lock()

song = vlc.MediaPlayer()

def init ():
    def iter_dir (dir):
        for item in os.listdir(dir):
            abs_path = os.path.join (dir, item)
            if os.path.isfile (abs_path):
                songs_list.append (abs_path)
            # else:
                # iter_dir (abs_path)

    iter_dir (song_path)
    iter_dir ( os.path.join (song_path, 'olds'))

def write_log (song):
    with open ('/tmp/music.log', 'at') as file:
        file.write (song + '\n')


# A Thread that keeps a check on if no song is playing, 
#   then, play a random track
class MyThread (threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            global song
            time.sleep(1)
            if song.is_playing() == 0:
                # lock.acquire()

                song.pause()
                del song # To improve Memory Consumption

                # Randomly choose the next track to play
                song_next_to_play = random.choice (songs_list)
                write_log (song_next_to_play)
                song = vlc.MediaPlayer (os.path.join (song_path, song_next_to_play))
                song.play()

                # playing = True
                # lock.release()

@app.route ('/', methods=['GET'])
def index():
    global thread
    return render_template("index.html", songs_list = songs_list, timestamp=time.time(), id = id);

@app.route ('/', methods=['POST'])
def play_music():
    first_request = True
    global song, thread
    lock.acquire()

    song.stop()
    del song    # Reduces Memory Consumption by a huge margin
    selected_song = str(request.form ['song'])
    write_log (selected_song)
    song = vlc.MediaPlayer (os.path.join (song_path, selected_song));
    song.play()
    playing = True
    time.sleep (0.5)

    lock.release()
    if thread is None:
        thread = MyThread()
        thread.setDaemon (True)
        thread.start()
    return render_template(f"index.html", songs_list = songs_list, timestamp=int(time.time()), id = selected_song);


if __name__ == '__main__':
    init()      # Populating the Songs once and for all 
    app.run('0.0.0.0', '9999')
