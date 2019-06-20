from app import app
from app import models
import time
from flask import render_template, request, send_file, url_for 
from app.models import MyThread

# Global variable that holds thread in execution
thread = None

@app.route ('/')
def index():
    return render_template ('index.html', songs = models.fetch_songs(),
                                timestamp = str(int(time.time())),
                                playing = models.currently_playing() )

# I need to start the Daemon Thread in this method, cause i only got it properly working in this situation
@app.route ('/play', methods=['POST'])
def receive_song():
    global thread
    if thread == None:
        thread = MyThread ()
        thread.setDaemon (True)
        thread.start()
    file = request.form['file']
    models.play_song (file)
    return ""

@app.route ('/pause', methods=['POST'])
def pause():
    models.pause(thread)
    return ""

@app.route ('/resume', methods = ['POST'])
def resume():
    models.resume(thread) 
    return ""

@app.route ('/next', methods=['POST'])
def next():
    models.next();
    return ""

@app.route ('/folder')
@app.route ('/folders')
def index_folders():
    return render_template ("folders.html", folders = models.fetch_folders());

@app.route ('/folder', methods=['POST'])
@app.route ('/folders', methods=['POST'])
def index_into_the_folder():
    path = request.form['path']
    return render_template ('folders.html', folders = models.fetch_folders (path, True));


@app.route ('/static/images/backdrop.jpg')
def return_backdrop ():
    return send_file ('./static/images/selena-1.jpg', mimetype='image/jpeg');

