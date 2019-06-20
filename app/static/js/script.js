function AjaxCall (song)
{
    document.getElementById ('currently_playing_song').innerHTML = song.split('/')[song.split('/').length - 1];

    $.ajax({
        url: 'play',
        data: {'file': song},
        type: "POST",
        success: function () { console.log ("Success: " + "Now Playing:" + song); },
        error: function () { console.log ("Not Sent Error"); }
    });
}

function PauseMusic ()
{
    var btn = document.getElementById ('pause');
    btn.innerHTML = "PLAY";
    btn.onclick = ResumeMusic;
    btn.id = "resume";

    $.ajax ({
        url: 'pause',
        type: 'POST',
        success: function () { console.log ("Song paused"); },
        error: function () { console.log ("[ERROR]: Song can't be paused"); }
    });
}

function ResumeMusic ()
{
    var btn = document.getElementById ('resume');
    btn.innerHTML = "PAUSE";
    btn.onclick = PauseMusic;
    btn.id = "pause";

    $.ajax ({
        url: 'resume',
        type: 'POST',
        success: function () { console.log ("Song Resumed"); },
        error: function () { console.log ("[ERROR]: Song can't be resumed"); }
    });
}

function NextMusic ()
{
    $.ajax ({
        url: 'next',
        type: 'POST',
        success: function () { console.log ("Next Song to be played"); },
        error: function () { console.log ("[ERROR]: Next Song thing"); }
    });
}
