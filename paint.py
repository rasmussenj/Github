class MakeCurves():
    def __init__(self, canvas):
        """
        Set some variables.
        :param canvas: the canvas in with the painting should be done.
        :return: nothing
        """
        self.dataSet = []
        self.xMax = 0
        self.colorIndex = 0
        self.gridColor = "white"
        self.oldWidth = 1
        self.cursorX = -1
        self.cursorXLine = -1
        self.zoomXold = 1

        #Save Canvas
        self.canvas = canvas

    def setData(self, dataSet, color, zoomX, yMinMax):
        """
        Sets the data so the line can be drawn.
        :param dataSet: the values
        :param color: color of the line
        :param zoomX: the x zoom factor
        :param yMinMax: the min and max height
        :return: nothing
        """
        self.dataSet = dataSet
        self.color = color
        self.zoomX = zoomX
        self.yMinMax = yMinMax
        self.xMin = 0
        self.xMax = len(dataSet) - 1
        self.repaint()

    def repaint(self):
        """
        First saves the height and the width of the canvas, then draws the grid and the lines.
        :return: nothing
        """
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.drawGrid()
        self.plotLines()

    def drawGrid(self):
        """
        Draws the grid as long as the canvas is. This is important because the scrollbar has the same length as this
        line has. The color of the line is the same as the background color from the canvas.
        :return: nothing
        """
        self.grid = self.canvas.create_line(0, 0, self.width, 0, width=0, fill=self.gridColor)
        self.canvas.delete("cursorLine")
        self.cursorLine = self.canvas.create_line(0, 0, 0, 0, fill="black", tag="cursorLine")

    def plotLines(self):
        """
        Draw the line into the canvas. If there is no value the line is goes out of the canvas. This way the user can not
         see the line anymore. The line is saved in a list which length is defined at the beginning. Ath the end the grid
         is updated and the scrollbar is made as long as the canvas.
        :return: nothing
        """
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

    def buttonPressed(self, event):
        """
        This function is called if the mouse button is clickt on the canvas. Then transform the coordinates into
        coordinates on the canvas and draws the line and calls the function which calculates the x value.
        :param event: the coordinates where the mouse button was clicked
        :return: nothing
        """
        canvas = event.widget
        self.cursorX = canvas.canvasx(event.x)
        if self.cursorX >= 0:
            self.canvas.coords(self.cursorLine, self.cursorX, 0, self.cursorX, self.height-1)
            self.calcXValues()

    def calcXValues(self):
        """
        Calculates the x value and returns it.
        :return: The x value
        """
        self.xValue = int(self.cursorX * self.xMax / (self.width * self.zoomX))
        return self.xValue