
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
	print(myArray)
	df = df[myArray]
	return df 

testdf = create_subset_df_for_list(df1, 'List', ['Code', 'Other', 'Baggins'])
print(testdf)

