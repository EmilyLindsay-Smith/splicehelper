from helperutils import *

import sys
import re
from pathlib import Path
import pandas as pd

from PyQt6.QtCore import(
	Qt,
	QAbstractTableModel
	)

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
	QFileDialog,
	QTableView, 
	QComboBox,
	QListWidget,
	QAbstractItemView
)

from helperutils import run_splice_helper

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
		self.backbtn = QPushButton("Back") #the back button starts with no label
		self.buttonLayout.addWidget(self.backbtn)
		self.btn = QPushButton("Next")
		self.buttonLayout.addWidget(self.btn)
	
			#Create Central Widget
		widget = QWidget()
		widget.setLayout(pageLayout)
		self.setCentralWidget(widget)


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
		#self.file_input_button.pressed.connect(lambda type='main':self.__selectFile(type))
		layout_form1 = QFormLayout()
		layout_form1.addRow(self.main_file_input_label, self.file_input_button)		
		self.textlabel = QLabel("")
		layout_form1.addWidget(self.textlabel)
		displayLayout.addLayout(layout_form1)

		self.table = QTableView()
		self.data = pd.DataFrame([])
		self.model = TableModel(self.data)
		self.table.setModel(self.model)

		displayLayout.addWidget(self.table)

		merge_explanation_text = "If all your stimuli and data are in that file, great! Press Next.\n\n"
		merge_explanation_text += "However, if you need to merge the above file with another one, let me know the file here:"""
		self.merge_explanation_label=QLabel(merge_explanation_text)	
		self.merge_explanation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		textLayout.addWidget(self.merge_explanation_label)
		displayLayout.addLayout(textLayout)

		self.merge_file_input_label = QLabel("What is your secondary stimulus file?")
		self.mergefile_input_button = QPushButton("Select File")
		#self.mergefile_input_button.pressed.connect(lambda type='merge':self.__selectFile(type))
		layout_form2 = QFormLayout()
		layout_form2.addRow(self.merge_file_input_label, self.mergefile_input_button)
		self.textlabel2 = QLabel("")
		layout_form2.addWidget(self.textlabel2)
		displayLayout.addLayout(layout_form2)


		self.table2 = QTableView()
		displayLayout.addWidget(self.table2)

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
		
		self.table_main_label = QLabel("Your Main File:")
		displayLayout.addWidget(self.table_main_label)
		self.table_main = QTableView()
		displayLayout.addWidget(self.table_main)

		self.table_merge_label = QLabel("Your Merge File:")
		displayLayout.addWidget(self.table_merge_label)
		self.table_merge = QTableView()
		displayLayout.addWidget(self.table_merge)

		self.instructions_label = QLabel("I need to know which column your files have in common so I can merge them:")
		displayLayout.addWidget(self.instructions_label)

		self.merge_details=QWidget(self)
		self.form_layout = QFormLayout()
		self.merge_details.setLayout(self.form_layout)

	#self.entry1 = QLineEdit(self.merge_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry1 = QComboBox(self.merge_details)
		self.entry1.currentTextChanged.connect(self.text_changed)

		self.entry1_label = 'Main File Row to Merge On:'
		self.form_layout.addRow(self.entry1_label, self.entry1)

		self.entry2 = QComboBox(self.merge_details)
		self.entry2_label = 'Merge File Row to Merge On:'
		self.form_layout.addRow(self.entry2_label, self.entry2)

		displayLayout.addWidget(self.merge_details)
		self.setLayout(displayLayout)

	def text_changed(self, s):
		print(s)

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

		self.table = QTableView()
		displayLayout.addWidget(self.table)

		self.specific_details=QWidget(self)
		self.form_layout = QFormLayout()

		self.entry1 = QLineEdit(self.specific_details, placeholderText='title', clearButtonEnabled=True)
		self.entry1_label = 'Title:'
		self.form_layout.addRow(self.entry1_label, self.entry1)

		self.entry2 = QLineEdit(self.specific_details, placeholderText='ISI ', clearButtonEnabled=True)
		self.entry2_label = 'ISI 1: Before All Stimuli'
		self.form_layout.addRow(self.entry2_label, self.entry2)

		self.entry3 = QLineEdit(self.specific_details, placeholderText='ISI', clearButtonEnabled=True)
		self.entry3_label = 'ISI 2: After All Stimuli'
		self.form_layout.addRow(self.entry3_label, self.entry3)


		self.entry7 = QLineEdit(self.specific_details, placeholderText='ISI', clearButtonEnabled=True)
		self.entry7_label = 'ISI 3: Between Audio and Visual Stimuli'
		self.form_layout.addRow(self.entry7_label, self.entry7)
	

		#self.entry4 = QLineEdit(self.specific_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry4 = QComboBox(self.specific_details)
		self.entry4_label = 'Auditory Stimuli Column Name:'
		self.form_layout.addRow(self.entry4_label, self.entry4)
		

		#self.entry8 = QLineEdit(self.specific_details, placeholderText='Column Name', clearButtonEnabled=True)
		self.entry8 = QComboBox(self.specific_details)
		self.entry8_label = 'Visual Stimuli Column Name:'
		self.form_layout.addRow(self.entry8_label, self.entry8)
		

		#self.entry5 = QLineEdit(self.specific_details, placeholderText="['Column1', 'Column2']", clearButtonEnabled=True)
		self.entry5 = QListWidget(self.specific_details)
		self.entry5.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
		self.entry5_label = 'Array of Coding Columns:'
		self.form_layout.addRow(self.entry5_label, self.entry5)

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
		
		self.info_label = QLabel("Your SpliceHelper File is now ready! Let me know the directory and filename where you want to save it:")
		displayLayout.addWidget(self.info_label)

		self.main_file_input_label = QLabel("Where should I save it?")
		self.file_input_button = QPushButton("Select File")
		self.file_input_button.pressed.connect(lambda bool=0:self.__selectFile())
		layout_form1 = QFormLayout()
		layout_form1.addRow(self.main_file_input_label, self.file_input_button)		
		self.textlabel = QLabel("")

		layout_form1.addWidget(self.textlabel)
		self.create_splice_btn = QPushButton("Make My Splice Files")
		layout_form1.addWidget(self.create_splice_btn)
		self.successlabel = QLabel("Click Make My Splice Files")
		layout_form1.addWidget(self.successlabel)
		displayLayout.addLayout(layout_form1)
		
		self.setLayout(displayLayout)

	def __selectFile(self):
		home_dir = str(Path.home())
		self.fileName = QFileDialog.getSaveFileName(self, "Project Save As", home_dir, ".txt")
		self.textlabel.setText(self.fileName[0] + self.fileName[1])
		#self.textlabel.setText(self.fileNames[0])
#		print(self.dialog)


class TableModel(QAbstractTableModel):
	def __init__(self, data):
		super(TableModel, self).__init__()
		self._data = data

	def data(self, index, role):
		if role == Qt.ItemDataRole.DisplayRole:
			#return self._data[index.row()][index.column()]
			value = self._data.iloc[index.row(), index.column()]
			return str(value)

	def rowCount(self, index):
		#return len(self._data)
		return self._data.shape[0]

	def columnCount(self, index):
		#return len(self._data[0])
		return self._data.shape[1]

	def headerData(self, section, orientation, role):
		if role == Qt.ItemDataRole.DisplayRole:
			if orientation == Qt.Orientation.Horizontal:
				return str(self._data.columns[section])

			if orientation == Qt.Orientation.Vertical:
				return str(self._data.index[section])

class SpliceHelper:
	def __init__(self, model, view):
		self.__view = view
		self.__model = model
		self.__connectSignalsAndSlots()

	def __connectSignalsAndSlots(self):
		self.__view.btn.pressed.connect(lambda bool=0, index=1:print(index))
		self.__view.backbtn.pressed.connect(lambda bool=0: self.__back_tab())

		self.__view.page1.file_input_button.pressed.connect(lambda type='main':self.__selectFile(type))
		self.__view.page1.mergefile_input_button.pressed.connect(lambda type='merge':self.__selectFile(type))
		self.__view.btn.pressed.connect(lambda bool=0 :self.__activate_tab())
		self.__view.page4.create_splice_btn.pressed.connect(lambda bool=0: self.__collectMe())
		self.__view.page4.create_splice_btn.pressed.connect(lambda bool=0: self.__printMe())
		self.__view.page4.create_splice_btn.pressed.connect(lambda bool=0: self.__runme())
		print('Tester')

	def __runme(self):
		try:
			self.__view.page4.successlabel.setText('Creating your files...')
			run_splice_helper_gui(self.data, 
			self.auditorystimuli, 
			self.coding_array,
			self.isi1, 
			self.isi2, 
			self.outputfilename, 
			self.title, 
			self.visualstimuli, 
			self.isi3)
			self.__view.page4.successlabel.setText('Your SpliceHelper File is finished! \n Click Next to make another file')
			print('Completed')
		except Exception:
			print("Error: ")
		

	def __activate_tab(self):
		current = self.__view.stackLayout.currentIndex()
		if current == (self.__view.stackLayout.count() -1 ):
			self.__view.btn.setText('Return to Start')
			self.__view.stackLayout.setCurrentIndex(0)
		elif (current == 0) & (self.__view.page1.textlabel2.text() == ''):
				self.__view.stackLayout.setCurrentIndex(current+2)
		elif current ==1 :
			self.__mergeFiles()
			self.__view.stackLayout.setCurrentIndex(current+1)
		else:
			self.__view.stackLayout.setCurrentIndex(current+1)

	def __back_tab(self):
		current = self.__view.stackLayout.currentIndex()
		if (current == 2) & (self.__view.page1.textlabel2.text() == ''):
			self.__view.stackLayout.setCurrentIndex(current-2)
		else:
			self.__view.stackLayout.setCurrentIndex(current-1)

	def __mergeFiles(self):
		self.input_file = create_df_from_input(self.__view.page1.textlabel.text())
		self.input_file2 = create_df_from_input(self.__view.page1.textlabel2.text())
		self.merge_on_main_df = self.__view.page2.entry1.currentText()
		self.merge_on_other_df = self.__view.page2.entry2.currentText()
		self.data = merge_df_with_another(self.input_file, self.input_file2, self.merge_on_main_df, self.merge_on_other_df)
		print('Merged df: ', self.data)
		self.__displayTable(self.data)

	def __collectMe(self):
		print("Collector")
		self.input_file= self.__view.page1.textlabel.text()
		self.auditorystimuli= self.__view.page3.entry4.currentText()
		self.visualstimuli=self.__view.page3.entry8.currentText()
		self.coding_array = []
		[self.coding_array.append(i.text()) for i in self.__view.page3.entry5.selectedItems()]
		self.isi1= self.__view.page3.entry2.text()
		self.isi2= self.__view.page3.entry3.text()
		self.isi3= self.__view.page3.entry7.text()
		self.title= self.__view.page3.entry1.text() 
		self.outputfilename = self.__view.page4.textlabel.text()
		self.input_file2 = self.__view.page1.textlabel2.text()
		self.merge_on_main_df= self.__view.page2.entry1.currentText()
		self.merge_on_other_df= self.__view.page2.entry2.currentText()
		print("CodingArray:", self.outputfilename)

	def __printMe(self):
		print("Printer")
		print(self.input_file, 
			self.auditorystimuli,
			self.visualstimuli,
			self.coding_array,
			self.isi1,
			self.isi2,
			self.isi3,
			self.outputfilename,
			self.title,
			self.input_file2,
			self.merge_on_main_df,
			self.merge_on_other_df,
		)

	def __selectFile(self, type):
		#home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileName(self.__view.page1, 'Open file') #, home_dir)
		if fname[0]:
			if type == 'main':
				self.__view.page1.textlabel.setText(fname[0])
				self.data = create_df_from_input(fname[0])
				self.__displayTable(self.data)
				print(self.data)
			else:
				self.__view.page1.textlabel2.setText(fname[0])
				self.data2 = create_df_from_input(fname[0])
				self.model2 = TableModel(self.data2)
				self.__view.page1.table2.setModel(self.model2)
				self.__view.page2.table_merge.setModel(self.model2)
				self.__view.page2.entry2.addItems(list(self.data2.columns))
				print(self.data2)

	def __displayTable(self, data):
		self.model = TableModel(data)
		self.__view.page1.table.setModel(self.model)
		self.__view.page2.table_main.setModel(self.model)
		self.__view.page3.table.setModel(self.model)
		self.datacolumns = list(self.data.columns)
		self.__view.page2.entry1.clear()
		self.__view.page3.entry4.clear()
		self.__view.page3.entry8.clear()
		self.__view.page3.entry5.clear()
		self.__view.page2.entry1.addItems(self.datacolumns)
		self.__view.page3.entry4.addItems(self.datacolumns)
		self.__view.page3.entry8.addItems(self.datacolumns)
		self.__view.page3.entry5.addItems(self.datacolumns)

def __runme(*args):
	run_splice_helper(self.input_file, 
		self.auditorystimuli, 
		self.coding_array,
		self.isi1, 
		self.isi2, 
		self.outputfilename, 
		self.title, 
		self.visualstimuli, 
		self.isi3, 
		self.input_file2, 
		self.merge_on_main_df, 
		self.merge_on_other_df)

if __name__=="__main__":
	app = QApplication([])
	window = MainWindow()
	window.setStyleSheet("""
		QLabel  {padding-bottom: 3px}
		""")
	SpliceHelper(model = __runme, view = window)

	window.show()
	sys.exit(app.exec())