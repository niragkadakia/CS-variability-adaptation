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
import time
import matplotlib.pyplot as plt
from local_methods import def_data_dir

DATA_DIR = def_data_dir()

def save_errors(errors, data_flag):
	"""
	Save decoding error from array of CS objects as numpy object.

	Args:
		errors: Error array to be saved
		data_flag: Data identifier for saving and loading.
	"""

	out_dir = '%s/analysis/%s' % (DATA_DIR, data_flag)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	filename = '%s/errors.npz' % out_dir
	sp.savez(filename, errors = errors)	
	print ('\nSignal errors file saved to %s' % filename)
										
def save_figure(fig, suffix, data_flag):
	"""
	Save a generic figure.
	
	Args: 
		fig: Figure object to be saved.
		suffix: Type of figure. Ex: 'error_plot'.
		data_flag: Data identifier for saving and loading.
	"""
	
	out_dir = '%s/figures/%s/' % (DATA_DIR, data_flag)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	
	filename = '%s/%s_%s.pdf' %(out_dir, suffix, data_flag)
	plt.tight_layout()
	plt.savefig(filename, bbox_inches = 'tight')

def dump_objects(iter_vars, iter_vars_idxs, CS_obj, data_flag):
	"""
	Save object instantiation from CS decoder as pickled object.
	
	Args:
		iter_vars: Dictionary of iterated variables and values.
		iter_vars_idxs: Arguments of iterated variable indices from command 
						line arguments.
		CS_obj: The instantiated four_state_receptor_CS object
		data_flag: Data identifier for loading and saving
	"""
	
	out_dir = '%s/objects/%s' % (DATA_DIR, data_flag)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	
	filename = '%s/%s.pklz' % (out_dir, iter_vars_idxs)
	with  gzip.open(filename, 'wb') as f:
		cPickle.dump(CS_obj, f, protocol = 2)
	print ("\n -- Object array item %s saved." % iter_vars_idxs)
	
def save_aggregated_object_list(agg_obj_list, data_flag):
	"""
	Save list of aggregated objects to file.
	
	Args:
		agg_obj_list: List of four_state_receptor_CS objects.
		data_flag: Data identifier for loading and saving.
	"""
	
	filename = '%s/objects/%s/aggregated_objects.pklz' % (DATA_DIR, data_flag)

	with gzip.open(filename, 'wb') as f:
		cPickle.dump(agg_obj_list, f, protocol = 2)

	print ('Aggregated object file %s saved.' % filename)
