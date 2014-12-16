from Tkinter import *

class MakeCurves():

    def __init__(self,canvas):
        #Variable
        self.dataSet = []

        self.xMin = 0
        self.xMax = 0

        self.colorIndex = 0
        self.gridColor = "white"

        #Create Canvas
        self.canvas = canvas

    def setData(self, dataSet, color, zoomX, yMinMax):
        self.dataSet = dataSet
        self.color = color
        self.zoomX = zoomX
        self.yMinMax = yMinMax
        self.xMin = 0
        self.xMax = len(dataSet) - 1
        self.repaint()

    # Paint logic
    #-------------

    def repaint(self):
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.drawGrid()
        self.plotLines()

    def drawGrid(self):
        self.grid = self.canvas.create_line(0, self.height/2, self.width, self.height/2, width=0, fill=self.gridColor)

    def plotLines(self):

        self.coordinates = []
        for i in range(0, len(self.dataSet)):
            x = float(i) / self.xMax * self.width * self.zoomX
            if self.dataSet[i] == "":
                y = float(self.height)+1
            elif float(self.dataSet[i]) > float(self.yMinMax[0]) or float(self.dataSet[i]) < float(self.yMinMax[1]):
                y = self.height - float(self.dataSet[i])
            else:
                y = float(self.height)+1
            self.coordinates.append(x)
            self.coordinates.append(y)

        self.canvas.create_line(self.coordinates, fill=self.color)
        self.canvas.coords(self.grid, 0, self.height/2, x, self.height/2)
        self.canvas.config(scrollregion=self.canvas.bbox(self.grid))

    # Event Handlers
    #----------------

    def canvasResized(self, event):
        self.repaint()


    def drawCurve(self, values):
        self.canvas.create_line(values)

