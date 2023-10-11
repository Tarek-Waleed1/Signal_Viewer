from PyQt5 import QtGui, QtCore, QtWidgets
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

arrayOfUpperChannels=[]
arrayOfLowerChannels=[]
zoomlevel=1
speedUp=1
speedDown=1
isplaying=True
# Function to handle the "Browse" button click event
def browseFiles(self, direction, graph,channel,control):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    self.filename,_ = QFileDialog.getOpenFileName(None, 'Open the signal file', './', filter="Raw Data(*.csv *.txt *.xls *.hea *.dat *.rec)")
    path = self.filename
    tempChl=channelLine()

    if self.filename:
        # Attempt to read the CSV file without specifying a header
        try:
            dataframe = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            # Handle the case when the CSV file is empty
            return
        except pd.errors.ParserError:
            # Handle the case when the CSV file has no header
            dataframe = pd.read_csv(path, header=None)
        
        if (channel.count()==0):
             channel.addItem('--Add Channels--')
             channel.addItem('Channel 1')
             
             if direction=='up':
              arrayOfUpperChannels.append(tempChl)
              arrayOfUpperChannels[0].label='channel 1'
              arrayOfUpperChannels[0].amplitude=dataframe.iloc[:, 1]
              arrayOfUpperChannels[0].time=dataframe.iloc[:, 0]
              plot_data(self, graph, arrayOfUpperChannels[0].time, arrayOfUpperChannels[0].amplitude,arrayOfUpperChannels[0].label,arrayOfUpperChannels[0],"up")
             else:
                arrayOfLowerChannels.append(tempChl)
                arrayOfLowerChannels[0].label='channel 1'
                arrayOfLowerChannels[0].amplitude=dataframe.iloc[:, 1]
                arrayOfLowerChannels[0].time=dataframe.iloc[:, 0]
                plot_data(self, graph, arrayOfLowerChannels[0].time, arrayOfLowerChannels[0].amplitude,arrayOfLowerChannels[0].label,arrayOfLowerChannels[0],"down")
        else:
            if channel.currentIndex()==0:                
                if direction=='up':
                    arrayOfUpperChannels.append(tempChl)
                    arrayOfUpperChannels[channel.count()-1].label=f'channel {channel.count()}'
                    arrayOfUpperChannels[channel.count()-1].amplitude=dataframe.iloc[:, 1]
                    arrayOfUpperChannels[channel.count()-1].time=dataframe.iloc[:, 0]
                    for i in range(len(arrayOfUpperChannels)):
                        arrayOfUpperChannels[i].x_values=[]
                        arrayOfUpperChannels[i].y_values=[]
                        arrayOfUpperChannels[i].plotRef.clear()
                    plot_data(self, graph, arrayOfUpperChannels[channel.count()-1].time, arrayOfUpperChannels[channel.count()-1].amplitude,arrayOfUpperChannels[channel.count()-1].label,arrayOfUpperChannels[channel.currentIndex()-1],"up")
                    channel.addItem(f'Channel {channel.count()}')
                else:
                    arrayOfLowerChannels.append(tempChl)
                    arrayOfLowerChannels[channel.count()-1].label=f'channel {channel.count()}'
                    arrayOfLowerChannels[channel.count()-1].amplitude=dataframe.iloc[:, 1]
                    arrayOfLowerChannels[channel.count()-1].time=dataframe.iloc[:, 0]
                    for i in range(len(arrayOfLowerChannels)):
                        arrayOfLowerChannels[i].x_values=[]
                        arrayOfLowerChannels[i].y_values=[]
                        arrayOfLowerChannels[i].plotRef.clear()
                    plot_data(self, graph,arrayOfLowerChannels[channel.count()-1].time, arrayOfLowerChannels[channel.count()-1].amplitude,arrayOfLowerChannels[channel.count()-1].label,arrayOfLowerChannels[channel.currentIndex()-1],"down")
                    channel.addItem(f'Channel {channel.count()}')
            else:
                if direction=='up':
                    arrayOfUpperChannels[channel.currentIndex()-1].label=f'channel {channel.currentIndex()}'
                    arrayOfUpperChannels[channel.currentIndex()-1].amplitude=dataframe.iloc[:, 1]
                    arrayOfUpperChannels[channel.currentIndex()-1].time=dataframe.iloc[:, 0]
                    for i in range(len(arrayOfUpperChannels)):
                        arrayOfUpperChannels[i].x_values=[]
                        arrayOfUpperChannels[i].y_values=[]
                        arrayOfUpperChannels[i].plotRef.clear()
                    plot_data(self, graph,arrayOfUpperChannels[channel.currentIndex()-1].time, arrayOfUpperChannels[channel.currentIndex()-1].amplitude,arrayOfUpperChannels[channel.currentIndex()-1].label,arrayOfUpperChannels[channel.currentIndex()-1],'up')
                    
                else:
                    arrayOfLowerChannels[channel.currentIndex()-1].label=f'channel {channel.currentIndex()}'
                    arrayOfLowerChannels[channel.currentIndex()-1].amplitude=dataframe.iloc[:, 1]
                    arrayOfLowerChannels[channel.currentIndex()-1].time=dataframe.iloc[:, 0]
                    for i in range(len(arrayOfLowerChannels)):
                        arrayOfLowerChannels[i].x_values=[]
                        arrayOfLowerChannels[i].y_values=[]
                        arrayOfLowerChannels[i].plotRef.clear()
                    plot_data(self, graph, arrayOfLowerChannels[channel.currentIndex()-1].time, arrayOfLowerChannels[channel.currentIndex()-1].amplitude,arrayOfLowerChannels[channel.currentIndex()-1].label,arrayOfLowerChannels[channel.currentIndex()-1],'down')


        

def plot_data(self, viewport, x, y,names,smth,direction):
        Minx = 0
        Maxx = 0
        Miny = 0
        Maxy = 0
        rancolor = list(np.random.choice(range(256), size=3))
        smth.color=rancolor
        viewport.addLegend()
        smth.plotRef = viewport.plot(x, y, pen=rancolor,name=smth.label)
        smth.plotRef.clear()
        if direction=="up":
            theranges=findmaxminranges(arrayOfUpperChannels,Minx,Maxx,Miny,Maxy)
        else:
            theranges=findmaxminranges(arrayOfLowerChannels,Minx,Maxx,Miny,Maxy)
        viewport.setLimits(xMin=theranges[0], xMax=theranges[1], yMin=theranges[2], yMax=theranges[3])
        smth.timer=QtCore.QTimer()
        smth.timer.setInterval(50)
        smth.timer.timeout.connect(partial(update_plot_data, x, y,viewport,smth,self,direction))
        if (isplaying == True):
            smth.timer.start()


def update_plot_data(x,y,viewport,smth,self,direction):
    smth.addValue()
    global speedUp
    global speedDown
    global speedUpDown
    if direction =="up":
        smth.timer.setInterval(int(50/speedUp))
    else:
        smth.timer.setInterval(int(50/speedDown))
    smth.plotRef.setData(smth.x_values, smth.y_values,pen=smth.color, name=smth.label,skipfinitecheck=True)

             
             
             
def zoominfunc(self,direction,viewup,viewdown,linkingcondition):
    zoom=(0.5,0.5)
    if direction=="up":
       viewup.plotItem.getViewBox().scaleBy(zoom)    
       if linkingcondition.isChecked():
           viewdown.plotItem.getViewBox().scaleBy(zoom)
    else:
         viewdown.plotItem.getViewBox().scaleBy(zoom)    
         if linkingcondition.isChecked():
             viewup.plotItem.getViewBox().scaleBy(zoom)   
    


def zoomoutfunc(self,direction,viewup,viewdown,linkingcondition):
    global zoomlevel
    zoomlevel=zoomlevel*2
    zoom=(2,2)
    if direction=="up":
       viewup.plotItem.getViewBox().scaleBy(zoom)    
       if linkingcondition.isChecked():
           viewdown.plotItem.getViewBox().scaleBy(zoom)
    else:
         viewdown.plotItem.getViewBox().scaleBy(zoom)    
         if linkingcondition.isChecked():
             viewup.plotItem.getViewBox().scaleBy(zoom)
     


def sliderValueChanged(numberu,numberd,slider,isLinked,direction):
    value=slider.value()/10
    global speedUp
    global speedDown
    if isLinked.isChecked():
        numberu.setText(str(value))
        numberd.setText(str(value))
        slider.setValue(slider.value())
        speedUp=value
        speedDown=value
    elif direction=='up':
        numberu.setText(str(value))
        speedUp=value
    else:
        numberd.setText(str(value))
        speedDown=value


def changeVisibility(direction,channel,check):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    if direction=='up' and channel.currentIndex()>0:
        arrayOfUpperChannels[channel.currentIndex()-1].changeVisibility(check.isChecked())
    elif direction=='down' and channel.currentIndex()>0:
        arrayOfLowerChannels[channel.currentIndex()-1].changeVisibility(check.isChecked())


def changcolors(direction,channel):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    choicecolor=QColorDialog.getColor()
    if direction=="up" and channel.currentIndex()>0:
        arrayOfUpperChannels[channel.currentIndex()-1].color=choicecolor
    elif direction=="down" and channel.currentIndex()>0:
        arrayOfLowerChannels[channel.currentIndex()-1].color=choicecolor
    else:
        return()


def changeLineName(direction, channel,newName,control):
    global arrayOfUpperChannels
    global arrayOfLowerChannels
    if direction=="up" and channel.currentIndex()>0:
        control.removeItem(arrayOfUpperChannels[channel.currentIndex()-1].label)
        arrayOfUpperChannels[channel.currentIndex()-1].label=newName
        control.addItem(arrayOfUpperChannels[channel.currentIndex()-1].plotRef,newName)
    elif direction=="down" and channel.currentIndex()>0:
        control.removeItem(arrayOfLowerChannels[channel.currentIndex()-1].label)
        arrayOfLowerChannels[channel.currentIndex()-1].label=newName
        control.addItem(arrayOfLowerChannels[channel.currentIndex()-1].plotRef,newName)
    else:
        return()
    # print(newName)
    
    
def pauseplay(self, direction):
    
    global isplaying
    if(direction=='up'):
        if(isplaying==True):
            isplaying=False
            for i in range(len(arrayOfUpperChannels)):
                arrayOfUpperChannels[i].timer.stop()
        else:
            isplaying=True
            for i in range(len(arrayOfUpperChannels)):
                arrayOfUpperChannels[i].timer.start()
    else:
        if (isplaying == True):
            isplaying = False
            for i in range(len(arrayOfLowerChannels)):
                arrayOfLowerChannels[i].timer.stop()
        else:
            isplaying = True
            for i in range(len(arrayOfLowerChannels)):
                arrayOfLowerChannels[i].timer.start()    
    
    
    
    
    
#Gets min max for ranges used in plot
def findmaxminranges(signalarray,Minx,Maxx,Miny,Maxy): 
    
    for index in range(len(signalarray)):
        if len(signalarray[index].time)!=0 and max(signalarray[index].time)>Maxx:
            Maxx=max(signalarray[index].time)
        if len(signalarray[index].time)!=0 and min(signalarray[index].time)<Minx:
            Minx=min(signalarray[index].time)    
        if len(signalarray[index].amplitude)!=0 and max(signalarray[index].amplitude)>Maxy:
            Maxy=max(signalarray[index].amplitude)
        if len(signalarray[index].amplitude)!=0 and min(signalarray[index].amplitude)<Miny:
            Miny=min(signalarray[index].amplitude)
    return([Minx,Maxx,Miny,Maxy])
    
    
def rewindfunc(self,direction):

    if (direction == 'up' and arrayOfUpperChannels !=[]):
        for i in range(len(arrayOfUpperChannels)):
            if arrayOfUpperChannels[i].amIDone():
                continue
            else:
                return
        for i in range(len(arrayOfUpperChannels)):
            arrayOfUpperChannels[i].x_values = []
            arrayOfUpperChannels[i].y_values = []
            arrayOfUpperChannels[i].plotRef.clear()
    elif(direction == 'down' and arrayOfLowerChannels !=[]):
        for i in range(len(arrayOfLowerChannels)):
            if arrayOfLowerChannels[i].amIDone():
                continue
            else:
                return
        for i in range(len(arrayOfLowerChannels)):
            arrayOfLowerChannels[i].x_values = []
            arrayOfLowerChannels[i].y_values = []
            arrayOfLowerChannels[i].plotRef.clear()    
            
            
            
            
            
# def changegraphsfunc(self,direction,channelup,channeldown,viewup,viewdown):
#     global arrayOfUpperChannels
#     global arrayOfLowerChannels
#     dummyline=channelLine()
#     if direction=='up' and channelup.count!=0 and channelup.currentIndex() > 0:
#         if channeldown.count==0:
#             channeldown.addItem('--Add Channels--')
#             channeldown.addItem('Channel 1')
#             arrayOfUpperChannels[channeldown.currentIndex()-1].timer.stop()
#             arrayOfUpperChannels[channeldown.currentIndex()-1].plotRef.clear()
#             arrayOfLowerChannels.append(arrayOfUpperChannels[channeldown.currentIndex()-1])
#             arrayOfUpperChannels[channelup.currentIndex()-1]=dummyline
#             for i in range(len(arrayOfLowerChannels)):
#                 arrayOfLowerChannels[i].x_values=[]
#                 arrayOfLowerChannels[i].y_values=[]
#                 arrayOfLowerChannels[i].plotRef.clear()
#             plot_data(self, viewdown, arrayOfLowerChannels[0].time, arrayOfLowerChannels[0].amplitude, arrayOfLowerChannels[0].label, arrayOfLowerChannels[0] , direction)
#         else:
#             channeldown.addItem(f'Channel {channeldown.count()}')
#             arrayOfUpperChannels[channeldown.currentIndex()-1].timer.stop()
#             arrayOfUpperChannels[channeldown.currentIndex()-1].plotRef.clear()
#             arrayOfLowerChannels.append(arrayOfUpperChannels[channeldown.currentIndex()-1])
#             arrayOfUpperChannels[channeldown.currentIndex()-1]=dummyline
#             for i in range(len(arrayOfLowerChannels)):
#                 arrayOfLowerChannels[i].x_values=[]
#                 arrayOfLowerChannels[i].y_values=[]
#                 arrayOfLowerChannels[i].plotRef.clear()
#             plot_data(self, viewdown, arrayOfLowerChannels[-1].time, arrayOfLowerChannels[-1].amplitude, arrayOfLowerChannels[-1].label, arrayOfLowerChannels[-1] , direction)
#     elif direction=='down' and channeldown.count!=0 and channeldown.currentIndex() > 0:
#          if channelup.count==0:
#              channelup.addItem('--Add Channels--')
#              channelup.addItem('Channel 1')
#              arrayOfLowerChannels[channeldown.currentIndex()-1].timer.stop()
#              arrayOfLowerChannels[channeldown.currentIndex()-1].plotRef.clear()
#              arrayOfUpperChannels.append(arrayOfUpperChannels[channelup.currentIndex()-1])
#              arrayOfLowerChannels[channeldown.currentIndex()-1]=dummyline
#              for i in range(len(arrayOfUpperChannels)):
#                  arrayOfUpperChannels[i].x_values=[]
#                  arrayOfUpperChannels[i].y_values=[]
#                  arrayOfUpperChannels[i].plotRef.clear()
#              plot_data(self, viewup, arrayOfUpperChannels[0].time, arrayOfUpperChannels[0].amplitude, arrayOfUpperChannels[0].label, arrayOfUpperChannels[0] , direction)
#          else:
#              channelup.addItem(f'Channel {channelup.count()}')
#              arrayOfLowerChannels[channeldown.currentIndex()-1].timer.stop()
#              arrayOfLowerChannels[channeldown.currentIndex()-1].plotRef.clear()
#              arrayOfUpperChannels.append(arrayOfLowerChannels[channeldown.currentIndex()-1])
#              arrayOfLowerChannels[channeldown.currentIndex()-1]=dummyline   
#              for i in range(len(arrayOfUpperChannels)):
#                  arrayOfUpperChannels[i].x_values=[]
#                  arrayOfUpperChannels[i].y_values=[]
#                  arrayOfUpperChannels[i].plotRef.clear()
#              plot_data(self, viewdown, arrayOfUpperChannels[-1].time, arrayOfUpperChannels[-1].amplitude, arrayOfUpperChannels[-1].label, arrayOfUpperChannels[-1] , direction)
        