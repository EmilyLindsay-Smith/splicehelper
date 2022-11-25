
import pandas as pd

data = {'List': ['Banana', 'Cherry', 'Kiwi'],
		'Code': ['Prime', 'Target', 'Filler'],
		'Freq': [102, 5099, 3],
		'Other': ['Pretty', 'Little', 'Fish'],
		'Child': ['A', 'D', 'E'],
		'Baggins': ['G', 'E', 'F']
}
df1 = pd.DataFrame(data)


data2 = {'! Bleep1': ['BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;'],
			'List': ['Banana', 'Cherry', 'Kiwi'],
			'Bleep2': ['PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, '],
			'Code': ['Prime', 'Target', 'Filler'],
			'Other': ['Pretty', 'Little', 'Fish'],
			'Baggins': ['G', 'E', 'F'],
						'Dummy': [0,0,0]
	}
df2 = pd.DataFrame(data2)

colname = "Other"
df2['VisualStimuli'] = [', '.join(i) for i in zip(df2["Code"],df2["Other"])]

isi3= 500
df2['VisualStimuli2'] =Bleep2 = [f" PULSE; STR, {i}, {isi3}" for i in df2[colname]]

def create_df_with_splice_columns(df, isi1, isi2, isi3 = '', stringColumn = ''):
	#Define Splice Line Start

	Bleep1 = f'BLEEP; PAUSE, {isi1};'
	df['! Bleep1'] = Bleep1

	# Define splice string whether visual stimuli present or not
	if stringColumn == '':
		df['Bleep2'] = ' PULSE'
	else:
		stringColumn = stringColumn
		df['Bleep2'] = [f" PULSE; STR, {i}, {isi3}" for i in df[stringColumn]]
	
	# Define final splice code 
	Bleep3 = f'; PAUSE, {isi2}; CODE, '
	df['Bleep3'] = Bleep3
	df['Dummy'] = 0
	return df

df3 = create_df_with_splice_columns(df2, 300, 500, 400, 'Other')
print(df3)