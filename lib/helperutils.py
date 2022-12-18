# This is the MODEL code for the SpliceHelper Project
# Think about checking for errors/problems etc

#For ToDos see Github Issues - assorted exist there

# Import Packages
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
def create_df_with_splice_columns(df, isi1, isi2, isi3 = '', stringColumn = ''):
	#Define Splice Line Start

	Bleep1 = f'BLEEP; PAUSE, {isi1};'
	df['! Bleep1'] = Bleep1

	# Define splice string whether visual stimuli present or not
	if stringColumn == '':
		df['Bleep2'] = '; PULSE'
	else:
		stringColumn = stringColumn
		df['Bleep2'] = [f"; PULSE; STR, {i}, {isi3}" for i in df[stringColumn]]
	
	# Define final splice code 
	Bleep3 = f'; PAUSE, {isi2}; CODE, '
	df['Bleep3'] = Bleep3
	df['Dummy'] = '0'
	return df


#Identify Columns to include in the output
def create_subset_df_for_list(df, soundfile, coding_array):
	if soundfile in df.columns:
		myArray = ['! Bleep1']
		myArray.append(soundfile)
		myArray.append('Bleep2')
		myArray.append('Bleep3')
	else:
		raise Exception(f'Sound file column name {soundfile} given to create subset is not present in data')

	for item in coding_array:
		if item in df.columns:
			myArray.append(item)
		else:
			raise Exception(f'Coding column {item} not present in data')

	myArray.append('Dummy')
	df = df[myArray]
	return df

# Add break rows
def add_empty_rows(df, breaktype, period):
	try:
		period = int(period)
	except Exception as e:
		print(e)
		return df
	if period == 0 or period == '' or breaktype == '':
		return df
	else:	
		if breaktype == 'break':
			n_empty = 1
		elif breaktype == 'countdown':
			n_empty = 5
		df = df.reset_index(drop=True)
		len_new_index = len(df) + n_empty*(len(df) // period)
		new_index = pd.RangeIndex(len_new_index)
		df.index += n_empty * (df.index
			.to_series()
			.groupby(df.index // period)
			.ngroup())
		new_df = df.reindex(new_index)
		return new_df



def fill_break_rows(df, coding_array):

	break_row = ['BLEEP; PAUSE,300', '','; PULSE; STR,1,1000;',' PAUSE,1000; CODE']
	break_row2 = ['BLEEP; PAUSE,300', '','; PULSE; STR,2,1000;',' PAUSE,1000; CODE']
	break_row3 = ['BLEEP; PAUSE,300', '','; PULSE; STR,3,1000;',' PAUSE,1000; CODE']
	break_row4 = ['BLEEP; PAUSE,300', '','; PULSE; STR,4,1000;',' PAUSE,1000; CODE']
	break_row5 = ['BLEEP; PAUSE,300', '','; PULSE; STR,5,1000;',' PAUSE,1000; CODE']
	break_row0 = ['BLEEP; PAUSE,501', '','; PULSE; 501;',' PAUSE,2001; CODE']

	rows = [break_row, break_row2, break_row3, break_row4, break_row5, break_row0]
	[row.append(' 0') for i in range(0, len(coding_array)+1) for row in rows]

	df_output = df
	for i in range(0, len(df)-1):
		if df.isna().iloc[i, 1] == True:
			#print(i, df.iloc[i])
			#if df.isna().iloc[i-4][1] == True: #
			if df_output.iloc[i-4][1] == break_row5[1]:
				df_output.loc[i] = break_row
			#elif df.isna().iloc[i-3][1] == True: #
			elif df_output.iloc[i-3][1] == break_row5[1]:
				df_output.loc[i] = break_row2
			#elif df.isna().iloc[i-2][1] == True:#
			elif df_output.iloc[i-2][1] == break_row5[1]:
				df_output.loc[i] = break_row3
			#elif df.isna().iloc[i-1][1] == True:
			elif df_output.iloc[i-1][1] == break_row5[1]:
				df_output.loc[i] = break_row4
			#elif df.isna().iloc[i+1][1] == True: #
			elif df_output.isna().iloc[i+1, 0] == True:
				df_output.loc[i] = break_row5
			else:
				df_output.loc[i] = break_row0
		else:
			df_output.loc[i] = df.iloc[i]
	#print(df_output)
	#print(df_output.iloc[24])
	#print(len(df), len(df_output))
	return df_output
#Add .wav to Stimuli List
def add_wav_to_stimuli(df, soundfile):
	#Assumes every row has content -can't handle gap rows
	try:
		df[soundfile] = [x + '.wav' if isinstance(x, str) and '.wav' not in str(x) else x for x in df.loc[:,soundfile]]
		#df[soundfile] = df['temp']
		#df.drop(columns=['temp'])
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
	PAUSE,5000;BLEEP; PAUSE,1000; BLEEP; PAUSE,1000; BLEEP; PAUSE,2001;

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
	with open(outputfilename, 'w',encoding="utf-8") as f:
		f.write(title)
		f.write(splice_header)
		f.write(splice_contents)

##Useful Functions

def get_column_names(df):
	return list(df.columns)

def run_splice_helper_gui(input_data, soundfile, coding_array, isi1, isi2, outputfilename, title, stringColumn= '', isi3 = '', input_file2 = '', merge_on_main_df='', merge_on_other_df='', breaktype='', period=''):
	try: 
		print('Running the helper:')
		df = input_data
		print(get_column_names(df))
		print('Add Splice:')
		df = create_df_with_splice_columns(df, isi1, isi2, isi3, stringColumn)
		print('Subsetting:')
		df = create_subset_df_for_list(df, soundfile, coding_array)
		print('Adding Waves')
		df = add_wav_to_stimuli(df, soundfile)
		print('Adding Breaks')
		df = add_empty_rows(df, breaktype, period)
		df = fill_break_rows(df, coding_array)
		print('Creating OUtput Files:')
		splice_header = configure_splice_header(coding_array)
		print_file(df, splice_header, outputfilename, title)
		return 'Success'
	except Exception as e:
		print(e)

def run_splice_helper_gui_noprint(input_data, soundfile, coding_array, isi1, isi2, title, stringColumn= '', isi3 = '',breaktype='', period=''):
	try: 
		print('Running the helper:')
		df = input_data
		print(get_column_names(df))
		print('Add Splice:')
		df = create_df_with_splice_columns(df, isi1, isi2, isi3, stringColumn)
		print('Subsetting:')
		df = create_subset_df_for_list(df, soundfile, coding_array)
		print('Adding Waves')
		df = add_wav_to_stimuli(df, soundfile)
		print('Adding Breaks')
		try:
			df = add_empty_rows(df, breaktype, period)
		except Exception as e:
			print('Empty Rows Error: ', e)
		#try:
		df = fill_break_rows(df, coding_array)
		#except Exception as e:
		#	print('Fill Empty Rows: ', e)
		return df
	except Exception as e:
		print(e)

def run_splice_helper_gui_justprint(outputfilename, inputdata, title, coding_array):
	try:
		print('Creating Output Files:')
		splice_header = configure_splice_header(coding_array)
		print_file(inputdata, splice_header, outputfilename, title)
		return 'Success'
	except Exception as e:
		print(e)

def run_splice_helper(input_file, soundfile, coding_array, isi1, isi2, outputfilename, title, stringColumn= '', isi3 = '', input_file2 = '', merge_on_main_df='', merge_on_other_df=''):
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
		df = create_df_with_splice_columns(df, isi1, isi2, isi3, stringColumn)
		print('Subsetting:')
		df = create_subset_df_for_list(df, soundfile, coding_array)
		print('Adding Waves')
		df = add_wav_to_stimuli(df, soundfile)
		print('Creating OUtput Files:')
		splice_header = configure_splice_header(coding_array)
		print_file(df, splice_header, outputfilename, title)
		return 'Success'
	except Exception as e:
		print(e)
