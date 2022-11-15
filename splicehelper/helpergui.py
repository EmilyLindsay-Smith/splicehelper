import sys
import re

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
	QFormLayout,
	QWidget,
	QLabel,
	QLineEdit
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

		self.page2 = SecondDisplay()
		self.stackLayout.addWidget(self.page2)

		self.page3 = ThirdDisplay()
		self.stackLayout.addWidget(self.page3)

		self.page4 = FourthDisplay()
		self.stackLayout.addWidget(self.page4)
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
	#TODO: Welcome to SpliceHelper. Import main file & second file if needed
		# Greeting Label
		# Explain Label
		# TextBox to give file name - consider validation?
		# Explain Label for merge file
		# TextBox to give file name - consider validation?
	def __init__(self):
		super().__init__()
		#Define Display
		displayLayout = QVBoxLayout()

		#Define Content and add to displayLayout
		self.temp_label = QLabel("Welcome to the First Display")
		displayLayout.addWidget(self.temp_label)

		
		greeting_label_text = """Welcome to SpliceHelper. My job is to help you build splice files \
			for use in splice.pl at the Language and Brain Lab, Oxford University.
			To get started, let me know what file you'd like to build from. \
			I can handle the following file formats:
			.csv, .xls, .xlsx, .xlsm, .xlsb, .odf, .ods, .odt
			(But I do assume you're using Sheet 1 of Excel.) """

		greeting_label_text = re.sub(r'\t', '', greeting_label_text)
		self.greeting_label=QLabel(greeting_label_text)	
		self.greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		displayLayout.addWidget(self.greeting_label)

		self.main_file_input = QLineEdit(
			self,
			placeholderText='Main Stimulus File Path',
			clearButtonEnabled=True)
		displayLayout.addWidget(self.main_file_input)

		merge_explanation_text = """If all your stimuli and data are in that file, great! Press Next.\n\n
		However, if you need to merge the above file with another one, let me know the file here:"""
		merge_explanation_text = re.sub(r'\t', '', 	merge_explanation_text)
		self.merge_explanation_label=QLabel(merge_explanation_text)	
		self.merge_explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		displayLayout.addWidget(self.merge_explanation_label)

		self.merge_file_input = QLineEdit(
			self,
			placeholderText='Merge File Path',
			clearButtonEnabled=True
			)
		displayLayout.addWidget(self.merge_file_input)
		#Set Layout
		self.setLayout(displayLayout)


class SecondDisplay(QWidget):
	#TODO: Merge files if needed
		# Show snippets of both files, check if correct and if not return to first screen
		# Get merge_on for main file
		# Get merge_on for second file 
	def __init__(self):
		super().__init__()
		displayLayout = QVBoxLayout()
		self.temp_label = QLabel("Welcome to the Second Display")
		displayLayout.addWidget(self.temp_label)
		self.setLayout(displayLayout)


class ThirdDisplay(QWidget):
	#TODO: Get ISIs, CodeArray COlumns, Listname, title, filename
		# Show snippet of dataframe in use
		# TextBoxes for ISIs, CodeArray COlumns, Listname, title, filename
	def __init__(self):
		super().__init__()
		displayLayout = QVBoxLayout()
		self.temp_label = QLabel("Welcome to the Third Display")
		displayLayout.addWidget(self.temp_label)
		self.setLayout(displayLayout)

class FourthDisplay(QWidget):
	#TODO: Announce file is ready, give option to start again from various stages or finish.
		# Explain situation, preferably repeat filename
		# Buttons for different restart points 
		# Finish button to close application 
	def __init__(self):
		super().__init__()
		displayLayout = QVBoxLayout()
		self.temp_label = QLabel("Welcome to the Fourth Display")
		displayLayout.addWidget(self.temp_label)
		self.setLayout(displayLayout)


if __name__=="__main__":
	app = QApplication([])
	window = MainWindow()
	window.show()
	sys.exit(app.exec())