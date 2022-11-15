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
	#Note this displays index of stack layout, not checking content shown
	widget = MainWindow()
	qtbot.addWidget(widget)
	currentIndex = widget.stackLayout.currentIndex()

	qtbot.mouseClick(widget.btn, qt_api.QtCore.Qt.MouseButton.LeftButton)

	newIndex = widget.stackLayout.currentIndex()
	totalViews = widget.stackLayout.count()
	if totalViews == 0:
		assert newIndex == -1
	elif totalViews != 0 and currentIndex != totalViews:
		assert currentIndex == newIndex + 1
	elif totalViews !=0:
		assert newIndex == 0

