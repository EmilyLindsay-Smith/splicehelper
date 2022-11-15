import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import(
	QApplication,
	QGridLayout,
	QLineEdit,
	QMainWindow,
	QPushButton,
	QVBoxLayout,
	QHBoxLayout,
	QStackedLayout,
	QWidget,
	QLabel
)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("SpliceHelper")

		#Define Layouts and add them together
		pageLayout = QVBoxLayout()
		self.stackLayout = QStackedLayout()
		self.headingLayout = QVBoxLayout()
		self.buttonLayout =QHBoxLayout()

		pageLayout.addLayout(self.headingLayout)
		pageLayout.addLayout(self.stackLayout)
		pageLayout.addLayout(self.buttonLayout)
		#Define headingLayout Elements
		self.header_label = QLabel("Welcome to SpliceHelper")
		self.headingLayout.addWidget(self.header_label)

		#Define Rotating views to show on stackedlayout
		self.page1 = FirstDisplay()
		self.stackLayout.addWidget(self.page1)
g
		#Define buttonLayout buttons to display all the time
		self.btn = QPushButton("Next")
		self.buttonLayout.addWidget(self.btn)
		self.btn.pressed.connect(lambda bool=0, index=1:self.__activate_tab(index))
		#Create Central Widget
		widget = QWidget()
		widget.setLayout(pageLayout)
		self.setCentralWidget(widget)

	def __activate_tab(self,index):
		current = self.stackLayout.currentIndex()
		if current == (self.stackLayout.count() -1 ):
			self.stackLayout.setCurrentIndex(0)
		else:
			self.stackLayout.setCurrentIndex(current+1)

class FirstDisplay(QWidget):
	#TODO: Does not stay on screen
	def __init__(self):
		super().__init__()
	#	displayLayout = QVBoxLayout()
		self.temp_label = QLabel("Welcome to the First Display")
	#	displayLayout.add(self.temp_label)
	#	self.setLayout(displayLayout)

if __name__=="__main__":
	app = QApplication([])
	window = MainWindow()
	window.show()
	sys.exit(app.exec())