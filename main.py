import glob
import os
import flask
from flask import *
import keyboard
from subprocess import run
import pygame
import time

pygame.mixer.init()

app = Flask(__name__)

pauseState = False
volume = 0.5
pygame.mixer.music.set_volume(volume)


@app.route("/sp/<song>", methods=["GET", "POST"])
def songPreview(song):
    run("player.py " + song, shell=True)
    return jsonify({"result": 1})


@app.route("/play/<song>", methods=["GET", "POST"])
def play(song):
    global pauseState
    pauseState = False
    preview = request.args.get("p")
    if not preview:
        preview = 1
    else:
        preview = int(preview)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load("audio/" + song + ".mp3")
    pygame.mixer.music.play()
    if preview:
        run("player.py " + song, shell=True)
    return jsonify({"result": 1})


def adjust(fromVol, toVol):
    volTmp = fromVol
    step = 0.01
    if fromVol > toVol:
        step = -0.01
    for i in range(int(abs(fromVol - toVol) * 100)):
        volTmp += step
        time.sleep(0.01)
        pygame.mixer.music.set_volume(volTmp)


@app.route("/setvol", methods=["GET", "POST"])
def volChange():
    global volume
    vol = request.args.get("val")
    fade = request.args.get("fade")
    if not fade:
        fade = 0
    else:
        fade = int(fade)
    if fade:
        adjust(volume, int(vol) / 100)
    volume = int(vol) / 100
    pygame.mixer.music.set_volume(volume)
    return jsonify({"result": 1, "data": volume})


@app.route("/pause", methods=["GET", "POST"])
def pause():
    fade = request.args.get("fade")
    if not fade:
        fade = 0
    else:
        fade = int(fade)
    global pauseState
    if pauseState:
        pygame.mixer.music.unpause()
        if fade:
            adjust(0, volume)
        pygame.mixer.music.set_volume(volume)
        pauseState = False
        return jsonify({"result": 1, "data": 0})
    else:
        if fade:
            adjust(volume, 0)
        pygame.mixer.music.pause()
        pauseState = True
        return jsonify({"result": 1, "data": 1})


@app.route("/key")
def pressKey():
    key = request.args.get("key")
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)
    return jsonify({"result": 1, "data": key})


@app.route("/")
def index():
    dirs = glob.glob("audio/*.mp3")
    for i in range(len(dirs)):
        dirs[i] = dirs[i].replace("audio\\", "").replace(".mp3", "")
    return render_template("index.html", dirs=dirs, vol=volume * 100, pause=pauseState)


if __name__ == "__main__":
    audios = glob.glob("audio/*.mp3")
    for i in audios:
        new = "anim/" + i.split("\\")[-1].replace(".mp3", "")
        if not os.path.exists(new):
            print("anim", i, "- Not Found.", new, end=" ")
    print("Loaded", len(audios), "audio(s).")
    app.run(host="0.0.0.0", port=1145, debug=True, threaded=True)
