from tkinter import *
import time
import sleep
import threading
from pynput.keyboard import KeyCode

class Timer:
    reminderTime = 1800  #in secs
    one_more_minute = False
    SECS_PER_MIN = 60
    FILE_NAME = 'configure.txt'
    TEXT_1 = "起身活动休息下"
    TEXT_2 =  "知道了"
    SIZE = 16
    muteHotKey = [KeyCode.from_char('l'),KeyCode.from_char('w'),KeyCode.from_char('x')]
    configHotKey = [KeyCode.from_char('c'),KeyCode.from_char('f'),KeyCode.from_char('g')]
    REMINDER_TIME_CHANGED = False

    def __init__(self):
        self.snooze = 0
        try:
            f = open(self.FILE_NAME,'r')
            for line in f:
                #exclude the last line
                if(len(line)!=0):
                    if(line.split('=')[0]=='endPassword'):
                        self.muteHotKey = []
                        for element in line.split('=')[1].split('\n')[0]:
                            self.muteHotKey.append(KeyCode.from_char(element))
                    elif(line.split('=')[0]=='configHotKey'):
                        self.configHotKey = []
                        for element in line.split('=')[1].split('\n')[0]:
                            self.configHotKey.append(KeyCode.from_char(element))
                    else:
                        self.reminderTime = int(line.split('=')[1].split('\n')[0])
            f.close()
        except :
            self.writeToFile()
        self.isRunning = True
        self.startTime = time.localtime()
        self.sleeper = sleep.Sleep(1)

    def writeToFile(self,fileName='configure.txt'):
        f = open(fileName,'w')

        f.write('reminderTime='+str(self.reminderTime)+'\n')

        temp =''
        for element in self.muteHotKey:
            element = str(element)
            temp = temp+element[1]
        f.write('muteHotKey'+'='+temp+'\n')

        temp =''
        for element in self.configHotKey:
            element = str(element)
            temp = temp+element[1]
        f.write('configHotKey'+'='+temp+'\n')

        f.close()

    def readFile(self):
        f = open(self.FILE_NAME,'r')
        for line in f:
            #exclude the last line
            if(len(line)!=0):
                if(line.split('=')[0]=='endPassword'):
                    self.muteHotKey = []
                    for element in line.split('=')[1].split('\n')[0]:
                        self.muteHotKey.append(KeyCode.from_char(element))
                elif(line.split('=')[0]=='configHotKey'):
                    self.configHotKey = []
                    for element in line.split('=')[1].split('\n')[0]:
                        self.configHotKey.append(KeyCode.from_char(element))
                else:
                    self.reminderTime = int(line.split('=')[1].split('\n')[0])
        f.close()

    def window(self,text_1,size,text_2 =TEXT_2,isReminder = False):
        root = Tk()
        label= Label(root, text=text_1,font=("Helvetica", size))
        label.pack()
        button = Button(root, text=text_2, command=label.quit)
        button.pack()
        if isReminder:
            def oneMoreMinute():
                self.one_more_minute = True
                label.quit()
            button2 = Button(root, text="请再给我1分钟", command=oneMoreMinute)
            button2.pack()
        root.attributes("-topmost", True)
        root.mainloop()
        # When you call self.root.destroy(), Tkinter will exit the root.mainloop
        # Then after the place where you call root.mainloop(), you probably have a
        # call to root.destroy(). This means you are trying to destroy twice,
        # which is what is causing the error. ------ Rob Murray
        try:
            root.destroy()
        except:
            pass

    def config(self):
        def setReminderTime():
            try:
                if(int(mins.get())>=0):
                    self.reminderTime = int(mins.get()) * self.SECS_PER_MIN
                    self.writeToFile()
                    self.window(text_1="提醒间隔设置成功",size = self.SIZE, text_2 ="确定")
                    self.REMINDER_TIME_CHANGED = True
                    self.sleeper.wake()
                else:
                    self.window(text_1="提醒间隔设置不成功, 请重新输入",text_2 ="确定",size=self.SIZE)
            except ValueError:
                self.window(text_1="提醒间隔设置不成功, 请重新输入s",text_2 ="确定",size=self.SIZE)

        def setmuteHotKey():
            self.muteHotKey = []
            for x in muteHotKey.get():
                self.muteHotKey.append(KeyCode.from_char(x))
            self.writeToFile()
            self.window(text_1="结束快捷键设置成功",text_2 ="确定",size = self.SIZE)

        def setconfigHotKey():
            self.configHotKey = []
            for x in configHotKey.get():
                self.configHotKey.append(KeyCode.from_char(x))
            self.writeToFile()
            self.window(text_1="设置面板快捷键设置成功",text_2 ="确定",size = self.SIZE)

        root = Tk()
        label_1 = Label(root, text="提醒间隔(分钟): ")
        label_1.grid(row=0, column=1)
        mins = Entry(root)
        mins.grid(row=0, column=2)
        mins.insert(INSERT,int(self.reminderTime/self.SECS_PER_MIN))
        mins.selection_range(0, END)
        b_1 = Button(root, text="设置", width=10, command=setReminderTime)
        b_1.grid(row=0, column=3)

        label_2 = Label(root, text="结束快捷键：")
        label_2.grid(row=2, column=1)
        muteHotKey = Entry(root)
        muteHotKey.grid(row=2, column=2)
        #display present password
        temp =''
        for element in self.muteHotKey:
            element = str(element)
            temp = temp+element[1]
        muteHotKey.insert(0, temp)
        muteHotKey.selection_range(0, END)
        b_2 = Button(root, text="设置", width=10, command=setmuteHotKey)
        b_2.grid(row=2, column=3)

        label_3 = Label(root, text="设置面板快捷键：")
        label_3.grid(row=3, column=1)
        configHotKey = Entry(root)
        configHotKey.grid(row=3, column=2)
        #display present password
        temp =''
        for element in self.configHotKey:
            element = str(element)
            temp = temp+element[1]
        configHotKey.insert(0, temp)
        configHotKey.selection_range(0, END)
        b_3 = Button(root, text="设置", width=10, command=setconfigHotKey)
        b_3.grid(row=3, column=3)

        root.mainloop()

    def mainLoop(self):
        self.count = 0
        while(True):
            if self.one_more_minute:
                self.sleeper.sleep(self.SECS_PER_MIN)
                self.one_more_minute = False
            else:
                self.sleeper.sleep(self.reminderTime)
            if not self.REMINDER_TIME_CHANGED:
                self.window(self.TEXT_1,self.SIZE,isReminder=True)
            self.REMINDER_TIME_CHANGED = False
