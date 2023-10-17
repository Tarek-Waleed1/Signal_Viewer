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
    upperViewPort.plotItem.getViewBox().scaleBy((0,100))
    # upperViewPort.getViewBox().scaleBy((0.3,1))
    # Find Lower Graph
    lowerViewPort = self.findChild(pyqtgraph.PlotWidget, "viewPortDown")
    lowerlegendcontrol=lowerViewPort.addLegend()
    lowerViewPort.getViewBox().setAutoPan(x=True,y=True)
    lowerViewPort.plotItem.getViewBox().scaleBy((0,100))
    # lowerViewPort.getViewBox().scaleBy((0.3,1))
    
    
    #find upper browse button
    browseupbtn = self.findChild(QtWidgets.QPushButton, "browseFilesUp")
    browseupbtn.clicked.connect(lambda: functions.browseFiles(self,"up",upperViewPort, upperChannelSelector,upperlegendcontrol))
    
    #find lower browse button
    browsedownbtn = self.findChild(QtWidgets.QPushButton, "browseFilesDown")
    browsedownbtn.clicked.connect(lambda: functions.browseFiles(self,"down",lowerViewPort, LowerChannelSelector,lowerlegendcontrol))
    
    
    #find upper pauseplay button
    pauseplayupbtn = self.findChild(QtWidgets.QPushButton,"pausePlayUp")
    pauseplayupbtn.clicked.connect(lambda: functions.pauseplay(self,"up",islinked))
    
    #find lower pauseplay button
    pauseplaydownbtn = self.findChild(QtWidgets.QPushButton,"pausePlayDown")
    pauseplaydownbtn.clicked.connect(lambda: functions.pauseplay(self,"down",islinked))
    
    #find upper rewind
    rewindupbtn = self.findChild(QtWidgets.QPushButton, "rewindUp")
    rewindupbtn.clicked.connect(lambda: functions.rewindfunction(self,"up",upperViewPort))
    
    #find lower rewind
    rewinddownbtn = self.findChild(QtWidgets.QPushButton, "rewindDown")
    rewinddownbtn.clicked.connect(lambda: functions.rewindfunction(self,"down",lowerViewPort))
    
    
    #find move to other graph upper button
    changegraphsup=self.findChild(QPushButton, "moveToOtherGraphUp" )
    changegraphsup.clicked.connect(lambda: functions.changegraphsfunction(self,"up",upperChannelSelector,LowerChannelSelector,upperViewPort,lowerViewPort,upperlegendcontrol))
    
    
    #find move to other graph lower button
    changegraphsdown=self.findChild(QPushButton, "moveToOtherGraphDown" )
    changegraphsdown.clicked.connect(lambda: functions.changegraphsfunction(self,"down",upperChannelSelector,LowerChannelSelector,upperViewPort,lowerViewPort,lowerlegendcontrol))
    
    
    #find zoom in upper
    zoominginup=self.findChild(QPushButton,"zoomInUp")
    zoominginup.clicked.connect(lambda: functions.zoominfunction(self,"up",upperViewPort,lowerViewPort,islinked))
    
    
    #find zoom in lower
    zoomingindown=self.findChild(QPushButton,"zoomInDown")
    zoomingindown.clicked.connect(lambda: functions.zoominfunction(self,"down",upperViewPort,lowerViewPort,islinked))
    
    #find zoom out upper
    zoomingoutup=self.findChild(QPushButton,"zoomOutUp")
    zoomingoutup.clicked.connect(lambda: functions.zoomoutfunction(self,"up",upperViewPort,lowerViewPort,islinked))
    
    #find zoom out lower
    zoomingoutdown=self.findChild(QPushButton,"zoomOutDown")
    zoomingoutdown.clicked.connect(lambda: functions.zoomoutfunction(self,"down",upperViewPort,lowerViewPort,islinked))
    
    #find extract lower
    extractiondown=self.findChild(QPushButton,"extractDown")
    extractiondown.clicked.connect(lambda: functions.exportToPdf(self))
    
    
    # select color upper
    colorchangeup=self.findChild(QPushButton, "colorSelectorUp")
    colorchangeup.clicked.connect(lambda: functions.changcolors("up",upperChannelSelector))
   
    
    # select color lower
    colorchangedown=self.findChild(QPushButton, "selectColorDown")
    colorchangedown.clicked.connect(lambda: functions.changcolors("down",LowerChannelSelector))
        
    # Capture Signal upper btn
    topCaptureBtn=self.findChild(QPushButton, "captureSignalUp")
    topCaptureBtn.clicked.connect(lambda: functions.Capture(self,"up",upperViewPort))

    # Capture Signal lower btn
    lowerCaptureBtn=self.findChild(QPushButton, "captureSignalDown")
    lowerCaptureBtn.clicked.connect(lambda: functions.Capture(self,"down",lowerViewPort))
    
    
    #linking checknox
    islinked=self.findChild(QtWidgets.QCheckBox,"linkingGraphs")
    islinked.stateChanged.connect(lambda: functions.handleLinkGraphs(self, islinked,cineNumberUp,cineNumberDown,cineSliderUp,cineSliderDown))
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
    cineSliderUp.setMaximum(100)        # Set maximum value to 20 (which is 2 multiplied by 10)
    cineSliderUp.setValue(10)          # Set an initial value (10 corresponds to 1.0)
    cineSliderUp.setTickInterval(1)  

    #Setting Initial states for the Cine Speed Slider Down
    cineSliderDown.setMinimum(10)         # Set minimum value to 1
    cineSliderDown.setMaximum(100)        # Set maximum value to 20 (which is 2 multiplied by 10)
    cineSliderDown.setValue(10)          # Set an initial value (10 corresponds to 1.0)
    cineSliderDown.setTickInterval(1)  
    
    #Connecting the Slider to function
    cineSliderUp.valueChanged.connect(lambda: functions.sliderValueChanged(cineNumberUp,cineNumberDown,cineSliderUp,islinked,"up"))

    cineSliderDown.valueChanged.connect(lambda: functions.sliderValueChanged(cineNumberUp,cineNumberDown,cineSliderDown,islinked,"down"))

    #connecting the upper hide checkbox to the hide function
    isVisibleUp=self.findChild(QtWidgets.QPushButton,'hideGraphUp')
    isVisibleUp.clicked.connect(lambda: functions.changeVisibility('up',upperChannelSelector))

    
    #connecting the lower hide checkbox to the hide function
    isVisibleDown=self.findChild(QtWidgets.QPushButton,'hideGraphDown')
    isVisibleDown.clicked.connect(lambda: functions.changeVisibility('down',LowerChannelSelector))

   #Update label Name up
    lineNameUp=self.findChild(QtWidgets.QLineEdit,'customSignalNameUp')
    lineNameUp.returnPressed.connect(lambda: functions.changeLineName('up',upperChannelSelector,lineNameUp.text(),upperlegendcontrol))
    lineNameUp.returnPressed.connect(lineNameUp.clear)

    #Update line Name Down
    lineNameDown=self.findChild(QtWidgets.QLineEdit,'customSignalNameDown')
    lineNameDown.returnPressed.connect(lambda: functions.changeLineName('down',LowerChannelSelector,lineNameDown.text(),lowerlegendcontrol))
    lineNameDown.returnPressed.connect(lineNameDown.clear)


    Horizontalpanup=self.findChild(QtWidgets.QScrollBar,"horizontalSlidingUp")
    Horizontalpanup.valueChanged.connect(lambda: functions.moveacrossx(self,upperViewPort,lowerViewPort,Horizontalpanup,"up",islinked))
    
    Horizontalpandown=self.findChild(QtWidgets.QScrollBar,"horizontalSlidingDown")
    Horizontalpandown.valueChanged.connect(lambda: functions.moveacrossx(self,upperViewPort,lowerViewPort,Horizontalpandown,"down",islinked))
    
    verticalpanup=self.findChild(QtWidgets.QScrollBar,"verticalSlidingUp")
    verticalpanup.valueChanged.connect(lambda: functions.moveacrossy(self,upperViewPort,lowerViewPort,verticalpanup,"up",islinked))
    
    verticalpandown=self.findChild(QtWidgets.QScrollBar,"verticalSlidingDown")
    verticalpandown.valueChanged.connect(lambda: functions.moveacrossy(self,upperViewPort,lowerViewPort,verticalpandown,"down",islinked))
