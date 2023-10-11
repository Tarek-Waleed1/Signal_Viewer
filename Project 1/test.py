import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.line_edit = QLineEdit(self)
        self.layout.addWidget(self.line_edit)

        self.button = QPushButton("Click Me!", self)
        self.layout.addWidget(self.button)

        # Connect the QLineEdit's textChanged signal to a custom slot
        self.line_edit.textChanged.connect(self.on_text_changed)

        self.setWindowTitle("QLineEdit Connect Example")
        self.setGeometry(100, 100, 400, 200)

    def on_text_changed(self, text):
        # This method will be called whenever the text in the QLineEdit changes
        print("Text changed:", text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
