from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton
import functions
from mplwidget import MplWidget
import pyqtgraph
from classes import channelLine




def initConnectors(self):
    # Upper Channel Selector
    upperChannelSelector=self.findChild(QtWidgets.QComboBox , "channelSelectorUp") 

    # LowerChannel Selector
    LowerChannelSelector=self.findChild(QtWidgets.QComboBox , "channelSelectorDown") 

    # Find upper Graph
    upperViewPort = self.findChild(pyqtgraph.PlotWidget, "ViewPortUp")
    upperlegendcontrol=upperViewPort.addLegend()
    upperViewPort.getViewBox().setAutoPan(x=True,y=True)
    # Find Lower Graph
    lowerViewPort = self.findChild(pyqtgraph.PlotWidget, "viewPortDown")
    lowerlegendcontrol=lowerViewPort.addLegend()
    lowerViewPort.getViewBox().setAutoPan(x=True,y=True)
    
    
    #find upper browse button
    browseupbtn = self.findChild(QtWidgets.QPushButton, "browseFilesUp")
    browseupbtn.clicked.connect(lambda: functions.browseFiles(self,"up",upperViewPort, upperChannelSelector,upperlegendcontrol))
    
    #find lower browse button
    browsedownbtn = self.findChild(QtWidgets.QPushButton, "browseFilesDown")
    browsedownbtn.clicked.connect(lambda: functions.browseFiles(self,"down",lowerViewPort, LowerChannelSelector,lowerlegendcontrol))
    
    
    #find upper pauseplay button
    pauseplayupbtn = self.findChild(QtWidgets.QPushButton,"pausePlayUp")
    pauseplayupbtn.clicked.connect(lambda: functions.pauseplay(self,"up"))
    
    #find lower pauseplay button
    pauseplaydownbtn = self.findChild(QtWidgets.QPushButton,"pausePlayDown")
    pauseplaydownbtn.clicked.connect(lambda: functions.pauseplay(self,"down"))
    
    #find upper rewind
    rewindupbtn = self.findChild(QtWidgets.QPushButton, "rewindUp")
    rewindupbtn.clicked.connect(lambda: functions.rewindfunc(self,"up"))
    
    #find lower rewind
    rewinddownbtn = self.findChild(QtWidgets.QPushButton, "rewindDown")
    rewinddownbtn.clicked.connect(lambda: functions.rewindfunc(self,"down"))
    
    
    #find move to other graph upper button
    changegraphsup=self.findChild(QPushButton, "moveToOtherGraphUp" )
    changegraphsup.clicked.connect(lambda: functions.changegraphsfunc(self,"up",upperChannelSelector,LowerChannelSelector,upperViewPort,lowerViewPort))
    
    
    #find move to other graph lower button
    changegraphsdown=self.findChild(QPushButton, "moveToOtherGraphDown" )
    changegraphsdown.clicked.connect(lambda: functions.changegraphsfunc(self,"down",upperChannelSelector,LowerChannelSelector,upperViewPort,lowerViewPort))
    
    
    #find zoom in upper
    zoominginup=self.findChild(QPushButton,"zoomInUp")
    zoominginup.clicked.connect(lambda: functions.zoominfunc(self,"up",upperViewPort,lowerViewPort,islinked))
    
    
    #find zoom in lower
    zoomingindown=self.findChild(QPushButton,"zoomInDown")
    zoomingindown.clicked.connect(lambda: functions.zoominfunc(self,"down",upperViewPort,lowerViewPort,islinked))
    
    #find zoom out upper
    zoomingoutup=self.findChild(QPushButton,"zoomOutUp")
    zoomingoutup.clicked.connect(lambda: functions.zoomoutfunc(self,"up",upperViewPort,lowerViewPort,islinked))
    
    #find zoom out lower
    zoomingoutdown=self.findChild(QPushButton,"zoomOutDown")
    zoomingoutdown.clicked.connect(lambda: functions.zoomoutfunc(self,"down",upperViewPort,lowerViewPort,islinked))
    
    #find extract lower
    extractiondown=self.findChild(QPushButton,"extractDown")
    extractiondown.clicked.connect(lambda: functions.exportToPdf(self,"down"))
    
    
    # select color upper
    colorchangeup=self.findChild(QPushButton, "colorSelectorUp")
    colorchangeup.clicked.connect(lambda: functions.changcolors("up",upperChannelSelector))
   
    
    # select color lower
    colorchangedown=self.findChild(QPushButton, "selectColorDown")
    colorchangedown.clicked.connect(lambda: functions.changcolors("down",LowerChannelSelector))
        
    # Capture Signal upper btn
    topCaptureBtn=self.findChild(QPushButton, "captureSignalUp")
    topCaptureBtn.clicked.connect(lambda: functions.handleUpperCapture(self,"up"))

    # Capture Signal lower btn
    lowerCaptureBtn=self.findChild(QPushButton, "captureSignalDown")
    lowerCaptureBtn.clicked.connect(lambda: functions.handleLowerCapture(self,"up"))
    
    
    #linking checknox
    islinked=self.findChild(QtWidgets.QCheckBox,"linkingGraphs")

    #Cine Speed Label Up
    cineNumberUp=self.findChild(QtWidgets.QLabel, "cineSpeedNumberUp")
    cineNumberUp.setText("1.0")

    #Cine Speed Label Down
    cineNumberDown=self.findChild(QtWidgets.QLabel, "cineSpeedNumberDown")
    cineNumberDown.setText("1.0")

    #Cine Speed Slider Up
    cineSliderUp=self.findChild(QtWidgets.QSlider, "cineSpeedSelectorUp")
    
    #Cine Speed Slider Down
    cineSliderDown=self.findChild(QtWidgets.QSlider, "cineSpeedSelectorDown")

    #Setting Initial states for the Cine Speed Slider Up
    cineSliderUp.setMinimum(10)         # Set minimum value to 1
    cineSliderUp.setMaximum(20)        # Set maximum value to 20 (which is 2 multiplied by 10)
    cineSliderUp.setValue(10)          # Set an initial value (10 corresponds to 1.0)
    cineSliderUp.setTickInterval(1)  

    #Setting Initial states for the Cine Speed Slider Down
    cineSliderDown.setMinimum(10)         # Set minimum value to 1
    cineSliderDown.setMaximum(20)        # Set maximum value to 20 (which is 2 multiplied by 10)
    cineSliderDown.setValue(10)          # Set an initial value (10 corresponds to 1.0)
    cineSliderDown.setTickInterval(1)  
    
    #Connecting the Slider to function
    cineSliderUp.valueChanged.connect(lambda: functions.sliderValueChanged(cineNumberUp,cineNumberDown,cineSliderUp,islinked,"up"))

    cineSliderDown.valueChanged.connect(lambda: functions.sliderValueChanged(cineNumberUp,cineNumberDown,cineSliderDown,islinked,"down"))

    #connecting the upper hide checkbox to the hide function
    isVisibleUp=self.findChild(QtWidgets.QCheckBox,'hideGraphUp')
    isVisibleUp.stateChanged.connect(lambda: functions.changeVisibility('up',upperChannelSelector,isVisibleUp))

    
    #connecting the lower hide checkbox to the hide function
    isVisibleDown=self.findChild(QtWidgets.QCheckBox,'hideGraphDown')
    isVisibleDown.stateChanged.connect(lambda: functions.changeVisibility('down',LowerChannelSelector,isVisibleDown))

   #Update label Name up
    lineNameUp=self.findChild(QtWidgets.QLineEdit,'customSignalNameUp')
    lineNameUp.returnPressed.connect(lambda: functions.changeLineName('up',upperChannelSelector,lineNameUp.text(),upperlegendcontrol))
    lineNameUp.returnPressed.connect(lineNameUp.clear)

    #Update line Name Down
    lineNameDown=self.findChild(QtWidgets.QLineEdit,'customSignalNameDown')
    lineNameDown.returnPressed.connect(lambda: functions.changeLineName('down',LowerChannelSelector,lineNameDown.text(),lowerlegendcontrol))
    lineNameDown.returnPressed.connect(lineNameDown.clear)


    
    

