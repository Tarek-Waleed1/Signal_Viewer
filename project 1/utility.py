import csv
import pandas as pd
import functions
from fpdf import FPDF

def read_csv_file(path):
    datContent = [i.strip().split() for i in open(path).readlines()]
    with open(path, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(datContent)
    return pd.read_csv(path)

def add_channel(self,dataframe, direction, graph, channel, control, arrayOfUpperChannels, arrayOfLowerChannels, tempChl):
    if channel.count() == 0:
        channel.addItem('--Add Channels--')
        channel.addItem('channel 1')
        if direction == 'up':
            channels = arrayOfUpperChannels
        else:
            channels = arrayOfLowerChannels
        channels.append(tempChl)
        channels[0].label = 'channel 1'
        channels[0].amplitude = dataframe.iloc[:, 1]
        channels[0].time = dataframe.iloc[:, 0]
        functions.plot_data(self,graph, channels[0].time, channels[0].amplitude, channels[0].label, channels[0], direction)
    else:
        if channel.currentIndex() == 0:
            channels = arrayOfUpperChannels if direction == 'up' else arrayOfLowerChannels
            add_new_channel(self,dataframe, channels, direction, graph, channel, control, tempChl)
        else:
            update_channel(self,dataframe, direction, channel, graph, control, arrayOfUpperChannels, arrayOfLowerChannels)



def add_new_channel(self,dataframe, channels, direction, graph, channel, control,tempChl):
    index = functions.numberoffilledarray(channels)
    if index != -1:
        index_of_moved = functions.isMoved(channels)
        if index_of_moved != -1:
            channels[index_of_moved].amplitude = dataframe.iloc[:, 1]
            channels[index_of_moved].time = dataframe.iloc[:, 0]
            channels[index_of_moved].x_values = []
            channels[index_of_moved].y_values = []
            channels[index_of_moved].isMoved = False
            channels[index_of_moved].fillxvaluesandyvalues(len(channels[index].x_values))
            functions.plot_data(self,graph, channels[index_of_moved].time, channels[index_of_moved].amplitude, channels[index_of_moved].label, channels[index_of_moved], direction)
            channels[channel.currentIndex() - 1].plotRef.setData(channels[channel.currentIndex() - 1].x_values, channels[channel.currentIndex() - 1].y_values, pen=channels[channel.currentIndex() - 1].color, name=channels[channel.currentIndex() - 1].label, skipfinitecheck=True)
        else:
            add_new_channel_instance(self,dataframe, channels, direction, index, graph, channel, control,tempChl)
            channel.addItem(f'channel {channel.count()}')
    else:
        add_new_channel_instance(self,dataframe, channels, direction, 0, graph, channel, control,tempChl)
        channel.addItem(f'channel {channel.count()}')


def add_new_channel_instance(self,dataframe, channels, direction, index, graph, channel, control, tempChl):
    channels.append(tempChl)
    channels[channel.count() - 1].label = f'channel {channel.count()}'
    channels[channel.count() - 1].amplitude = dataframe.iloc[:, 1]
    channels[channel.count() - 1].time = dataframe.iloc[:, 0]
    channels[channel.count() - 1].fillxvaluesandyvalues(len(channels[0].x_values))
    functions.plot_data(self,graph, channels[channel.count() - 1].time, channels[channel.count() - 1].amplitude, channels[channel.count() - 1].label, channels[channel.currentIndex() - 1], direction)
    channels[channel.currentIndex() - 1].plotRef.setData(channels[channel.currentIndex() - 1].x_values, channels[channel.currentIndex() - 1].y_values, pen=channels[channel.currentIndex() - 1].color, name=channels[channel.currentIndex() - 1].label, skipfinitecheck=True)

def update_channel(self,dataframe, direction, channel, graph, control, arrayOfUpperChannels, arrayOfLowerChannels):
    channels = arrayOfUpperChannels if direction == 'up' else arrayOfLowerChannels
    index = channel.currentIndex() - 1
    if channels[index].isMoved:
        channels[index].isMoved = False
    length_x = len(channels[0].x_values)
    control.removeItem(channels[index].label)
    channels[index].label = f'channel {channel.currentIndex()}'
    channels[index].amplitude = dataframe.iloc[:, 1]
    channels[index].time = dataframe.iloc[:, 0]
    channels[index].x_values = []
    channels[index].y_values = []
    channels[index].plotRef.clear()
    if channel.count() == 2:
        functions.plot_data(self,graph, channels[index].time, channels[index].amplitude, channels[index].label, channels[index], direction)
        channels[index].plotRef.setData(channels[index].x_values, channels[index].y_values, pen=channels[index].color, name=channels[index].label, skipfinitecheck=True)
    else:
        if channel.currentIndex() == 1:
            channels[0].fillxvaluesandyvalues(length_x)
            functions.plot_data(self,graph, channels[index].time, channels[index].amplitude, channels[index].label, channels[index], direction)
            channels[index].plotRef.setData(channels[index].x_values, channels[index].y_values, pen=channels[index].color, name=channels[index].label, skipfinitecheck=True)
        else:
            index_of_available_line = functions.numberoffilledarray(channels)
            channels[index].fillxvaluesandyvalues(len(channels[index_of_available_line].x_values))
            functions.plot_data(self,graph, channels[index].time, channels[index].amplitude, channels[index].label, channels[index], direction)
            channels[index].plotRef.setData(channels[index].x_values, channels[index].y_values, pen=channels[index].color, name=channels[index].label, skipfinitecheck=True)


def coverPageTemplate(pdf):
    # pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    # Add new page. Without this you cannot create the document
    pdf.add_page()

    # Style of the pdf
    pdf.set_font('Arial', 'B', 20)
    pdf.set_xy(70, (pdf.h - 90) / 2)
    pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')
    pdf.set_font('Arial', 'B', 15)
    pdf.ln()
    pdf.cell(70)
    pdf.cell(50, 10, 'Report to:')
    pdf.ln()
    pdf.cell(70)
    pdf.cell(50, 10, 'Dr.Tamer Basha')
    pdf.ln()
    pdf.cell(70)
    pdf.cell(50, 10, 'Eng.Christina Adly')
    pdf.ln()
    pdf.ln()
    pdf.cell(20)
    pdf.cell(50, 10, 'Team members:')
    pdf.ln()
    pdf.cell(20)
    pdf.cell(50, 10, 'Tarek Waleed Fathy')
    pdf.ln()
    pdf.cell(20)
    pdf.cell(50, 10, 'Youssef Ahmed Afify')
    pdf.ln()
    pdf.cell(20)
    pdf.cell(50, 10, 'Youssef Ahmed Mohamed')
    pdf.ln()
    pdf.cell(20)
    pdf.cell(50, 10, 'Mohamed Tamer')
    # insert the logos
    pdf.image('CUFE.png', 1, 1, 50, 40)
    pdf.image('OIP.jpeg', 160, 1, 50, 40)

 

# def clearTable():
#     functions.mean_values=[]
#     functions.std_values=[]
#     functions.min_values=[]
#     functions.duration_values=[]
#     functions.channelNames=[]