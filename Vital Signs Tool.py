from Tkinter import *
import tkMessageBox
import time
import paint
import data

varsCheckButton = []
varsSpinBox = []
headlines = []
values = []
color = ["blue","red","green", "purple", "orange", "black"]

def keyControlQ(event):
    '''
    Asks the if the user really wants to quit the programm.
    :param event: key events
    :return: nothing
    '''
    menuBar.quitWarning()

def keyControlO(event):
    '''
    Opens a new file.
    :param event: key events
    :return: nothing
    '''
    newFile()

def newFile():
    '''
    Is the mainfuncion to create the plot.
    :return: nothing
    '''
    global mainMenu, canvasFrame, headlines, values
    if (daten.getFilename()):
        #CLEAE ALL THINGS
        clearEverything()
        headlines = daten.readHeadline()
        headlines = headlines[3:] #get every sensor, the three is to not get the time titles
        values = daten.readAllValues()
        infoBar.updateInfo()
        mainMenu.createSensor()
        infoBar.spinBox()
        canvasFrame.drawCurve()

def clearEverything():
    '''
    Deletes everything and sets the values to the back.
    :return: nothing
    '''
    global mainMenu, canvasFrame, headlines, values, varsSpinBox, varsCheckButton
    headlines = []
    values = []
    varsSpinBox = []
    varsCheckButton = []
    infoBar.clearInfoBar()
    mainMenu.clearMainMenu()

class MenuBar():
    def __init__(self, root):
        '''
        Creates the menubar.
        :param root: mainwindow
        :return: nothing
        '''
        self.root = root
        self.menubar = Menu(self.root)

        #file
        self.filemenu = Menu(self.menubar, tearoff = 0)
        self.filemenu.add_command(labe="Open", command=newFile, accelerator="Control-O")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=self.quitWarning, accelerator="Control-Q")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        ##info
        self.infomenu = Menu(self.menubar, tearoff = 0)
        self.infomenu.add_command(label="Info")
        self.infomenu.add_command(label="Help")
        self.infomenu.add_command(label="About", command=self.versionInfo)
        self.infomenu.add_separator()
        self.infomenu.add_command(label="Check for Updates...", command=self.updateWindow)
        self.menubar.add_cascade(label="Info", menu=self.infomenu)

        self.root.config(menu=self.menubar)

    def updateWindow(self):
        '''
        Displays the update messege.
        :return: nothing
        '''
        self.updateMessage = tkMessageBox.showinfo("Update", "No Update Avaiable...", icon="info")
    def versionInfo(self):
        '''
        Displays the version of the programm.
        :return: nothing
        '''
        self.versionMessage = tkMessageBox.showinfo("Version", "Vital Signs Data Explorer Version 1.0", icon="info")
    def quitWarning(self):
        '''
        Asks the user if he really wants to quit the programm.
        :return: nothing
        '''
        self.result = tkMessageBox.askquestion("Quit", "Are You Sure? Data will be lost!", icon="warning")
        if self.result == "yes":
            quit()

class MainMenu():
    def __init__(self, root):
        '''
        Creates the frame on the left side.
        :param root: mainwindow
        :return: nothing
        '''
        global daten
        self.frameMainMenu = Frame(root, bd=1, relief=RIDGE, height=550)
        self.frameMainMenu.pack(side=LEFT, anchor=N, fill=Y)
        self.createFrameSenor()

    def createFrameSenor(self):
        '''
        Creates the frame for the sensors.
        :return: nothing
        '''
        self.frameSensor = Frame(self.frameMainMenu)
        Label(self.frameSensor, text="Sensoren").pack(padx=30)
        self.frameSensor.pack()

    def createSensor(self):
        '''
        Creates a checkbutton for every sensor.
        :return: nothing
        '''
        global varsCheckButton, headlines, color

        self.varsCheckButton = []
        self.textColors = color
        self.i = 0

        for self.headline in headlines:
            self.var = IntVar()
            self.checkButton = Checkbutton(self.frameSensor, text=self.headline, variable=self.var, command=canvasFrame.drawCurve, fg=self.textColors[self.i])
            self.checkButton.select()
            self.checkButton.pack(padx=10)
            self.varsCheckButton.append(self.var)
            self.i += 1
        self.frameSensor.pack()
        varsCheckButton = self.varsCheckButton

    def clearMainMenu(self):
        '''
        Deletes the sensorframe and creates it again.
        :return: nothing
        '''
        self.frameSensor.destroy()
        self.createFrameSenor()
        self.i = 0

class CanvasFrame():
    def __init__(self, root):
        '''
        Creates the frame, canvas and the scrollbar.
        :param root: mainwindow
        :return: nothing
        '''
        global color
        self.plotColors = color
        self.root = root
        self.zoomX = 1
        self.canvasColor = "white"

        self.canvasframe = Frame(root, bd=1, relief=RIDGE)
        self.canvasframe.pack(side=TOP, fill=BOTH, expand=1)

        self.canvas = Canvas(self.canvasframe, bg=self.canvasColor)
        self.canvas.pack(side=TOP, fill=BOTH, expand=1)

        #Buttons
        self.plusButton = Button(self.canvas, text="+", width=3, command=self.plusB)
        self.plusButton.pack(side=TOP, anchor=E, pady=3, padx=3)
        self.minusButton = Button(self.canvas, text="-", width=3, command=self.minusB)
        self.minusButton.pack(side=TOP, anchor=E, padx=3)

        #Scrollbar
        self.scrollbar = Scrollbar(self.canvasframe, orient=HORIZONTAL)
        self.scrollbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.scrollbar.set, scrollregion=self.canvas.bbox(ALL))
        self.scrollbar.pack(side=BOTTOM, fill=X)

        self.canvas.bind('<Configure>', self.canvasResized)
        self.curves = paint.MakeCurves(self.canvas)

    def plusB(self):
        '''
        Increases the length of the x axis.
        :return: nothing
        '''
        if self.zoomX < 51:
            self.zoomX += 1.5
        self.drawCurve()

    def minusB(self):
        '''
        Decreases the length of the x axis.
        :return: nothing
        '''
        if self.zoomX > 1:
            self.zoomX -= 1.5
        self.drawCurve()

    def drawCurve(self):
        '''
        Draws the lines for every sensor with is activated.
        :return: nothing
        '''
        global varsCheckButton, headlines, values, color
        self.canvas.delete(ALL)
        self.value =[]
        for i in range(len(headlines)):
            if varsCheckButton[i].get() == 1:
                self.value = values[i+3]
                self.yMinMax = infoBar.getMinMax(i)
                self.curves.setData(self.value, color[i], self.zoomX, self.yMinMax)


    def canvasResized(self, event):
        '''
        Draws the line again after the size of the canvas have been changed.
        :param event: size of the canvas
        :return: nothing
        '''
        self.drawCurve()

class InfoBar():
    def __init__(self, root):
        '''
        Defines some start variables.
        :param root: mainwindow
        :return: nothing
        '''
        global headlines, color
        self.varsSpinBox = []
        self.i = 0
        self.createInfoFrame()
        self.yMax = 200

    def createInfoFrame(self):
        '''
        Creates the frame for the spinboxes and the infos.
        :return: nothing
        '''
        self.infoframe = Frame(root, height=60, bd=1, relief=RIDGE)
        self.infoframe.pack(side=BOTTOM, fill=BOTH)

        self.infoframe2 = Frame(root, height=20, bd=1, relief=RIDGE)
        self.infoframe2.pack(side=BOTTOM, fill=BOTH)

    def spinBox(self):
        '''
        Creates the spinboxes for each sensor.
        :return: nothing
        '''
        for self.headline in headlines:
            Label(self.infoframe, text=self.headline + " min:", fg=color[self.i]).grid(row=2, column=(self.i*2))
            Label(self.infoframe, text=self.headline + " max:", fg=color[self.i]).grid(row=3, column=(self.i*2))

            self.var0 = StringVar()
            self.var1 = StringVar()
            self.var1.set(self.yMax)
            self.entryMin = Spinbox(self.infoframe, from_=1, to=self.yMax, width=5, wrap=TRUE, textvariable=self.var0).grid(row=2, column=(self.i*2+1))
            self.varsSpinBox.append(self.var0)
            self.entryMax = Spinbox(self.infoframe, from_=1, to=self.yMax, width=5, wrap=TRUE, textvariable=self.var1).grid(row=3, column=(self.i*2+1))
            self.varsSpinBox.append(self.var1)

            self.i += 1

        Button(self.infoframe, text="Refresh", command=canvasFrame.drawCurve).grid(row=2, column=self.i*2, padx=20)
        Button(self.infoframe, text="Reset All", command=self.resetSpinBox).grid(row=3, column=self.i*2, padx=20)

    def resetSpinBox(self):
        '''
        Resets the spinboxes to the start values.
        :return: nothing
        '''
        for j in range(len(self.varsSpinBox)):
            if j%2 == 0:
                self.varsSpinBox[j].set(1)
            else:
                self.varsSpinBox[j].set(self.yMax)
        canvasFrame.drawCurve()

    def updateInfo(self):
        '''
        Displayes the infos.
        :return: nothing
        '''
        self.infos = daten.getInfo()
        self.starttime = Label(self.infoframe2, text="Starttime: " + self.infos[1])
        self.starttime.grid(row=0, column=0)

        self.endtime = Label(self.infoframe2, text="Endtime: " + self.infos[2])
        self.endtime.grid(row=0, column=1)

        self.length = Label(self.infoframe2, text="Length: " + self.infos[0])
        self.length.grid(row=0, column=2)

    def getMinMax(self, sensor):
        '''
        Gets the min and the max Value from the spinboxe.
        :param sensor: the sensor with values should be returned
        :return: the min and max value
        '''
        self.minMaX = []
        self.minMaX.append(float(self.varsSpinBox[sensor*2].get()))
        self.minMaX.append(float(self.varsSpinBox[sensor*2+1].get()))
        return self.minMaX

    def clearInfoBar(self):
        '''
        Deletes everything from the inforbar.
        :return:
        '''
        self.infoframe.destroy()
        self.infoframe2.destroy()
        self.createInfoFrame()
        self.varsSpinBox = []
        self.i = 0

class Statusbar():
    def __init__(self, root):
        '''
        Creates the statusbar.
        :param root: mainwindow
        :return: nothing
        '''
        self.status = Label(root, text="", bd=2, relief=SUNKEN, anchor=E)
        self.status.pack(side=BOTTOM, fill=X)
        self.updateDateTime()

    def updateDateTime(self):
        '''
        Updates the time and date in the statusbar.
        :return: nothing
        '''
        self.now = time.strftime("%A %d.%m.%Y    %H:%M:%S")
        self.status.configure(text=self.now)
        self.status.after(1000, self.updateDateTime)


root = Tk()

#blablabla

# **** Title ****
root.wm_title("Vital Signs Data Explorer 1.0")
root.geometry('1000x700')
root.bind("<Control-q>", keyControlQ)
root.bind("<Control-o>", keyControlO)

daten = data.Data()

# **** Menu Bar ****
menuBar = MenuBar(root)

# **** Status Bar ****
statusBar = Statusbar(root)

# **** Main Menu ****
mainMenu = MainMenu(root)

# **** Info Bar ****
infoBar = InfoBar(root)

# **** Canvas Window ****
canvasFrame = CanvasFrame(root)

root.mainloop()
