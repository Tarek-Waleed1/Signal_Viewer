import pyqtgraph as pg

# Create a QApplication and PlotWidget
pg.mkQApp()
pw = pg.PlotWidget()

# Add a legend
legend = pw.addLegend()

# Add a ScatterPlotItem
scatter = pg.ScatterPlotItem([0, 1, 2], [0, 1, 2], name='test')
pw.addItem(scatter)

# At this point, the legend is visible
# To remove the legend:
pw.scene().removeItem(legend)

# Now, the legend is gone
pw.show()