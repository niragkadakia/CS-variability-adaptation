"""
Script to calculate errors in two variables, one as a function of one another 
to minimize decoding errors in 4-state receptor model of compressed 
sensing.

Created by Nirag Kadakia at 23:30 08-02-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import pickle
import shelve
import gzip


def load_errors(data_flag, 
	data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation"):
    
	"""
	Load error data from compressed sensing 
	encoding/decoding module 
	"""

	errors = sp.loadtxt('%s/errors_%s.dat' %(data_dir, data_flag))
	return errors
	
def load_structs(data_flag,
	data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation"):

	"""
	Load globals and class structures from 
	compressed sensing encoding/decoding
	"""

	f = '%s/globals_%s.out' % (data_dir, data_flag)
	vars_dict = shelve.open(f,'r')
	nX, nY = vars_dict["nX"], vars_dict["nY"]
	
	f = gzip.open('%s/structures_%s.pklz' % (data_dir, data_flag), 'rb')
	structs = sp.asarray(pickle.load(f))
	f.close()
	structs  = structs.reshape((nX, nY))

	return structs, vars_dict
