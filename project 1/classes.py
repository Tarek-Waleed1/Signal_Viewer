import numpy as np
import random
from pyqtgraph import PlotWidget

class channelLine():
    def __init__(self):
        self.time=[]
        self.amplitude=[]
        self.color=self.changecolor()
        self.isHidden=False
        self.label="Untitled"
        self.plotRef=PlotWidget()
        self.x_values=[]
        self.y_values=[]
        self.index=0
        self.timer = 0
        #check is moved
        self.isMoved=False
    # print(type(rancolor[0]))
        
    def changecolor(self):
        rancolor = list(np.random.choice(range(256), size=3))
        return rancolor

    def addValue(self):
        if len(self.y_values)==0:
            self.y_values.append(self.amplitude[0])
        else:
            if len(self.amplitude)>len(self.y_values):
                self.y_values.append(self.amplitude[len(self.y_values)])
            
        if len(self.x_values)==0:
            self.x_values.append(self.time[0])
        else:
            if len(self.time)>len(self.x_values):
                self.x_values.append(self.time[len(self.x_values)])
    
    def changeVisibility(self):
        if (self.isHidden==False):
            self.isHidden=True
            self.plotRef.hide()
        else:
            self.isHidden=False
            self.plotRef.show()
       
    def amIDone(self):
        if(len(self.x_values)==len(self.time)):
            return True
        else:
            return False
            
    def fillxvaluesandyvalues(self,number):
        self.x_values.extend(self.time[0:number])
        self.y_values.extend(self.amplitude[0:number])


            
        



