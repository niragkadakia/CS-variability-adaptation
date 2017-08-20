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
from local_methods import def_data_dir


DATA_DIR = def_data_dir()
					

def load_errors(data_flag):
	"""
	Load error data from compressed sensing encoding/decoding module.
	
	Args: 
		data_flag: Name of shelved file of globals (.out).
	
	Returns:
		errors: numpy array of errors loaded from file.
	"""

	errors = sp.loadtxt('%s/errors_%s.dat' %(DATA_DIR, data_flag))
	return errors

def load_explicit_vars(vars_to_load, data_flag):
	"""
	Load an explicitly defined set of variables from externally shelved 
	file of variables into a dictionary.
	
	Args: 
		vars_to_load: List of variable names as strings to load into 
						the dictionary.
		data_flag: Name of shelved file of globals (.out).
	
	Returns:
		out_dict: Dictionary of keyed items and their respective values.
	"""
	
	vars_dict = load_structures_globals(data_flag, load_structures = False)
	out_dict = dict()
	for idx in vars_to_load:
		out_dict[idx] = vars_dict[idx]

	return out_dict

def load_objects(obj_idx, data_flag):
	"""
	Load objects saved by save_objects in the save_data module. 

	Args:
		obj_idx: List whose indices corresponding to name of saved *.npz 
					file holding object array.
		data_flag: Data identifier for loading and saving.
	"""

	filename = '%s/objects/%s/%s.npz' % (DATA_DIR, data_flag, obj_idx)
	obj = sp.load(filename)
	
	return obj
