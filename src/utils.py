"""
General, miscellaneous functions for CS decoding scripts.

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys


def get_flag():
	"""
	Get the command line arguments
	"""
	try:
		data_flag = str(sys.argv[1])
	except:
		raise Exception("Need to specify a tag for the data")
	
	return data_flag

def merge_two_dicts(x, y):
   	"""
	Given two dicts, merge them into a 
	new dict as a shallow copy.
	"""

	z = x.copy()
	z.update(y)
	
	return z
		
def noisify(Ss, params):
	"""
	Adds noise to any vector
	"""
	
	mu, sigma = params
	size = Ss.shape
	Ss += sp.random.normal(mu, sigma, size)
	
	return Ss
	
