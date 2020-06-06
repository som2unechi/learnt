import os
from tkinter import *
from threading import Thread
from tkinter import filedialog
from pygame import mixer
import time
from mutagen.mp3 import MP3
from PIL import ImageTk, Image
from tkinter import ttk
from ttkthemes import themed_tk as tk

#buttons
#play
#mute, unmute, play button, unmute,

#functions
#play
#pausea
#stop
#mute
#contdown
mixer.init()
root=tk.ThemedTk()
root.get_themes()
#root.configure(bg="black")
root.set_theme("plastik")

#-----------------------------------------------------------------------F U N C T I O N S----------------------------------------------------------

def files():
    global filename
    filename=filedialog.askopenfilename()
    Playlist()

playlib=[]

def play():
    global paused

    try:
        paused
    except NameError:
# testing git hub
        selectedsong=playlist.curselection()
        print(selectedsong)
        selectedsong=int(selectedsong[0])
        print(selectedsong)
        play_it = playlib[selectedsong]
        print(playlib)
        print(play_it)
        mixer.music.load(play_it)
        mixer.music.play()
        music_name=os.path.basename(play_it)
        status_bar.config(text=f"{music_name} is playing")
        paused=FALSE
        show_detail()

    else :
        mixer.music.unpause()
        status_bar.config(text="music is playing")
        show_detail()


def delete_action():
    selectedsong = playlist.curselection()
    selectedsong= int(selectedsong[0])
    playlist.delete(selectedsong)
    playlib.pop(selectedsong)


def Playlist():
    music_file=os.path.basename(filename)
    index=0
    playlist.insert(index, music_file)
    playlib.insert(index, filename)
    index+=1

def show_detail():

    filesname=os.path.splitext(filename)
    if filesname[1]==".mp3":
        audio=MP3(filename)
        total_length=audio.info.length
        min, sec= divmod(total_length, 60)
        min=round(min)
        sec=round(sec)
        music_time.config(text=f'0{min}:{sec}')
    else:
        a=mixer.Sound(filename)
        total_length=a.get_length()
        min, sec= divmod(total_length, 60)
        min=round(min)
        sec=round(sec)
        music_time.config(text=f"0{min}:{sec}")
    t1=Thread(target=countdown, args=(total_length,))
    t1.start()


def pause():
    global paused
    paused= True
    mixer.music.pause()
    status_bar.config(text="MUSIC IS PAUSED")


MUTE=FALSE


def mute():
    global MUTE
    if MUTE:
        mute_widget.config(image=unmute_photo)
        mixer.music.set_volume(0.6)
        MUTE=FALSE
    else:
        mute_widget.config(image=mute_photo)
        mixer.music.set_volume(0)
        MUTE=True


def stop():
    mixer.music.stop()
    status_bar.config(text="MUSIC STOPPED")


def countdown(t):
    while t and mixer.music.get_busy():
        if paused:
            pass
        else:
            min, sec=divmod(t , 60)
            min=round(min)
            sec=round(sec)
            time.sleep(1)
            t-=1
            print(min)
            music_time.config(text=f"0{min}:{sec}")


def set_vol(v):

    volume=float(v)/100
    mixer.music.set_volume(volume)


mute_photo=PhotoImage(file="mute.png")
play_photo=PhotoImage(file="play-button.png")
unmute_photo=PhotoImage(file="music-and-multimedia.png")
stop_button= PhotoImage(file="stop.png")
pause_button= PhotoImage(file="pause(1).png")


#---------------------------------------------------------------CREATING WIDGETS-------------------------------------------------------------------

status_bar=  ttk.Label(root, text ="music player", relief=SUNKEN, anchor=W)
status_bar.pack(side=BOTTOM,fill=X, pady=23)
Topframe= Frame(root,)
Topframe.pack()
leftframe=Frame(root)
leftframe.pack(side=LEFT)

Middleframe= Frame(root,)
Middleframe.pack()
bottomframe=Frame(root)
bottomframe.pack(side=BOTTOM)
playlist=Listbox(leftframe)

playlist.pack(side=TOP)
add_button=ttk.Button(leftframe, text="+add music", command=files)
add_button.pack(side=LEFT)
del_button=ttk.Button(leftframe, text="-delete", command=delete_action)
del_button.pack(side=LEFT)
menu=Menu(root)

root.config(menu=menu)
submenu= Menu(menu)
menu.add_cascade(label="file", menu=submenu)
submenu.add_command(label="open music", command=files)
menu.add_command(label="exit")


music_time= ttk.Label(Topframe, text="Music Time: --:--", font="Times 13 bold")
music_time.pack(pady=33)

play_widget= ttk.Button(Middleframe, image=play_photo, command= play)
play_widget.pack(side=LEFT, padx=5)

pause_widget=ttk.Button(Middleframe, image=pause_button, command=pause)
pause_widget.pack(side=LEFT, padx=5)

stop_widget= ttk.Button(Middleframe, image=stop_button, command=stop)
stop_widget.pack(side=LEFT, padx=5)

mute_widget= ttk.Button(Middleframe, image=mute_photo, command=mute)
mute_widget.pack(side=LEFT, padx=5)

volume=  ttk.Scale(Middleframe, from_=0, to =100,orient=HORIZONTAL, command=set_vol)
volume.pack()



root.mainloop()