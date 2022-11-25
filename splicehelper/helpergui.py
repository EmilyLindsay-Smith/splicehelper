import sys
import re
from pathlib import Path

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
	QLineEdit,
	QFileDialog
)

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("SpliceHelper")
		self.setGeometry(300, 200, 700, 700)
		self.setFixedSize(700,700)

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
		self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.header_label.setStyleSheet("font-weight: bold")
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

		greetingLayout = QHBoxLayout()
		textLayout = QHBoxLayout()
		#Define Content and add to displayLayout
		
		greeting_label_text = "Let me help you build splice files"
		greeting_label_text += " for use in splice.pl at the Language and Brain Lab, Oxford University.\n"
		greeting_label_text += "To get started, let me know what file you'd like to build from.\n"
		greeting_label_text += "I can handle the following file formats:\n"
		greeting_label_text += ".csv, .xls, .xlsx, .xlsm, .xlsb, .odf, .ods, .odt\n"
		greeting_label_text += "(But I do assume you're using Sheet 1 of Excel.) "

		self.greeting_label=QLabel(greeting_label_text)	
		greetingLayout.addWidget(self.greeting_label)
		self.greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		displayLayout.addLayout(greetingLayout)
		

		self.main_file_input_label = QLabel("What is your main stimulus file?")
		self.file_input_button = QPushButton("Select File")
		self.file_input_button.pressed.connect(self.__selectFile)
		layout_form1 = QFormLayout()
		layout_form1.addRow(self.main_file_input_label, self.file_input_button)
		displayLayout.addLayout(layout_form1)


		merge_explanation_text = "If all your stimuli and data are in that file, great! Press Next.\n\n"
		merge_explanation_text += "However, if you need to merge the above file with another one, let me know the file here:"""
		self.merge_explanation_label=QLabel(merge_explanation_text)	
		self.merge_explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		textLayout.addWidget(self.merge_explanation_label)
		displayLayout.addLayout(textLayout)

		self.merge_file_input_label = QLabel("What is your secondary stimulus file?")
		self.mergefile_input_button = QPushButton("Select File")
		self.mergefile_input_button.pressed.connect(self.__selectFile)
		layout_form2 = QFormLayout()
		layout_form2.addRow(self.merge_file_input_label, self.mergefile_input_button)
		displayLayout.addLayout(layout_form2)
		#Set Layout
		self.setLayout(displayLayout)

	def __selectFile(self):
		home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
		if fname[0]:
			f = open(fname[0], 'r')
			with f:
				data = f.read()



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
		
		self.instructions_label = QLabel("Let me know the following values so I can merge your files:")
		displayLayout.addWidget(self.instructions_label)

		self.merge_details=QWidget(self)
		self.form_layout = QFormLayout()
		self.merge_details.setLayout(self.form_layout)

		self.entry1 = QLineEdit(self.merge_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry1_label = 'Main File Row to Merge On:'
		self.form_layout.addRow(self.entry1_label, self.entry1)

		self.entry2 = QLineEdit(self.merge_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry2_label = 'Merge File Row to Merge On:'
		self.form_layout.addRow(self.entry2_label, self.entry2)

		displayLayout.addWidget(self.merge_details)
		self.setLayout(displayLayout)
class ThirdDisplay(QWidget):
	#TODO: Get ISIs, CodeArray COlumns, Listname, title, filename
		# Show snippet of dataframe in use
		# TextBoxes for ISIs, CodeArray COlumns, Listname, title, filename
	def __init__(self):
		super().__init__()
		displayLayout = QVBoxLayout()
		textLayout = QHBoxLayout()
		self.temp_label = QLabel("Welcome to the Third Display")
		displayLayout.addWidget(self.temp_label)
		
		self.instructions_label = QLabel("Let me know the following values so I can build your splice file:")
		textLayout.addWidget(self.instructions_label)
		displayLayout.addLayout(textLayout)

		self.specific_details=QWidget(self)
		self.form_layout = QFormLayout()

		self.entry1 = QLineEdit(self.specific_details, placeholderText='title', clearButtonEnabled=True)
		self.entry1_label = 'Title:'
		self.form_layout.addRow(self.entry1_label, self.entry1)

		self.entry2 = QLineEdit(self.specific_details, placeholderText='ISI', clearButtonEnabled=True)
		self.entry2_label = 'ISI 1:'
		self.form_layout.addRow(self.entry2_label, self.entry2)

		self.entry3 = QLineEdit(self.specific_details, placeholderText='ISI', clearButtonEnabled=True)
		self.entry3_label = 'ISI 2:'
		self.form_layout.addRow(self.entry3_label, self.entry3)


		self.entry7 = QLineEdit(self.specific_details, placeholderText='ISI', clearButtonEnabled=True)
		self.entry7_label = 'ISI 3:'
		self.form_layout.addRow(self.entry7_label, self.entry7)
	

		self.entry4 = QLineEdit(self.specific_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry4_label = 'Auditory Stimuli Column Name:'
		self.form_layout.addRow(self.entry4_label, self.entry4)
		

		self.entry8 = QLineEdit(self.specific_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry8_label = 'Visual Stimuli Column Name:'
		self.form_layout.addRow(self.entry8_label, self.entry8)
		

		self.entry5 = QLineEdit(self.specific_details, placeholderText="['Column1', 'Column2']", clearButtonEnabled=True)
		self.entry5_label = 'Array of Coding Columns:'
		self.form_layout.addRow(self.entry5_label, self.entry5)
		

		self.entry6 = QLineEdit(self.specific_details, placeholderText="path/to/filename_without_extension", clearButtonEnabled=True)
		self.entry6_label = 'Output Filename and Path:'
		self.form_layout.addRow(self.entry6_label, self.entry6)

		displayLayout.addWidget(self.specific_details)
		self.specific_details.setLayout(self.form_layout)
		displayLayout.addWidget(self.specific_details)

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
	window.setStyleSheet("""
		QLabel  {padding-bottom: 3px}
		""")


	window.show()
	sys.exit(app.exec())