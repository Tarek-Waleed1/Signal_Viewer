from PyQt5 import QtGui, QtCore, QtWidgets
import csv
from PyQt5.QtWidgets import QFileDialog, QColorDialog
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import numpy as np
import pandas as pd
import random
import os
from classes import channelLine
from functools import partial
from random import randint
from fpdf import FPDF
import utility

arrayOfUpperChannels = []
arrayOfLowerChannels = []
zoomlevel = 1
speedUp = 1
speedDown = 1
isplayingup = True
isplayingdown = True
statTables = []
captured_images = []
mean_values = []
std_values = []
min_values = []
max_values = []
duration_values = []
channelNames = []
zoominupcount=0
zoomindowncount=0
zoomoutupcount=0
zoomoutdowncount=0

def browseFiles(self, direction, graph, channel, control):
        self.filename, _ = QFileDialog.getOpenFileName(None, 'Open the signal file', './',
                                                       filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
        path = self.filename
        tempChl = channelLine()
        filetype = path[len(path) - 3:]

        if filetype == "dat":
            dataframe=utility.read_csv_file(path)

        if self.filename:
            try:
                dataframe = pd.read_csv(path)
            except pd.errors.EmptyDataError:
                return
            except pd.errors.ParserError:
                dataframe = pd.read_csv(path, header=None)

            utility.add_channel(self,dataframe, direction, graph, channel, control, arrayOfUpperChannels, arrayOfLowerChannels, tempChl)
        


def plot_data(self, viewport, x, y, names, line, direction):
    global isplayingup
    global isplayingdown
    viewport.addLegend()
    line.plotRef = viewport.plot(x, y, pen=line.color, name=line.label)
    line.plotRef.clear()
    if direction == "up":
        theranges = findmaxminranges(arrayOfUpperChannels)
    else:
        theranges = findmaxminranges(arrayOfLowerChannels)
    viewport.setLimits(xMin=theranges[0], xMax=theranges[1], yMin=theranges[2], yMax=theranges[3])
    line.timer = QtCore.QTimer()
    line.timer.setInterval(100)
    line.timer.timeout.connect(partial(update_plot_data, x, y, viewport, line, self, direction))
    if (isplayingup == True and direction == 'up') or (isplayingdown == True and direction == 'down'):
        line.timer.start()


def update_plot_data(x, y, viewport, line, self, direction):
    line.addValue()
    global speedUp
    global speedDown
    global speedUpDown
    if direction == "up":
        line.timer.setInterval(int(100 / speedUp))
    else:
        line.timer.setInterval(int(100 / speedDown))
    line.plotRef.setData(line.x_values, line.y_values, pen=line.color, name=line.label, skipfinitecheck=True)


def zoominfunction(self, direction, viewup, viewdown, linkingcondition):
    global zoominupcount
    global zoomindowncount
    zoom = (0.5, 0.9)
    if direction == "up":
        viewup.plotItem.getViewBox().scaleBy(zoom)
        if linkingcondition.isChecked():
            viewdown.plotItem.getViewBox().scaleBy(zoom)
        zoominupcount+=1
    else:
        viewdown.plotItem.getViewBox().scaleBy(zoom)
        if linkingcondition.isChecked():
            viewup.plotItem.getViewBox().scaleBy(zoom)
        zoomindowncount+=1    

def zoomoutfunction(self, direction, viewup, viewdown, linkingcondition):
    global zoomoutdowncount
    global zoomoutupcount
    zoom = (2, 8)
    if direction == "up":
        viewup.plotItem.getViewBox().scaleBy(zoom)
        if linkingcondition.isChecked():
            viewdown.plotItem.getViewBox().scaleBy(zoom)
        zoomoutupcount+=1
    else:
        viewdown.plotItem.getViewBox().scaleBy(zoom)
        if linkingcondition.isChecked():
            viewup.plotItem.getViewBox().scaleBy(zoom)
        zoomoutdowncount+=1   

def sliderValueChanged(numberu, numberd, slider, isLinked, direction):
    value = slider.value() / 10
    global speedUp
    global speedDown
    if isLinked.isChecked():
        numberu.setText(str(value))
        numberd.setText(str(value))
        slider.setValue(slider.value())
        speedUp = value
        speedDown = value
    elif direction == 'up':
        numberu.setText(str(value))
        speedUp = value
    else:
        numberd.setText(str(value))
        speedDown = value


def changeVisibility(direction, channel):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    if direction == 'up' and channel.currentIndex() > 0:
        arrayOfUpperChannels[channel.currentIndex() - 1].changeVisibility()
    elif direction == 'down' and channel.currentIndex() > 0:
        arrayOfLowerChannels[channel.currentIndex() - 1].changeVisibility()


def changcolors(direction, channel):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    choicecolor = QColorDialog.getColor()
    if direction == "up" and channel.currentIndex() > 0:
        arrayOfUpperChannels[channel.currentIndex() - 1].color = choicecolor
        arrayOfUpperChannels[channel.currentIndex() - 1].plotRef.setData(arrayOfUpperChannels[channel.currentIndex() - 1].x_values, arrayOfUpperChannels[channel.currentIndex() - 1].y_values, pen=arrayOfUpperChannels[channel.currentIndex() - 1].color, name=arrayOfUpperChannels[channel.currentIndex() - 1].label, skipfinitecheck=True)
    elif direction == "down" and channel.currentIndex() > 0:
        arrayOfLowerChannels[channel.currentIndex() - 1].color = choicecolor
        arrayOfLowerChannels[channel.currentIndex() - 1].plotRef.setData(arrayOfLowerChannels[channel.currentIndex() - 1].x_values, arrayOfLowerChannels[channel.currentIndex() - 1].y_values, pen=arrayOfLowerChannels[channel.currentIndex() - 1].color, name=arrayOfLowerChannels[channel.currentIndex() - 1].label, skipfinitecheck=True)
    else:
        return ()


def changeLineName(direction, channel, newName, control):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    if direction == "up" and channel.currentIndex() > 0 and arrayOfUpperChannels[(channel.currentIndex())-1].isMoved==False :
        control.removeItem(arrayOfUpperChannels[channel.currentIndex() - 1].label)
        arrayOfUpperChannels[channel.currentIndex() - 1].label = channel.currentText() + " - " + newName
        control.addItem(arrayOfUpperChannels[channel.currentIndex() - 1].plotRef,
                        arrayOfUpperChannels[channel.currentIndex() - 1].label)
    elif direction == "down" and channel.currentIndex() > 0 and arrayOfLowerChannels[(channel.currentIndex())-1].isMoved==False:
        control.removeItem(arrayOfLowerChannels[channel.currentIndex() - 1].label)
        arrayOfLowerChannels[channel.currentIndex() - 1].label = channel.currentText() + " - " + newName
        control.addItem(arrayOfLowerChannels[channel.currentIndex() - 1].plotRef,
                        arrayOfLowerChannels[channel.currentIndex() - 1].label)
    else:
        return ()


def handleLinkGraphs(self, islinked,numUp,numDown,sliderNumUp,sliderNumDown):
    global isplayingup
    global isplayingdown
    global speedUp
    global speedDown
    if (islinked.isChecked()):
        isplayingup = False
        isplayingdown = False
        for i in range(len(arrayOfUpperChannels)):
            arrayOfUpperChannels[i].timer.stop()
        for i in range(len(arrayOfLowerChannels)):
            arrayOfLowerChannels[i].timer.stop()
    speedUp=1.0
    numUp.setText('1.0')
    sliderNumUp.setValue(10)
    speedDown=1.0
    numDown.setText('1.0')
    sliderNumDown.setValue(10)


def pauseplay(self, direction, linkcheck):
    global isplayingup
    global isplayingdown
    # global isplaying
    if (direction == 'up'):
        if(linkcheck.isChecked()):
            if (isplayingup == True):
                isplayingup = False
                isplayingdown = False
                for i in range(len(arrayOfLowerChannels)):
                    arrayOfLowerChannels[i].timer.stop()
                for i in range(len(arrayOfUpperChannels)):
                    arrayOfUpperChannels[i].timer.stop()

            else:
                isplayingup = True
                isplayingdown = True
                for i in range(len(arrayOfLowerChannels)):
                    if arrayOfLowerChannels[i].isMoved == False:
                        arrayOfLowerChannels[i].timer.start()
                for i in range(len(arrayOfUpperChannels)):
                    if arrayOfUpperChannels[i].isMoved == False:
                        arrayOfUpperChannels[i].timer.start()
        else:
            if (isplayingup == True):
                isplayingup = False
                for i in range(len(arrayOfUpperChannels)):
                    arrayOfUpperChannels[i].timer.stop()
            else:
                isplayingup = True
                for i in range(len(arrayOfUpperChannels)):
                    if arrayOfUpperChannels[i].isMoved == False:
                        arrayOfUpperChannels[i].timer.start()
    else:
        if (linkcheck.isChecked()):
            if (isplayingup == True):
                isplayingup = False
                isplayingdown = False
                for i in range(len(arrayOfLowerChannels)):
                    arrayOfLowerChannels[i].timer.stop()
                for i in range(len(arrayOfUpperChannels)):
                    arrayOfUpperChannels[i].timer.stop()

            else:
                isplayingup = True
                isplayingdown = True
                for i in range(len(arrayOfLowerChannels)):
                    if arrayOfLowerChannels[i].isMoved == False:
                        arrayOfLowerChannels[i].timer.start()
                for i in range(len(arrayOfUpperChannels)):
                    if arrayOfUpperChannels[i].isMoved == False:
                        arrayOfUpperChannels[i].timer.start()
        else:
            if (isplayingdown == True):
                isplayingdown = False
                for i in range(len(arrayOfLowerChannels)):
                    arrayOfLowerChannels[i].timer.stop()
            else:
                isplayingdown = True
                for i in range(len(arrayOfLowerChannels)):
                    if arrayOfLowerChannels[i].isMoved == False:
                        arrayOfLowerChannels[i].timer.start()


# Gets min max for ranges used in plot
def findmaxminranges(signalarray):
    Minx = 0
    Maxx = 0
    Miny = 0
    Maxy = 0

    for index in range(len(signalarray)):
        if len(signalarray[index].time) != 0 and max(signalarray[index].time) > Maxx:
            Maxx = max(signalarray[index].time)
        if len(signalarray[index].time) != 0 and min(signalarray[index].time) < Minx:
            Minx = min(signalarray[index].time)
        if len(signalarray[index].amplitude) != 0 and max(signalarray[index].amplitude) > Maxy:
            Maxy = max(signalarray[index].amplitude)
        if len(signalarray[index].amplitude) != 0 and min(signalarray[index].amplitude) < Miny:
            Miny = min(signalarray[index].amplitude)
    return ([Minx, Maxx, Miny, Maxy])


def rewindfunction(self, direction, viewport):
    if (direction == 'up' and arrayOfUpperChannels != []):
        for i in range(len(arrayOfUpperChannels)):
            arrayOfUpperChannels[i].x_values = []
            arrayOfUpperChannels[i].y_values = []
            arrayOfUpperChannels[i].plotRef.clear()
            # viewport.setXRange(0, arrayOfUpperChannels[i].time[100])
    elif (direction == 'down' and arrayOfLowerChannels != []):
        for i in range(len(arrayOfLowerChannels)):
            arrayOfLowerChannels[i].x_values = []
            arrayOfLowerChannels[i].y_values = []
            arrayOfLowerChannels[i].plotRef.clear()
            # viewport.setXRange(0, arrayOfLowerChannels[i].time[100])


def changegraphsfunction(self, direction, channelup, channeldown, viewup, viewdown, control):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    dummyline = channelLine()
    if direction == 'up' and channelup.count != 0 and channelup.currentIndex() > 0 and arrayOfUpperChannels[
        channelup.currentIndex() - 1].isMoved == False:  # moving from up to down
        if channeldown.count() == 0:  # moving to empty channels
            channeldown.addItem('--Add Channels--')
            channeldown.addItem('channel 1')
            dummyline.time = arrayOfUpperChannels[channelup.currentIndex() - 1].time
            dummyline.amplitude = arrayOfUpperChannels[channelup.currentIndex() - 1].amplitude
            dummyline.x_values = arrayOfUpperChannels[channelup.currentIndex() - 1].x_values
            dummyline.y_values = arrayOfUpperChannels[channelup.currentIndex() - 1].y_values
            arrayOfUpperChannels[channelup.currentIndex() - 1].plotRef.setData([], [])
            arrayOfUpperChannels[channelup.currentIndex() - 1].timer.stop()
            arrayOfLowerChannels.append(dummyline)
            arrayOfLowerChannels[0].label = 'channel 1'
            arrayOfUpperChannels[channelup.currentIndex() - 1].isMoved = True
            control.removeItem(arrayOfUpperChannels[channelup.currentIndex() - 1].label)
            plot_data(self, viewdown, arrayOfLowerChannels[0].time, arrayOfLowerChannels[0].amplitude,
                      arrayOfLowerChannels[0].label, arrayOfLowerChannels[0], 'down')
            refresh(arrayOfLowerChannels)
        else:  # moving to none empty channel selector
            dummyline.time = arrayOfUpperChannels[channelup.currentIndex() - 1].time
            dummyline.amplitude = arrayOfUpperChannels[channelup.currentIndex() - 1].amplitude
            arrayOfUpperChannels[channelup.currentIndex() - 1].plotRef.setData([], [])
            arrayOfUpperChannels[channelup.currentIndex() - 1].timer.stop()
            arrayOfUpperChannels[channelup.currentIndex() - 1].isMoved = True
            indexOfMoved = isMoved(arrayOfLowerChannels)
            control.removeItem(arrayOfUpperChannels[channelup.currentIndex() - 1].label)
            if indexOfMoved != -1:  # means that there is an empty channel takes prioity
                indexofavailableline = numberoffilledarray(arrayOfLowerChannels)
                arrayOfLowerChannels[indexOfMoved].time = dummyline.time
                arrayOfLowerChannels[indexOfMoved].amplitude = dummyline.amplitude
                arrayOfLowerChannels[indexOfMoved].x_values = arrayOfUpperChannels[
                    channelup.currentIndex() - 1].x_values
                arrayOfLowerChannels[indexOfMoved].y_values = arrayOfUpperChannels[
                    channelup.currentIndex() - 1].y_values
                arrayOfLowerChannels[indexOfMoved].isMoved = False
                arrayOfLowerChannels[indexOfMoved].label = f'channel {indexOfMoved + 1}'
                if indexofavailableline != -1:
                    arrayOfLowerChannels[indexOfMoved].x_values = []
                    arrayOfLowerChannels[indexOfMoved].y_values = []
                    arrayOfLowerChannels[indexOfMoved].fillxvaluesandyvalues(
                        len(arrayOfLowerChannels[indexofavailableline].x_values))
                plot_data(self, viewdown, arrayOfLowerChannels[indexOfMoved].time,
                          arrayOfLowerChannels[indexOfMoved].amplitude, arrayOfLowerChannels[indexOfMoved].label,
                          arrayOfLowerChannels[indexOfMoved], 'down')
                refresh(arrayOfLowerChannels)
            else:  # no empty channels therfore add to end of list
                channeldown.addItem(f'channel {channeldown.count()}')
                arrayOfLowerChannels.append(dummyline)
                arrayOfLowerChannels[-1].label = f'channel {channeldown.count() - 1}'
                arrayOfLowerChannels[-1].fillxvaluesandyvalues(len(arrayOfLowerChannels[0].x_values))
                plot_data(self, viewdown, arrayOfLowerChannels[-1].time, arrayOfLowerChannels[-1].amplitude,
                          arrayOfLowerChannels[-1].label, arrayOfLowerChannels[-1], 'down')
                refresh(arrayOfLowerChannels)
    elif direction == 'down' and channeldown.count != 0 and channeldown.currentIndex() > 0 and arrayOfLowerChannels[
        channeldown.currentIndex() - 1].isMoved == False:  # moving from down to up
        if channelup.count() == 0:  # moving to empty channels selector
            channelup.addItem('--Add Channels--')
            channelup.addItem('channel 1')
            dummyline.time = arrayOfLowerChannels[channeldown.currentIndex() - 1].time
            dummyline.x_values = arrayOfLowerChannels[channeldown.currentIndex() - 1].x_values
            dummyline.y_values = arrayOfLowerChannels[channeldown.currentIndex() - 1].y_values
            dummyline.amplitude = arrayOfLowerChannels[channeldown.currentIndex() - 1].amplitude
            arrayOfLowerChannels[channeldown.currentIndex() - 1].plotRef.setData([], [])
            arrayOfLowerChannels[channeldown.currentIndex() - 1].timer.stop()
            arrayOfUpperChannels.append(dummyline)
            arrayOfUpperChannels[0].label = 'channel 1'
            arrayOfLowerChannels[channeldown.currentIndex() - 1].isMoved = True
            control.removeItem(arrayOfLowerChannels[channeldown.currentIndex() - 1].label)
            plot_data(self, viewup, arrayOfUpperChannels[0].time, arrayOfUpperChannels[0].amplitude,
                      arrayOfUpperChannels[0].label, arrayOfUpperChannels[0], 'up')
            refresh(arrayOfUpperChannels)
        else:  # moving to non empty channels selector
            dummyline.time = arrayOfLowerChannels[channeldown.currentIndex() - 1].time
            dummyline.amplitude = arrayOfLowerChannels[channeldown.currentIndex() - 1].amplitude
            arrayOfLowerChannels[channeldown.currentIndex() - 1].plotRef.setData([], [])
            arrayOfLowerChannels[channeldown.currentIndex() - 1].timer.stop()
            arrayOfLowerChannels[channeldown.currentIndex() - 1].isMoved = True
            indexOfMoved = isMoved(arrayOfUpperChannels)
            control.removeItem(arrayOfLowerChannels[channeldown.currentIndex() - 1].label)
            if indexOfMoved != -1:  # means that there is an empty channel takes prioity
                indexofavailableline = numberoffilledarray(arrayOfUpperChannels)
                arrayOfUpperChannels[indexOfMoved].time = dummyline.time
                arrayOfUpperChannels[indexOfMoved].amplitude = dummyline.amplitude
                arrayOfUpperChannels[indexOfMoved].x_values = arrayOfLowerChannels[
                    channeldown.currentIndex() - 1].x_values
                arrayOfUpperChannels[indexOfMoved].y_values = arrayOfLowerChannels[
                    channeldown.currentIndex() - 1].y_values
                arrayOfUpperChannels[indexOfMoved].isMoved = False
                arrayOfUpperChannels[indexOfMoved].label = f'channel {indexOfMoved + 1}'
                if indexofavailableline != -1:
                    arrayOfUpperChannels[indexOfMoved].x_values = []
                    arrayOfUpperChannels[indexOfMoved].y_values = []
                    arrayOfUpperChannels[indexOfMoved].fillxvaluesandyvalues(
                        len(arrayOfUpperChannels[indexofavailableline].x_values))
                plot_data(self, viewup, arrayOfUpperChannels[indexOfMoved].time,
                          arrayOfUpperChannels[indexOfMoved].amplitude, arrayOfUpperChannels[indexOfMoved].label,
                          arrayOfUpperChannels[indexOfMoved], 'up')
                refresh(arrayOfUpperChannels)
            else:  # no empty channels therfore add to end of list
                channelup.addItem(f'channel {channelup.count()}')
                arrayOfUpperChannels.append(dummyline)
                arrayOfUpperChannels[-1].label = f'channel {channelup.count() - 1}'
                arrayOfUpperChannels[-1].fillxvaluesandyvalues(len(arrayOfUpperChannels[0].x_values))
                plot_data(self, viewup, arrayOfUpperChannels[-1].time, arrayOfUpperChannels[-1].amplitude,
                          arrayOfUpperChannels[-1].label, arrayOfUpperChannels[-1], 'up')
                refresh(arrayOfUpperChannels)


def isMoved(arrayOfChannels):
    for i in range(len(arrayOfChannels)):
        if arrayOfChannels[i].isMoved == True:
            return i

    return -1


def numberoffilledarray(arrayOfChannels):
    for i in range(len(arrayOfChannels)):
        if arrayOfChannels[i].isMoved != True:
            return i

    return -1


def moveacrossx(self, viewportup, viewportdown, scrollbar, direction, linkcheck):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    global zoominupcount
    global zoomindowncount
    global zoomoutupcount
    global zoomoutdowncount
    if linkcheck.isChecked():
        if len(arrayOfUpperChannels) == 0 or len(arrayOfLowerChannels) == 0:
            return
        else:
            allvalues = arrayOfLowerChannels
            allvalues.extend(arrayOfUpperChannels)
            maxid = findmaxxvalues(allvalues)
            scrollbar.setMinimum(0)
            scrollbar.setMaximum(int(allvalues[maxid].x_values[-1]))
            scrollbar.setSingleStep(1)
            valueofhorizontal = scrollbar.value()
            viewportup.plotItem.setXRange((valueofhorizontal - 1), valueofhorizontal)
            viewportdown.plotItem.setXRange((valueofhorizontal - 1), valueofhorizontal)
    elif direction == "up":
        if len(arrayOfUpperChannels) == 0:
            return
        else:
            zoomfactor=zoominupcount-zoomoutupcount
            zoomfactor=findzoomfactor(zoomfactor)
            maxid = findmaxxvalues(arrayOfUpperChannels)
            scrollbar.setMinimum(0)
            scrollbar.setMaximum(int(arrayOfUpperChannels[maxid].x_values[len(arrayOfUpperChannels[maxid].x_values)-1]*zoomfactor))
            scrollbar.setSingleStep(1)
            valueofhorizontal = scrollbar.value()
            viewportup.plotItem.setXRange((valueofhorizontal - 1)/zoomfactor, valueofhorizontal/zoomfactor)
    elif direction == "down":
        if len(arrayOfLowerChannels) == 0:
            return
        else:
            maxid = findmaxxvalues(arrayOfLowerChannels)
            zoomfactor=zoomindowncount-zoomoutdowncount
            zoomfactor=findzoomfactor(zoomfactor)
            scrollbar.setMinimum(0)
            scrollbar.setMaximum(int(arrayOfLowerChannels[maxid].x_values[len(arrayOfLowerChannels[maxid].x_values)-1]*zoomfactor))
            scrollbar.setSingleStep(1)
            valueofhorizontal = scrollbar.value()
            viewportdown.plotItem.setXRange((valueofhorizontal - 1)/zoomfactor, valueofhorizontal/zoomfactor)


def moveacrossy(self, viewportup, viewportdown, scrollbar, direction, linkcheck):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    if linkcheck.isChecked():
        if len(arrayOfUpperChannels) == 0 or len(arrayOfLowerChannels) == 0:
            return
        else:
            allvalues = arrayOfLowerChannels
            allvalues.extend(arrayOfUpperChannels)
            minmaxrange = findmaxminranges(allvalues)
            scrollbar.setMinimum(int(minmaxrange[2]))
            scrollbar.setMaximum(int(minmaxrange[3]))
            scrollbar.setSingleStep(1)
            valueofvertical = scrollbar.value()
            viewportup.plotItem.setYRange((valueofvertical - 1), valueofvertical)
            viewportdown.plotItem.setYRange((valueofvertical - 1), valueofvertical)
    elif direction == "up":
        if len(arrayOfUpperChannels) == 0:
            return
        else:
            minmaxrange = findmaxminranges(arrayOfUpperChannels)
            scrollbar.setMinimum(int(minmaxrange[2]))
            scrollbar.setMaximum(int(minmaxrange[3]))
            scrollbar.setSingleStep(1)
            valueofvertical = scrollbar.value()
            viewportup.plotItem.setYRange((valueofvertical - 1), valueofvertical)
    elif direction == "down":
        if len(arrayOfLowerChannels) == 0:
            return
        else:
            minmaxrange = findmaxminranges(arrayOfLowerChannels)
            scrollbar.setMinimum(int(minmaxrange[2]))
            scrollbar.setMaximum(int(minmaxrange[3]))
            scrollbar.setSingleStep(1)
            valueofvertical = scrollbar.value()
            viewportdown.plotItem.setYRange((valueofvertical - 1), valueofvertical)


def findmaxxvalues(arrayOfChannels):
    maxi = 0
    for index in range(len(arrayOfChannels)):
        if len(arrayOfChannels[index].x_values) != 0 and max(arrayOfChannels[index].x_values) > maxi and \
                arrayOfChannels[index].isMoved == False:
            maxi = max(arrayOfChannels[index].x_values)
            maxid = index

    return (maxid)


def Capture(self, direction, viewport):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    global isplayingup
    global isplayingdown
    global captured_images
    global mean_values
    global std_values
    global min_values
    global max_values
    global duration_values
    global statTables
    global channelNames
    if direction == 'up' and (not isplayingup):
        plot_image = viewport.grab()

        for i in range(len(arrayOfUpperChannels)):
            if arrayOfUpperChannels[i].isMoved == False and arrayOfUpperChannels[i].isHidden==False:
                mean_value = round(np.mean(arrayOfUpperChannels[i].amplitude), 2)
                std_deviation = round(np.std(arrayOfUpperChannels[i].amplitude), 2)
                min_val = round(np.min(arrayOfUpperChannels[i].amplitude), 2)
                max_val = round(np.max(arrayOfUpperChannels[i].amplitude), 2)
                duration = arrayOfUpperChannels[i].x_values[-1]
                channel_name = arrayOfUpperChannels[i].label

                mean_values.append(mean_value)
                std_values.append(std_deviation)
                min_values.append(min_val)
                max_values.append(max_val)
                duration_values.append(duration)
                channelNames.append(channel_name)

        statistics_df = {
            "channel": channelNames,
            "Mean": mean_values,
            "STD": std_values,
            "Min": min_values,
            "Max": max_values,
            "Duration": duration_values
        }
        df = pd.DataFrame(statistics_df)
        statTables.append(df)
        mean_values = []
        std_values = []
        min_values = []
        max_values = []
        duration_values = []
        channelNames = []
        # utility.clearTable()

        captured_images.append(plot_image)

    elif direction == 'down' and (not isplayingdown):
        plot_image = viewport.grab()

        for i in range(len(arrayOfLowerChannels)):
            if arrayOfLowerChannels[i].isMoved == False and arrayOfLowerChannels[i].isHidden==False:
                mean_value = round(np.mean(arrayOfLowerChannels[i].amplitude), 2)
                std_deviation = round(np.std(arrayOfLowerChannels[i].amplitude), 2)
                min_val = round(np.min(arrayOfLowerChannels[i].amplitude), 2)
                max_val = round(np.max(arrayOfLowerChannels[i].amplitude), 2)
                duration = arrayOfLowerChannels[i].x_values[-1]
                channel_name = arrayOfLowerChannels[i].label

                mean_values.append(mean_value)
                std_values.append(std_deviation)
                min_values.append(min_val)
                max_values.append(max_val)
                duration_values.append(duration)
                channelNames.append(channel_name)

        statistics_df = {
            "channel": channelNames,
            "Mean": mean_values,
            "STD": std_values,
            "Min": min_values,
            "Max": max_values,
            "Duration": duration_values
        }
        df = pd.DataFrame(statistics_df)
        statTables.append(df)
        mean_values = []
        std_values = []
        min_values = []
        max_values = []
        duration_values = []
        channelNames = []
        # utility.clearTable()

        captured_images.append(plot_image)


def exportToPdf(self):
    global statTables
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)", options=options)

    if file_path:
        pdf = FPDF()
        utility.coverPageTemplate(pdf)
        if(captured_images):
            pdf.add_page()
        pdf.set_font("Arial", size=10)

        image_width = 80
        x_left = 5
        x_right = 120
        y_top = 30
        cell_width = 17
        cell1_width = 25
        cell_height = 8
        y_bottom = 140

        for x, (image, statistics_df) in enumerate(zip(captured_images, statTables)):
            temp_image_path = f"plot_temp_{x}.png"
            image.save(temp_image_path, "PNG")

            if x % 2 == 0:
                if x != 0:
                    pdf.add_page()
                pdf.image(temp_image_path, x=x_left, y=y_top - 25, w=image_width)
                header = statTables[x].columns.tolist()

                table_x = 90
                table_y = 5  # Adjust the Y position as needed
                pdf.set_xy(table_x, table_y)
                for i, item in enumerate(header):
                    if i == 0:
                        pdf.cell(cell1_width, cell_height, str(item), 1)
                    else:
                        pdf.cell(cell_width, cell_height, str(item), 1)
                pdf.ln()
                pdf.set_font("Arial", size=8)
                for index, row in statTables[x].iterrows():
                    pdf.set_xy(table_x, pdf.get_y())
                    for i, item in enumerate(row):
                        if i == 0:
                            pdf.cell(cell1_width, cell_height, str(item), 1)
                        else:
                            pdf.cell(cell_width, cell_height, str(item), 1)
                    pdf.ln()

            else:
                pdf.image(temp_image_path, x=x_right, y=y_bottom - 20, w=image_width)

                # Print the corresponding DataFrame as a table
                header = statTables[x].columns.tolist()

                table_x = 10
                table_y = 125  # Adjust the Y position as needed
                pdf.set_xy(table_x, table_y)
                for i, item in enumerate(header):
                    if i == 0:
                        pdf.cell(cell1_width, cell_height, str(item), 1)
                    else:
                        pdf.cell(cell_width, cell_height, str(item), 1)
                pdf.ln()
                pdf.set_font("Arial", size=8)
                for index, row in statTables[x].iterrows():
                    pdf.set_xy(table_x, pdf.get_y())
                    for i, item in enumerate(row):
                        if i == 0:
                            pdf.cell(cell1_width, cell_height, str(item), 1)
                        else:
                            pdf.cell(cell_width, cell_height, str(item), 1)
                    pdf.ln()

            os.remove(temp_image_path)  # Remove the temporary image file

        pdf.output(file_path)

def refresh(array):
    for i in range(len(array)):
        array[i].plotRef.setData(array[i].x_values, array[i].y_values, pen=array[i].color, name=array[i].label, skipfinitecheck=True)
        

def findzoomfactor(zoomfactor):
    value=1
    if zoomfactor<0:
        for i in range(-zoomfactor):
            value=value/2
    elif zoomfactor==0:
        zoomfactor=1
    else:
        for i in range(zoomfactor):
            value=value*2
    return(value)