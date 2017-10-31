"""
Functions for loading data for analysis.

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

	filename = '%s/objects/%s/%s.pklz' % (DATA_DIR, data_flag, obj_idx)
	with gzip.open(filename, 'rb') as f:
		obj = cPickle.load(f)
	
	return obj
	
def load_aggregated_object_list(iter_vars_dims, data_flag):
	"""
	Load objects saved by aggregated_objects module; in correct array
	reflecting the shape of the iterated variables.

	Args:
		data_flag: Data identifier for loading and saving.
	
	Returns:
		agg_obj: Array of objects
	"""

	filename = '%s/objects/%s/aggregated_objects.pklz' % (DATA_DIR, data_flag)
	with gzip.open(filename, 'rb') as f:
		CS_object_list = cPickle.load(f)
	
	CS_object_array = sp.reshape(CS_object_list, iter_vars_dims)

	return CS_object_array

def load_MSE_errors(data_flag):
	"""
	Load .npz file containing error data.

	Args:
		data_flag: Data identifier for loading and saving.
	
	Returns:
		errors: Numpy object containing error data.
	"""

	filename = '%s/analysis/%s/MSE_errors.npz' % (DATA_DIR, data_flag)
	errors = dict()
	infile = sp.load(filename)
	errors['errors_nonzero'] = infile['errors_nonzero']
	errors['errors_zero'] = infile['errors_zero']
	
	return errors
	
def load_binary_errors(data_flag):
	"""
	Load .npz file containing error data.

	Args:
		data_flag: Data identifier for loading and saving.
	
	Returns:
		errors: Numpy object containing error data.
	"""
	
	filename = '%s/analysis/%s/binary_errors.npz' % (DATA_DIR, data_flag)
	errors = dict()
	infile = sp.load(filename)
	errors['errors_nonzero'] = infile['errors_nonzero']
	errors['errors_zero'] = infile['errors_zero']
	
	return errors

def load_binary_errors_dual_odor(data_flag):
	"""
	Load .npz file containing error data.

	Args:
		data_flag: Data identifier for loading and saving.
	
	Returns:
		errors: Numpy object containing error data.
	"""
	
	filename = '%s/analysis/%s/binary_errors.npz' % (DATA_DIR, data_flag)
	errors = dict()
	infile = sp.load(filename)
	errors['errors_nonzero'] = infile['errors_nonzero']
	errors['errors_nonzero_2'] = infile['errors_nonzero_2']
	errors['errors_zero'] = infile['errors_zero']
	
	return errors
	
def load_success_ratios(data_flag):
	"""
	Load list of successes based on decoding error of CS
	objects.
	
	Args:
		data_flag: Data identifier for loading and saving.
		
	Returns:
		successes: numpy object of success ratio data
	"""
	
	filename = '%s/analysis/%s/successes.npz' % (DATA_DIR, data_flag)
	infile = sp.load(filename)
	successes = infile['successes']
	
	return successes