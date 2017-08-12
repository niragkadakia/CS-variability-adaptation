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


default_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/" \
					"nirag_kadakia/data/CS-variability-adaptation"
					
def check_existing_file(data_flag, data_dir = default_dir, 
						prefix = 'structures_', **kwargs):
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

def load_errors(data_flag, data_dir = default_dir, **kwargs):
	"""
	Load error data from compressed sensing 
	encoding/decoding module 
	"""

	errors = sp.loadtxt('%s/errors_%s.dat' %(data_dir, data_flag))
	return errors

def load_structures_globals(data_flag, load_structures = True, 
					data_dir = default_dir, **kwargs):
	"""
	Load globals and class structures from 
	compressed sensing encoding/decoding
	"""

	f = '%s/globals_%s.out' % (data_dir, data_flag)
	shelf_file = shelve.open(f,'r')
	vars_dict = dict()
	for key in shelf_file:
		try:
			vars_dict[key] = shelf_file[key]
		except:
			continue
	
	if load_structures == False:
		return vars_dict
	else:
		f = gzip.open('%s/structures_%s.pklz' % (data_dir, data_flag), 'rb')
		structures = sp.asarray(cPickle.load(f))
		f.close()
		nX, nY = vars_dict["nX"], vars_dict["nY"]
		structures  = structures.reshape((nX, nY))

		return vars_dict, structures
		
def load_explicit_vars(data_flag, vars_to_load, data_dir = default_dir, 
						**kwargs):
	"""
	Load explicit variables from externally 
	shelved file of variables
	"""
	vars_dict = load_structures_globals(data_flag, load_structures = False)
	out_dict = dict()
	for idx in vars_to_load:
		out_dict[idx] = vars_dict[idx]

	return out_dict