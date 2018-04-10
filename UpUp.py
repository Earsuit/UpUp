import timer
import threading
from pynput.keyboard import Key, Listener, KeyCode
from tkinter import *

def on_press(key):
    global mainThread
    global count_1
    global count_2
    global app

    if(key == app.muteHotKey[count_1]):
        count_1 += 1
    else:
        count_1 =0

    if(key == app.configHotKey[count_2]):
        count_2 += 1
    else:
        count_2 =0

    if(count_1 == len(app.muteHotKey)):
        mainThread.join(0.1)
        return False
    elif(count_2 == len(app.configHotKey)):
        app.config()
        count_2 = 0

def on_release(key):
    pass

app = timer.Timer()

mainThread = threading.Thread(name='daemon', target=app.mainLoop)
mainThread.setDaemon(True)
mainThread.start()

count_1 = 0
count_2 = 0

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
