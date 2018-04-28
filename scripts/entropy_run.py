"""
Run an entropy calculation for one given index of a set of iterated
variables. 

Created by Nirag Kadakia at 12:40 04-26-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
import os
sys.path.append('../src')
from entropy import response_entropy
from utils import get_flag
from load_specs import read_specs_file, compile_all_run_vars
from save_data import dump_objects


def entropy_run(data_flag, iter_var_idxs):
	"""
	Run an entropy calculation one given index of a set of iterated
	variables. 

	Data is read from a specifications file in the data_dir/specs/ 
	folder, with proper formatting given in read_specs_file.py. The
	specs file indicates the full range of the iterated variable; this
	script only produces output from one of those indices, so multiple
	runs can be performed in parallel.
	"""
	
	# Aggregate all run specifications from the specs file; instantiate model
	list_dict = read_specs_file(data_flag)
	vars_to_pass = compile_all_run_vars(list_dict, iter_var_idxs)
	obj = response_entropy(**vars_to_pass)
	
	# Basic setting of Kk1, etc.; Ss, Yy, and eps will be overwritten below.
	obj.encode_power_Kk()
	
	# Set the signals and free energy, depending if adaptive or not.
	if 'run_type' in list_dict['run_specs'].keys():
		val = list_dict['run_specs']['run_type']
		if val[0] == 'encode_entropy_calc':
			obj.encode_entropy_calc()
		elif val[0] == 'encode_entropy_calc_adapted':
			obj.encode_entropy_calc_adapted()
		else:
			print '`%s` run type not accepted for entropy calculation' % val[0]
			quit()
	else:
		print ('No entropy calculation run type specified, proceeding with' \
				'unadapted entropy calculation')
		obj.encode_entropy_calc()
	
	# Calculate the response pdfs, entropy, and mutual information
	obj.set_mean_response_array()
	obj.set_response_pdf()
	obj.calc_MI()
	
	dump_objects(obj, iter_var_idxs, data_flag)
	
	
if __name__ == '__main__':
	data_flag = get_flag()
	iter_var_idxs = map(int, sys.argv[2:])
	entropy_run(data_flag, iter_var_idxs)
