import pytest
from splicehelper.helpergui import *

from pytestqt.qt_compat import qt_api

def test_basics(qtbot):
	assert QApplication.instance() is not None
	widget = MainWindow()
	qtbot.addWidget(widget)

	widget.show()
	assert widget.isVisible()
	assert widget.windowTitle() == "SpliceHelper"

def test_windowheader(qtbot):
	widget = MainWindow()
	qtbot.addWidget(widget)

	assert widget.header_label.text() == 'Welcome to SpliceHelper'

def test_nextbutton(qtbot):
	widget = MainWindow()
	qtbot.addWidget(widget)

	assert widget.btn.text() == 'Next'

def test_nextbutton_function(qtbot):
	widget = MainWindow()
	qtbot.addWidget(widget)
	
	totalViews = widget.stackLayout.count()

	def assertions():
		currentIndex = widget.stackLayout.currentIndex()
		qtbot.mouseClick(widget.btn, qt_api.QtCore.Qt.MouseButton.LeftButton)
		newIndex = widget.stackLayout.currentIndex()
		if totalViews == 0:
			assert newIndex == -1
		elif totalViews != 0 and currentIndex != totalViews -1:
			assert currentIndex == newIndex - 1
		elif totalViews !=0:
			assert newIndex == 0

	def checkcontent():
		newIndex = widget.stackLayout.currentIndex()
		if newIndex == 0:
			assert widget.page1.temp_label.text() == "Welcome to the First Display"
		elif newIndex == 1:
			assert widget.page2.temp_label.text() == "Welcome to the Second Display"
		elif newIndex == 2:
			assert widget.page3.temp_label.text() == "Welcome to the Third Display"
		elif newIndex == 3:
			assert widget.page4.temp_label.text() == "Welcome to the Fourth Display"

	for i in range(0, totalViews):
		assertions()
		checkcontent()

def test_firstdisplay(qtbot):
	widget = FirstDisplay()
	qtbot.addWidget(widget)

	assert widget.temp_label.text() == "Welcome to the First Display"
	assert "help you build splice files" in widget.greeting_label.text()
	assert "if you need to merge" in widget.merge_explanation_label.text()

def test_seconddisplay_instructions(qtbot):
	widget = SecondDisplay()
	qtbot.addWidget(widget)

	assert widget.instructions_label.text() == "Let me know the following values so I can merge your files:"

def test_seconddisplay_form(qtbot):
	widget = SecondDisplay()
	qtbot.addWidget(widget)

	assert widget.form_layout.rowCount() == 2
	assert "Main File Row to Merge On:" == widget.entry1_label
	assert "Merge File Row to Merge On:" == widget.entry2_label

def test_thirddisplay_instructions(qtbot):
	widget = ThirdDisplay()
	qtbot.addWidget(widget)

	assert widget.instructions_label.text() == "Let me know the following values so I can build your splice file:"

def test_thirddisplay_form(qtbot):
	widget = ThirdDisplay()
	qtbot.addWidget(widget)

	assert widget.form_layout.rowCount() == 6
	assert "Title:" == widget.entry1_label
	assert "ISI 1:" == widget.entry2_label
	assert "ISI 2:" == widget.entry3_label
	assert "Stimulus Column Name:" == widget.entry4_label
	assert "Array of Coding Columns:" == widget.entry5_label
	assert "Output Filename and Path:" == widget.entry6_label
