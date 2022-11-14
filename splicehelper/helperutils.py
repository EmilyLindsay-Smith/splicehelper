# This is the MODEL code for the SpliceHelper Project
# Think about checking for errors/problems etc
#Does not handle GAP rows to add breaks in 

#Import Packages
import pandas as pd
import re
import os

#Create df from csv or excel input
def create_df_from_input(filename):
	#TODO: check if file exists, and if not raise error
	file_extension = filename.split('.')[-1] 
	excel_extensions = ['xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'] 
	#To Resolve these paths:
	##Excel: openpyxl
	##ODS: odfpy
	##XLS: xlrd

	if file_extension == 'csv':
		df = pd.read_csv(filename)
	elif file_extension in excel_extensions:
		#presumes first row is the header row, else header = None needed
		df = pd.read_excel(filename)
	elif filename == '':
		raise Exception("No filename supplied")
	else:
		raise Exception(f"SpliceHelper does not accept filenames with the extension {file_extension}. \n Try again with: .csv, .xls, .xlsx, .xlsm, .xlsb, .odf, .ods, .odt")
	
	return df

#Merge with another CSV file
def merge_df_with_another(main_df, other_df, merge_on_main_df, merge_on_other_df='', how='left'):
	try:
		if merge_on_other_df == '':
			df = main_df.merge(other_df, on=merge_on_main_df,how=how)
		else:
			df = main_df.merge(other_df, left_on=merge_on_main_df, right_on=merge_on_other_df, how=how)
			df.drop(merge_on_other_df, axis=1, inplace=True)
	except:
		raise Exception('Error with DF Merging')
	return df

#Merge in splice specific columns - incl specify ISI
def create_df_with_splice_columns(df, isi1, isi2):
	#Define Splice Specific Columns

	Bleep1 = f'bleep; pause, {isi1};'
	Bleep2 = f'pulse; pause, {isi2}; code, '
	#Add Them In 
	df['! Bleep1'] = Bleep1.upper()
	df['Bleep2'] = Bleep2.upper()
	df['Dummy'] = 0
	return df
	

#Identify Columns to include in the output
def create_subset_df_for_list(df, listname, coding_array):
	if listname in df.columns:
		myArray = ['! Bleep1']
		myArray.append(listname)
		myArray.append('Bleep2')
	else:
		raise Exception(f'Stimuli Listname {listname} given to create subset is not present in data')

	for item in coding_array:
		if item in df.columns:
			myArray.append(item)
		else:
			raise Exception(f'Coding column {item} not present in data')

	myArray.append('Dummy')
	df = df[myArray]
	return df 

#Add .wav to Stimuli List
def add_wav_to_stimuli(df, listname):
	#Assumes every row has content -can't handle gap rows
	try:
		df[listname] = [x + '.wav' if '.wav' not in x else x for x in df[listname]]
		return df
	except Exception as e:
		print(e)
		return df

# Create output file including the splice header code 
## Ensure no BOM

def configure_splice_header(coding_array):
	zeroes = ''
	column_headers = ''
	for item in coding_array:
		zeroes += '0 '
		column_headers += item + ' '
	zeroes += '0' #for the Dummy Column
	splice_header=f"""
	CODEHEAD, {column_headers}Dummy 

	ZEROCROSS,on
	PAUSE,4000
	BLEEP; PAUSE,1000; BLEEP; PAUSE,1000; BLEEP;
	PAUSE,2000

	!
	! Countdown
	!

	BLEEP; PAUSE,300; PULSE; STR,5,1000; PAUSE,1000; CODE,{zeroes}
	BLEEP; PAUSE,300; PULSE; STR,4,1000; PAUSE,1000; CODE,{zeroes}
	BLEEP; PAUSE,300; PULSE; STR,3,1000; PAUSE,1000; CODE,{zeroes}
	BLEEP; PAUSE,300; PULSE; STR,2,1000; PAUSE,1000; CODE,{zeroes}
	BLEEP; PAUSE,300; PULSE; STR,1,1000; PAUSE,1000; CODE,{zeroes}

	"""
	splice_header = re.sub(r'\t', '', splice_header)
	return splice_header


#print to csv then to txt 
def print_file(df, splice_header, outputfilename, title):
	splice_header = splice_header
	title = '! ' + title + '\n'
	#Creates temporary .csv to avoid extra spaces created by df.to_String() - this is removed
	temp = outputfilename + '.csv' #so if multiple runs at once no clashes
	df.to_csv(temp, index=None, sep=' ', header=False, na_rep='NULL', quoting=3, escapechar=' ', encoding='utf-8')
	with open(temp, "r", encoding = 'utf-8') as f:
		splice_contents = f.read()
	os.remove(temp)
	splice_contents = re.sub(r' {2,}', ' ', splice_contents)
	with open(outputfilename, 'w') as f:
		f.write(title)
		f.write(splice_header)
		f.write(splice_contents)

##Useful Functions

def get_column_names(df):
	return list(df.columns)

def run_splice_helper(input_file, listname, coding_array, isi1, isi2, outputfilename, title, input_file2 = '', merge_on_main_df='', merge_on_other_df=''):
	try: 
		print('Running the helper:')
		df = create_df_from_input(input_file)
		print(df.head())
		print(get_column_names(df))
		if input_file2 != '':
			print('Merge to do')
			second_df = create_df_from_input(input_file2)
			print(second_df.head())
			df = merge_df_with_another(df, second_df, merge_on_main_df, merge_on_other_df)
			print(df.head())
		print('Add Splice:')
		df = create_df_with_splice_columns(df, isi1, isi2)
		print('Subsetting:')
		df = create_subset_df_for_list(df, listname, coding_array)
		print('Adding Waves')
		df = add_wav_to_stimuli(df, listname)
		print('Creating OUtput Files:')
		splice_header = configure_splice_header(coding_array)
		print_file(df, splice_header, outputfilename, title)
		return 'Success'
	except Exception as e:
		print(e)


###CommandLineFunctions####
def get_mainfile(main_or_second):
	def request_file(main_or_second):
		try:
			input_file = input(f'What is your {main_or_second} filename?')
			df = create_df_from_input(input_file)
			return df
		except FileNotFoundError:
			print('We did not recognise that filename. Please try again:')
			request_file(main_or_second)
	df = request_file(main_or_second)
	print(f'This is the start of your {main_or_second} file: \n')
	print(df.head())
	answer = input('Is this the right file? Y/N \n')
	if answer.lower() == 'n':
		get_mainfile(main_or_second)
	else:
		return df

def merge_files(df):
	need_to_merge = input('Do you need to merge this with another file? Y/N \n')	
	
	def merger(df):
		df2 = get_mainfile('other')
		on_main = input('What is the shared column name in your main file?\n Column Name: ')
		on_second = input('What is the shared column name in your other file?\n Column Name: ')
		df_new = merge_df_with_another(df, df2, on_main, on_second)
		print('This is the merger of your two files: \n')
		print(df_new.head())
		answer = input('Does this look right? Y/N \n')
		if answer.lower() == 'n':
			print("Let's try again.")
			merger(df)	
		else:
			return df_new			

	if need_to_merge.lower() == 'y':
		df = merger(df)
		return df
	else:
		return df	

def get_specifics(df):
	isi1 = input('What is your first interstimulus interval?\n First ISI: ')
	isi2 = input('What is your second interstimulus interval?\n Second ISI: ')
	print('The column names available are: \n')
	print(df)
	print(get_column_names(df))
	listname = input('What is the column name for your stimulus list? \n')

	def get_codearray(codearray, df):
		codearray = codearray
		print('Available Columns: ', get_column_names(df))
		print('Columns Selected to Include: ', codearray)
		item = input('What column do you want to include? \nColumn: ')
		if item in get_column_names(df):
			codearray.append(item)
			print('So far you have selected: ', codearray)
		else:
			print('You have not typed something that matches the column names available :( \n')
			print('The options are: ', get_column_names(df))
		answer = input('Do you want to add another column? Y/N \n')
		if answer.lower() == 'y':
			get_codearray(codearray, df)
		return codearray

	codearray = []
	answer = input('Do you need to include other columns for the coding? Y/N \n')
	if answer.lower() == 'y':	
		codearray = get_codearray(codearray, df)
			
	print('Creating your splice file...')
	df = create_df_with_splice_columns(df, isi1, isi2)
	df = create_subset_df_for_list(df, listname, codearray)
	df = add_wav_to_stimuli(df, listname)
	splice_header = configure_splice_header(codearray)
	return df , splice_header

def print_splice(df, splice_header):
	print('Your splice file is almost ready!\n')
	title = input('What do you want your title to be on the first line of the splice file?')
	outputfilename = input('What do you want your output file to be called?\n Do not include file extension \n Filename: ') + '.txt'
	print_file(df, splice_header, outputfilename, title)
	print('Your splice file is has been created.')
	answer = input('Do you need to make more splice files from the same input files? i.e. new lists\n Y/N \n')
	if answer.lower() == 'n':
		return 'finished'
	else:
		print("OK, let's make another one!")
		return 'again'

def create_inputs():
	df = get_mainfile('main')
	df = merge_files(df)
	return df

def create_files(df):
	df_final, splice_header = get_specifics(df)
	repeat_query = print_splice(df_final, splice_header)
	if repeat_query == 'again':
		create_files(df)
	else:
		print('Thanks for using me')


print('Welcome to SpliceHelper! \n My job is to help you create splice files from your data')
df = create_inputs()
create_files(df)
