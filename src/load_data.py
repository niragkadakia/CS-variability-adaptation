"""
Functions for loading data to plot and analyze data.

Created by Nirag Kadakia at 23:30 08-02-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import cPickle
import shelve
import gzip
import os

def check_existing_file(data_flag, 
						data_dir = "C:\Users/nk479/Dropbox " \
						"(emonetlab)/users/nirag_kadakia/data" \
						"/CS-variability-adaptation", prefix = 'structures_'):
	"""
	Check if file exists by data flag; 
	prompt to overwrite
	"""

	if os.path.isfile("%s/%s%s.pklz" % (data_dir, prefix, data_flag)) == True:
		overwrite = None
		while overwrite != ('n' or 'y'):
			overwrite = raw_input('Overwrite, y or n? ')
			if overwrite == 'y':
				break
			elif overwrite == 'n':
				print ('Specify different data flag')
				exit()
		


def load_errors(data_flag, 
	data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/" \
				"nirag_kadakia/data/CS-variability-adaptation"):
    
	"""
	Load error data from compressed sensing 
	encoding/decoding module 
	"""

	errors = sp.loadtxt('%s/errors_%s.dat' %(data_dir, data_flag))
	return errors

	
def load_structs(data_flag, skip_structs = False,
	data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/" \
				"nirag_kadakia/data/CS-variability-adaptation"):

	"""
	Load globals and class structures from 
	compressed sensing encoding/decoding
	"""

	f = '%s/globals_%s.out' % (data_dir, data_flag)
	vars_dict = shelve.open(f,'r')
	
	if skip_structs == True:
		return vars_dict
	else:
		f = gzip.open('%s/structures_%s.pklz' % (data_dir, data_flag), 'rb')
		structs = sp.asarray(cPickle.load(f))
		f.close()
		nX, nY = vars_dict["nX"], vars_dict["nY"]
		structs  = structs.reshape((nX, nY))

		return vars_dict, structs
