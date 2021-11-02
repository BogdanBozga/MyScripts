#!/usr/bin/python3
import subprocess
import os
import sys
import datetime
import time
import pyglet




#--- set the process name to limit below
apps = {"steam","lutris"}
# app1 = "steam"
# app2 = "lutris"
dayChoose={
    "luni":False,
    "marti":"False",
    "miercuri":False,
    "joi":False,
    "vineri":{"hour":21,"minute":0},
    "sâmbătă":{"hour":17,"minute":0},
    "duminică":False
}

reminderTimeEye = 3600 # 1 hour
repetitionTime = 600 # 10 minutes
adviseTime = {"hour":22,"minutes":25} #time when "enough for today appear"

uselog = "/opt/limit/uselog"
datefile = "/opt/limit/currdate"

def center_on_screen(self):
    """Centers the window on the screen."""
    _left = SCREEN_WIDTH // 2 - self.width // 2
    _top = SCREEN_HEIGHT // 2 - self.height // 2
    self.set_location(_left, _top)
    
def accessDenied():
    os.system('spd-say "ACCESS DENIED"')
    time.sleep(1) # to make sure that the comand finish to say

def gif_suck():

    animation = pyglet.image.load_animation('/home/bozga/MyScripts/time_use/access-denied-pizza-steve.gif')
    animSprite = pyglet.sprite.Sprite(animation)
    w = animSprite.width
    h = animSprite.height
    window = pyglet.window.Window(width=w, height=h)
    r,g,b,alpha = 0.5,0.5,0.8,0.5

    _left = 1800 // 2
    _top = 800 // 2
    
    window.set_location(_left, _top)
    @window.event
    def on_draw():
        window.clear()
        animSprite.draw()
    pyglet.app.run()






def app_kill(app):
    try:
        # if the pid of the targeted process exists, add a "tick" to the used quantum
        pid = subprocess.check_output(["pgrep", app]).decode("utf-8").strip()
        if pid:
            if not dayChoose[time.strftime("%A")]:
                subprocess.Popen(["kill", pid.split("\n")[0]])
                accessDenied()
                gif_suck()
            elif datetime.datetime.now().hour < dayChoose[time.strftime("%A")]["hour"]:
                subprocess.Popen(["kill", pid.split("\n")[0]])
                accessDenied()
                gif_suck()
        open(uselog, "wt").write(app)
    except subprocess.CalledProcessError:
        pass
    except PermissionError:
        pass


def main():
    for app in apps:
        app_kill(app)

def eyeSound():
    os.system('spd-say "eye care first"')
    time.sleep(1) # to make sure that the comand finish to say


def enoughForTodaySound():
    os.system('spd-say "go to sleep"')
    time.sleep(1) # to make sure that the comand finish to say

def verifyTimeEye(addedTime):
    if(addedTime >= reminderTimeEye):
        eyeSound()
        addedTime = 0 
    return addedTime


def verifyTimeEnough(addedTime):
    currentTime = datetime.datetime.now()
    if(currentTime.hour==adviseTime["hour"] and currentTime.minute >= adviseTime["minutes"]):
        if currentTime.minute == adviseTime["minutes"]:
            enoughForTodaySound()
            addedTime = 0
        elif addedTime >= repetitionTime:
            enoughForTodaySound()
            addedTime = 0
    return addedTime


rAddTime = 0 
while True:
    time.sleep(10)
    rAddTime += 10
    main()
    rAddTime = verifyTimeEye(rAddTime)
    rAddTime = verifyTimeEnough(rAddTime)






# https://stackoverflow.com/questions/16573051/sound-alarm-when-code-finishes
# sudo apt install speech-dispatcher
# sudo apt install sox
# pip install piglet
