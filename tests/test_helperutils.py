import pytest
from splicehelper.helperutils import *
def inc(x):
	return x + 1

def test_inc():
	assert inc(3) == 4

def test_doubleme():
	assert doubleme(2) == 4