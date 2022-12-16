
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

df = pd.DataFrame(columns=['a','b'],data=[[3,4],[pd.np.nan, pd.np.nan],
    [5,5],[9,3],[1,2],[9,9],[6,5],[6,5],[6,5],[6,5],
    [6,5],[6,5],[6,5],[6,5],[6,5],[6,5],[6,5]])

def add_empty_rows(df, breaktype, period):
	if period == 0 or period == '':
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



def fill_break_rows(df):


	break_row = ['countdown', '1']
	break_row2 = ['countdown', '2']
	break_row3 = ['countdown', '3']
	break_row4 = ['countdown', '4']
	break_row5 = ['countdown', '5']
	break_row0 = ['break', 'break']

	for i in range(0, len(df)):
		if df.isna().iloc[i, 0] == True:
			if df.iloc[i-4][1] == break_row5[1]:
				df.iloc[i] = break_row
			elif df.iloc[i-3][1] == break_row5[1]:
				df.iloc[i] = break_row2
			elif df.iloc[i-2][1] == break_row5[1]:
				df.iloc[i] = break_row3
			elif df.iloc[i-1][1] == break_row5[1]:
				df.iloc[i] = break_row4
			elif df.isna().iloc[i+1, 0] == True:
				df.iloc[i] = break_row5
			else:
				df.iloc[i] = break_row0
	return df

df_result = add_empty_rows(df, 'break', 5)
print(df_result)
df_sole = fill_break_rows(df)
print(df_sole)
df_full = fill_break_rows(df_result)
print(df_full)
df_result2 = add_empty_rows(df, 'countdown', 7)
print(df_result)
df_full2 = fill_break_rows(df_result2)
print(df_full2)


zeroes = []
coding_array = ['TestA', 'TestB', 'TestC']

break_row = ['BLEEP; PAUSE,300', '','; PULSE; STR,1,1000;',' PAUSE,1000; CODE']
break_row2 = ['BLEEP; PAUSE,300', '','; PULSE; STR,2,1000;',' PAUSE,1000; CODE']
break_row3 = ['BLEEP; PAUSE,300', '','; PULSE; STR,3,1000;',' PAUSE,1000; CODE']
break_row4 = ['BLEEP; PAUSE,300', '','; PULSE; STR,4,1000;',' PAUSE,1000; CODE']
break_row5 = ['BLEEP; PAUSE,300', '','; PULSE; STR,5,1000;',' PAUSE,1000; CODE']
break_row0 = ['BLEEP; PAUSE,300', '','; PULSE; 1000;',' PAUSE,1000; CODE']

rows = [break_row, break_row2, break_row3, break_row4, break_row5, break_row0]
[break_row.append(', 0') for i in range(0, len(coding_array)+2) for row in rows]
print(rows)