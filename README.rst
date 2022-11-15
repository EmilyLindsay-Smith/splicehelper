SpliceHelper
============

:Author:
	Emily Lindsay-SMith
:Version: 1.1 of 2022/11/14

Purpose
=======
This is a python application to create Splice files for use in the Language and Brain Lab (Oxford)'s behavioural tasks.
A command line tool broadly works but needs refactoring and testing 


To Do
======

* How to handle GAP / other signifiers for breaks
	* both for add_wav_to_stimuli
	* and for getting correct break output later
* Check if file exists and if not try again for create_df_from_input - decide where this goes, maybe in wrapper?
* Refactor commandline code into separate file that imports these main functions
	* add tests for commandline code? 
	* if working, can try to make the commandline version available on PyPI?
* Create GUI view
	* In progress - forms created
	* Need to sort basic styling
* Create controller to link model and view
* Package GUI for installation
