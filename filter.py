"""
Arthor: Chen Meng

python version: 2.7.10
"""

import os, time
from Tkinter import *
class CoreOperation:
    def __init__(self):
        self.now = time.localtime(time.time())
        self.nowyr = self.now.tm_year
        self.nowmon = self.now.tm_mon
        self.user = None
        self.idletime = 0
        self.minsize = 0
        self.loginfo = None
        self.directory = None
        self.desktop = None
        self.documents = None
        self.downloads = None
        self.movies = None
        self.music = None
        self.pictures = None

    def initialize(self):
        self.user = username.get()
        try:
            self.idletime = int(timeentry.get())
        except ValueError:
            pass
        try:
            mbsize = int(sizeentry.get())
            self.minsize = MBtoB(mbsize)
        except ValueError:
            pass
        self.directory = "/Users/" + self.user
        try:
            os.listdir(self.directory)
            self.desktop = self.directory + "/desktop"
            self.documents = self.directory + "/documents"
            self.downloads = self.directory + "/downloads"
            self.movies = self.directory + "/movies"
            self.music = self.directory + "/music"
            self.pictures = self.directory + "/pictures"
            createlog = os.path.join(self.desktop, "LogInfo.txt")
            self.loginfo = open(createlog, "w")
            self.Go()
        except OSError:
            usererrmsg.set("User not found!")
            
        

    def filter(self,direct):
        folders = []
        os.chdir(direct)
        files = os.listdir(direct)
        self.loginfo.write("\n")
        self.loginfo.write("Checking files in directory: " + direct+ "\n")
        for file in files:
            if ".photoslibrary" in file:
                pass
            elif ".imovielibrary" in file:
                pass
            elif ".theater" in file:
                pass
            elif ".DS_Store" in file:
                pass
            elif ".localized" in file:
                pass
            else:
                info = os.stat(file)
                bytesize = info.st_size
                atime = info.st_atime
                acctime = time.localtime(atime)
                yr = acctime.tm_year
                month = acctime.tm_mon
                day = acctime.tm_mday
                try:
                    os.listdir(direct + "/" + file)
                    folders.append(file)
                except OSError:
                    if self.nowmon-self.idletime<0:
                        if (self.nowyr-yr>=2 or(self.nowyr-yr==1 and month<=(12-abs(self.nowmon-self.idletime)))) and bytesize >= self.minsize:
                                self.loginfo.write(file + '        last accessed: ' + str(yr) + '.' + str(month) + '.' +str(day) + " size: " + str(BtoMB(bytesize)) + "MB." + "\n")
                    else:
                        if (yr<self.nowyr or (self.nowyr==yr and self.nowmon-month>=self.idletime)) and bytesize >= self.minsize:
                            self.loginfo.write(file + '        last accessed: ' + str(yr) + '.' + str(month) + '.' +str(day) + " size: " + str(BtoMB(bytesize)) + "MB."+ "\n")
        for folder in folders:
                try:
                    self.filter(direct + "/" + folder)
                except OSError:
                    pass

    def Go(self):
        self.filter(self.desktop)
        self.loginfo.write("\n")
        self.loginfo.write("\n")
        self.filter(self.documents)
        self.loginfo.write("\n")
        self.loginfo.write("\n")
        self.filter(self.downloads)
        self.loginfo.write("\n")
        self.loginfo.write("\n")
        self.filter(self.movies)
        self.loginfo.write("\n")
        self.loginfo.write("\n")
        self.filter(self.music)
        self.loginfo.write("\n")
        self.loginfo.write("\n")
        self.filter(self.pictures)
        self.loginfo.write("\n")
        self.loginfo.write("\n")
        self.loginfo.close()

def opendirect():
    direct = openentry.get()
    bashdirect = ""
    userlength = 0;
    if direct == "":
        pass
    else:
        try:
            sysdirect = "'" + direct + "'"
            os.system("open " + sysdirect)
        except:
            pass

def BtoMB(byte):
    return byte/1048576

def MBtoB(MB):
    return MB*1048576

##################################################
#                                                #
#            Graphical User Interface            #                                               
#                                                #
##################################################
win = Tk()
win.title("Idle File Filter")
win.geometry("530x260")
core = CoreOperation()

welcome = StringVar()
welcome.set("Welcome to Idle File Filter created by MC!")
welcome_label = Label(win, textvariable = welcome)
welcome_label.place(x=5, y=5)

usernamelabel = StringVar()
usernamelabel.set("Enter your username:")
username_label = Label(win, textvariable = usernamelabel)
username_label.place(x=5,y=50)

usererrmsg = StringVar()
usererrmsg.set("")
username = Entry(win, bd=2, width=15,textvariable=usererrmsg)
username.place(x=5,y=70)

timelabel = StringVar()
timelabel.set("Enter the month(s) you think a file is idle(maximum 12):")
time_label = Label(win, textvariable = timelabel)
time_label.place(x=5, y=100)

timeentry = Entry(win, bd=2, width=15)
timeentry.place(x=5, y=120)

openlabel = StringVar()
openlabel.set("Enter a directory to open a folder:")
open_label = Label(win, textvariable = openlabel)
open_label.place(x=5, y=200)

openentry = Entry(win, bd=2, width=20)
openentry.place(x=5, y=220)

openbutton = Button(win, text = "open" , command = opendirect)
openbutton.place(x=200, y=220)

sizelabel = StringVar()
sizelabel.set("Enter minimum size in Mbs if you want:")
size_label = Label(win, textvariable = sizelabel)
size_label.place(x=5, y=150)

sizeentry = Entry(win, bd=2, width=15)
sizeentry.place(x=5,y=170)

Golabel = StringVar()
Golabel.set("By clicking on go would create")
Go_label = Label(win, textvariable = Golabel)
Go_label.place(x=300, y=200)

Golabel2 = StringVar()
Golabel2.set("'loginfo.txt' on desktop.")
Go_label2 = Label(win, textvariable = Golabel2)
Go_label2.place(x=300, y=220)

Go_Button = Button(win, text="Go!", command=core.initialize)
Go_Button.place(x=450, y=220)

win.mainloop()
