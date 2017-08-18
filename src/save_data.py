"""
Functions for saving data for later analysation

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
import matplotlib.pyplot as plt
from local_methods import def_data_dir


DATA_DIR = def_data_dir()

def dump_globals(global_vars, data_flag):
	"""
	Function to dump all globals in a dictionary to file
	"""
	
	f = '%s/globals_%s.out' % (DATA_DIR, data_flag)
	vars_file = shelve.open(f, 'n') 
	for key in global_vars:
		try:
			vars_file[key] = global_vars[key]
		except:
			continue
	vars_file.close()

def dump_structures(structures, data_flag):
	"""
	Function to save all the called CS objects 
	as a zipped pickled file.
	"""

	f = gzip.open('%s/structures_%s.pklz' % (DATA_DIR, data_flag), 'wb')
	cPickle.dump(structures, f, protocol=2)
	f.close()
	
def dump_errors(errors, data_flag):
	"""
	Function to save all the decoding errors of a CS run.
	"""

	sp.savetxt('%s/errors_%s.dat' % (DATA_DIR, data_flag), errors, 
										fmt = "%.5e", delimiter = "\t")	
										

def save_figure(fig, data_flag, suffix):
	"""
	Function to save all the decoding errors of a CS run.
	"""
	
	plt.tight_layout()
	plt.savefig('%s/figures/%s_%s.pdf' %(DATA_DIR, suffix, data_flag), 
				bbox_inches = 'tight')

def save_object_array(iter_vars, iter_vars_idxs, CS_obj, data_flag):
	"""
	Save object instantiation from CS decoder into corresponding 
	entry of pickled array. If pickled array does not exist, 
	create it. Otherwise, load it, and append the current entry.
	
	Args:
		iter_vars: Dictionary of iterated variables and values.
		iter_vars_idxs: Arguments of iterated variable indices from command 
						line arguments.
		CS_obj: The instantiated four_state_receptor_CS object
		data_flag: Data identifier for loading and saving
	"""
	
	filename = '%s/objects/%s.pklz' % (DATA_DIR, data_flag)
	
	# Generate new array or pull from existing file
	if not os.path.exists(filename):
		dims = []
		for keys, val in iter_vars.items(): 
			dims.append(len(val))
		CS_obj_array = sp.empty(dims, dtype = object)
	else:
		with gzip.open(filename, "rb") as f:
			CS_obj_array = sp.asarray(cPickle.load(f))
	
	# Append current data and save
	CS_obj_array[tuple(iter_vars_idxs)] = CS_obj
	with gzip.open(filename, 'wb') as f:
		cPickle.dump(CS_obj_array, f, protocol=2)
