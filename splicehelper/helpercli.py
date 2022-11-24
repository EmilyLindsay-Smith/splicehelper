from helperutils import *
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

if __name__ == 'main':
	print('Welcome to SpliceHelper! \n My job is to help you create splice files from your data')
	df = create_inputs()
	create_files(df)