class MakeCurves():
    def __init__(self,canvas):
        #Variable
        self.dataSet = []
        self.xMax = 0
        self.colorIndex = 0
        self.gridColor = "white"

        #Save Canvas
        self.canvas = canvas

    def setData(self, dataSet, color, zoomX, yMinMax):
        '''
        Sets the data so the line can be drawn
        :param dataSet: the values
        :param color: color of the line
        :param zoomX: the x zoom factor
        :param yMinMax: the min and max height
        :return:
        '''
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
        '''
        Draws the grid and the lines.
        :return: nothing
        '''
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.drawGrid()
        self.plotLines()

    def drawGrid(self):
        '''
        Draws the grid.
        :return: nothing
        '''
        self.grid = self.canvas.create_line(0, 0, self.width, 0, width=0, fill=self.gridColor)

    def plotLines(self):
        '''
        Draw the line into the canvas.
        :return: nothing
        '''
        self.lenDataSet = len(self.dataSet)
        self.coordinates = [0 for x in range(self.lenDataSet * 2)]

        for i in range(0, self.lenDataSet):
            x = float(i) / self.xMax * self.width * self.zoomX
            if self.dataSet[i] == "":
                y = self.height + 1
            else:
                y = (float(self.dataSet[i]) - self.yMinMax[0]) / (self.yMinMax[1]-self.yMinMax[0]) * self.height
                y = self.height - y
            self.coordinates[i*2] = x
            self.coordinates[i*2+1] = y

        self.canvas.create_line(self.coordinates, fill=self.color)
        self.canvas.coords(self.grid, 0, 0, x, 0)
        self.canvas.config(scrollregion=self.canvas.bbox(self.grid))

    # Event Handlers
    #----------------

    def canvasResized(self, event):
        '''
        Repaint the lines after the size of the canvas have been changed.
        :param event: Coordinates for the canvas
        :return: nothing
        '''
        self.repaint()