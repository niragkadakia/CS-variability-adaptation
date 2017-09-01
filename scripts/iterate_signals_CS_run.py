"""
Run a CS decoding run for one given index of a set of iterated
variables, iterating over many different signals 

Created by Nirag Kadakia at 13:00 09-01-2017
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
from utils import merge_two_dicts, get_flag
from save_data import dump_objects
from load_specs import read_specs_file, parse_iterated_vars, \
						parse_relative_vars
from four_state_receptor_CS import four_state_receptor_CS


def iterate_signals_CS_run(signal_ensemble_size=100):
	"""
	Run a CS decoding run for one given index of a set of iterated
	variables, over many statistical iterations with different seeds
	for the randomly chosen signals

	Data is read from a specifications file in the data_dir/specs/ 
	folder, with proper formatting given in read_specs_file.py. The
	specs file indicates the full range of the iterated variable. This
	script only produces output from one of those indices, so multiple
	runs can be performed in parallel.
	"""
	
	data_flag = get_flag()
	iter_var_idxs = map(int, sys.argv[2:])
	
	# Get the five dictionaries of variables and run specifications, 
	# and pass to locals()
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)
	
	vars_to_pass = dict()
	vars_to_pass = parse_iterated_vars(iter_vars, iter_var_idxs, vars_to_pass)
	vars_to_pass = parse_relative_vars(rel_vars, iter_vars, vars_to_pass)
	vars_to_pass = merge_two_dicts(vars_to_pass, fixed_vars)
	vars_to_pass = merge_two_dicts(vars_to_pass, params)

	a = four_state_receptor_CS(**vars_to_pass)
	
	if 'run_type' not in run_specs.keys():
		print ('Run type not specified, proceeding with "normal_activity"')
		a.encode_normal_activity()
	
	for key, val in run_specs.items():
		if key == 'run_type':
			if val[0] == 'normal_Kk':
				a.encode_normal_Kk()
			elif val[0] == 'normal_activity':
				a.encode_normal_activity()
			elif val[0]  == 'normal_activity_WL':
				WL_rule = dict(eps = float(val[1]) + float(val[2])
								*sp.log(vars_to_pass['mu_Ss0']))
				a.encode_normal_activity_WL(**WL_rule)
			else:
				print ('run type %s not recognized' % val[0])
		else:
			'Run specification %s not recognized' % key 
	
	# TODO -- save these in a meaningful way
	for iSignal in range(signal_ensemble_size):
		import matplotlib.pyplot as plt
		a.seed_dSs = iSignal
		a.set_signals()
		a.set_measured_activity()
		a.decode()
		a.set_linearized_response() 
		plt.plot(a.dSs_est)
		plt.plot(a.dSs)
		plt.show()
		print '\n'
		
	dump_objects(iter_vars, iter_var_idxs, a, data_flag)
	
if __name__ == '__main__':
	iterate_signals_CS_run(signal_ensemble_size=100)
