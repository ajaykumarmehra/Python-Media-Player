import os
import numpy as np
from tkinter import *
from tkinter import filedialog
#from fileDialog import askopenfilename
#import FileDialog
#from tkFileDialog import askopenfilename
import time
import vlc

def Main():

    root = Tk()
    root.title("Player")
    height = 180
    width = 420
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sh/2) - (height/2)
    y = (sw/2) - (width/2)

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


    player = Player(root)
    player.pack(side=TOP)

    Bottom = Frame(root)
    Bottom.pack(side=BOTTOM)

    Open = Button(Bottom, text='Open', command=player.Open, width=8, height=2)
    Open.pack(side=LEFT)

    Start = Button(Bottom, text='Start', command=player.Start, width=8, height=2)
    Start.pack(side=LEFT)

    Stop = Button(Bottom, text='Pause', command=player.Stop, width=8, height=2)
    Stop.pack(side=LEFT)

    Reset = Button(Bottom, text='Reset', command=player.Reset, width=8, height=2)
    Reset.pack(side=LEFT)

    Exit = Button(Bottom, text='Close', command=player.Exit, width=8, height=2)
    Exit.pack(side=LEFT)

    root.config(bg="grey")
    root.mainloop()

class Player(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.startT = 0.0
        self.nextT = 0.0
        self.Run = 0
        self.timestr = StringVar()
        self.MakeWidget()
        self.ply = None
        self.curr_fil = None

    def MakeWidget(self):
        timeText = Label(self, textvariable=self.timestr, font=("times new roman", 50), fg="red", bg="black")
        self.SetTime(self.nextT)
        timeText.pack(expand = YES ,pady=2, padx=2)

    def Updater(self):
        self.nextT = time.time() - self.startT
        self.SetTime(self.nextT)
        self.timer = self.after(60, self.Updater)

    def SetTime(self, nextElap):
        hours = int(nextElap / 60 / 60.0)
        minutes = int(nextElap / 60)
        seconds = int(nextElap - minutes * 60.0)
        miliSeconds = int((nextElap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours ,minutes, seconds, miliSeconds))

    def Start(self):
        if (not self.Run) and (self.ply):
            self.startT = time.time() - self.nextT
            self.Updater()
            self.Run = 1
            self.ply.play()

    def Stop(self):
        if self.Run and self.ply:
            self.after_cancel(self.timer)
            self.nextT = time.time() - self.startT
            self.SetTime(self.nextT)
            self.Run = 0
            self.ply.pause()

    def Exit(self):
        exit()

    def sel_fil(self):
        self.file = filedialog.askopenfile(title='Choose a Media file')
        self.filename = self.file.name
        self.curr_fil = self.filename

    def Open(self):
        self.sel_fil()
        self.ply = vlc.MediaPlayer(self.curr_fil)

	    
    def Reset(self):
        self.Stop()
        self.startT = time.time()
        self.nextT = 0.0
        self.SetTime(self.nextT)
        if self.ply:
            self.ply.stop()
            self.ply = None

Main()
