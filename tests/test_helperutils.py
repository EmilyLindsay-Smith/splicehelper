import pytest
import pandas as pd
from splicehelper.helperutils import *

####################################################################################
#TESTS

@pytest.mark.parametrize('filename', [
	'tests/test.csv', 'tests/test.ods', 'tests/test.xls', 'tests/test.xlsm', 'tests/test.xlsx'
	])

def test_create_df_from_input_csv(filename, sample_df):
	testdf = create_df_from_input(filename)
	print(testdf.head())
	pd.testing.assert_frame_equal(testdf, sample_df)


def test_merge_df_with_another_difcol(sample_df, sample_df2, sample_df_merged):
	testdf = merge_df_with_another(sample_df, sample_df2, 'List', 'Fruit')
	pd.testing.assert_frame_equal(testdf,sample_df_merged)

def test_merge_df_with_another_samecol(sample_df, sample_df3, sample_df_merged):
	testdf = merge_df_with_another(sample_df, sample_df3, 'List')
	pd.testing.assert_frame_equal(testdf,sample_df_merged)

def test_create_df_with_splice_columns(sample_df, sample_df_spliced):
	testdf = create_df_with_splice_columns(sample_df, 500, 1000)
	pd.testing.assert_frame_equal(testdf, sample_df_spliced)

def test_create_subset_df_for_list(sample_df_spliced, sample_df_spliced_subset):
	testdf = create_subset_df_for_list(sample_df_spliced, 'List', ['Code', 'Other'])
	pd.testing.assert_frame_equal(testdf, sample_df_spliced_subset)

def test_add_wav_to_stimuli(sample_df_spliced, sample_df_waved):
	testdf = add_wav_to_stimuli(sample_df_spliced, 'List')
	pd.testing.assert_frame_equal(testdf, sample_df_waved)

def test_add_wav_to_stimuli_2(sample_df_spliced_2, sample_df_waved):
	testdf = add_wav_to_stimuli(sample_df_spliced_2, 'List')
	pd.testing.assert_frame_equal(testdf, sample_df_waved)

def test_configure_splice_header(sample_splice_header):
	spliceheader = configure_splice_header(['Cheese', 'Banana', 'Apricot'])
	assert spliceheader == sample_splice_header

def test_get_column_names(sample_df):
	names = get_column_names(sample_df)
	assert names == ['List', 'Code', 'Freq', 'Other']

###################################################################################
#FIXTURES


@pytest.fixture 
def sample_df():
	data = {'List': ['Banana', 'Cherry', 'Kiwi'],
			'Code': ['Prime', 'Target', 'Filler'],
			'Freq': [102, 5099, 3],
			'Other': ['Pretty', 'Little', 'Fish']
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df2():
	data = {'Fruit': ['Banana', 'Cherry', 'Kiwi'],
			'Child': ['A', 'D', 'E'],
			'Baggins': ['G', 'E', 'F']
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df3():
	data = {'List': ['Banana', 'Cherry', 'Kiwi'],
			'Child': ['A', 'D', 'E'],
			'Baggins': ['G', 'E', 'F']
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df_merged():
	data = {'List': ['Banana', 'Cherry', 'Kiwi'],
			'Code': ['Prime', 'Target', 'Filler'],
			'Freq': [102, 5099, 3],
			'Other': ['Pretty', 'Little', 'Fish'],
			'Child': ['A', 'D', 'E'],
			'Baggins': ['G', 'E', 'F']
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df_spliced():
	data = {'List': ['Banana', 'Cherry', 'Kiwi'],
			'Code': ['Prime', 'Target', 'Filler'],
			'Freq': [102, 5099, 3],
			'Other': ['Pretty', 'Little', 'Fish'],
			'! Bleep1': ['BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;'],
			'Bleep2': ['PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, '],
			'Dummy': [0,0,0]
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df_spliced_subset():
	data = {'! Bleep1': ['BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;'],
			'List': ['Banana', 'Cherry', 'Kiwi'],
			'Bleep2': ['PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, '],
			'Code': ['Prime', 'Target', 'Filler'],
			'Other': ['Pretty', 'Little', 'Fish'],
						'Dummy': [0,0,0]
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df_waved():
	data = {'List': ['Banana.wav', 'Cherry.wav', 'Kiwi.wav'],
			'Code': ['Prime', 'Target', 'Filler'],
			'Freq': [102, 5099, 3],
			'Other': ['Pretty', 'Little', 'Fish'],
			'! Bleep1': ['BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;'],
			'Bleep2': ['PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, '],
			'Dummy': [0,0,0]
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture 
def sample_df_spliced_2():
	data = {'List': ['Banana', 'Cherry.wav', 'Kiwi'],
			'Code': ['Prime', 'Target', 'Filler'],
			'Freq': [102, 5099, 3],
			'Other': ['Pretty', 'Little', 'Fish'],
			'! Bleep1': ['BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;',
						'BLEEP; PAUSE, 500;'],
			'Bleep2': ['PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, ','PULSE; PAUSE, 1000; CODE, '],
			'Dummy': [0,0,0]
	}
	df = pd.DataFrame(data)
	return df

@pytest.fixture
def sample_splice_header():
	splice_header="""
	CODEHEAD, Cheese Banana Apricot Dummy 

	ZEROCROSS,on
	PAUSE,4000
	BLEEP; PAUSE,1000; BLEEP; PAUSE,1000; BLEEP;
	PAUSE,2000

	!
	! Countdown
	!

	BLEEP; PAUSE,300; PULSE; STR,5,1000; PAUSE,1000; CODE,0 0 0 0
	BLEEP; PAUSE,300; PULSE; STR,4,1000; PAUSE,1000; CODE,0 0 0 0
	BLEEP; PAUSE,300; PULSE; STR,3,1000; PAUSE,1000; CODE,0 0 0 0
	BLEEP; PAUSE,300; PULSE; STR,2,1000; PAUSE,1000; CODE,0 0 0 0
	BLEEP; PAUSE,300; PULSE; STR,1,1000; PAUSE,1000; CODE,0 0 0 0

	"""
	splice_header = re.sub(r'\t', '', splice_header)
	return splice_header