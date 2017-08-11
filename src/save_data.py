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


default_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/" \
					"nirag_kadakia/data/CS-variability-adaptation"

def dump_globals(global_vars, data_flag, data_dir = default_dir, **kwargs):
	"""
	Function to dump all globals in a dictionary to file
	"""
	
	f = '%s/globals_%s.out' % (data_dir, data_flag)
	vars_file = shelve.open(f, 'n') 
	for key in global_vars:
		try:
			vars_file[key] = global_vars[key]
		except:
			continue
	vars_file.close()

def dump_structures(structures, data_flag, data_dir = default_dir, **kwargs):
	"""
	Function to save all the called CS objects 
	as a zipped pickled file.
	"""

	f = gzip.open('%s/structures_%s.pklz' % (data_dir, data_flag), 'wb')
	cPickle.dump(structures, f, protocol=2)
	f.close()
	
def dump_errors(errors, data_flag, data_dir = default_dir, **kwargs):
	"""
	Function to save all the decoding errors of a CS run.
	"""

	sp.savetxt('%s/errors_%s.dat' % (data_dir, data_flag), errors, 
										fmt = "%.5e", delimiter = "\t")	
										

def save_figure(fig, data_flag, suffix, data_dir = default_dir, **kwargs):
	"""
	Function to save all the decoding errors of a CS run.
	"""
	
	plt.savefig('%s/figures/%s_%s.pdf' %(data_dir, suffix, data_flag), 
				bbox_inches = 'tight')
	