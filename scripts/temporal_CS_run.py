"""
Run a CS decoding run for a time-varying signal.

Created by Nirag Kadakia at 22:26 01-17-2018
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
from four_state_receptor_CS import four_state_receptor_CS
from utils import get_flag
from save_data import dump_objects
from load_specs import read_specs_file, compile_all_run_vars
from encode_CS import single_encode_CS
from analysis import binary_errors


def temporal_CS_run(data_flag, iter_var_idxs, sigma_Ss0=0, 
					mu_dSs=0, mu_dSs_multiplier=1./3., sigma_dSs=0, 
					sigma_dSs_multiplier=1./9., signal_window=None):
	"""
	Run a CS decoding run for a full temporal signal trace.

	Data is read from a specifications file in the data_dir/specs/ 
	folder, with proper formatting given in read_specs_file.py. The
	specs file indicates the full range of the iterated variable; this
	script only produces output from one of those indices, so multiple
	runs can be performed in parallel.
	"""
	
	assert mu_dSs >= 0, "mu_dSs kwarg must be >= 0"
	assert sigma_dSs >= 0, "sigma_dSs kwarg must be >= 0"
	
	vars_to_save = ['dYy', 'Yy', 'Yy0', 'eps', 'dSs_est', 'dSs', 'Ss0', 'Ss']
	
	# Aggregate all run specifications from the specs file; instantiate model
	list_dict = read_specs_file(data_flag)
	vars_to_pass = compile_all_run_vars(list_dict, iter_var_idxs)
	obj = four_state_receptor_CS(**vars_to_pass)
		
	# Set the temporal signal array from file; truncate to signal window
	obj.set_signal_trace()
	assert sp.sum(obj.signal_trace <= 0) == 0, \
		"Signal contains negative values; increase signal_trace_offset"
	if signal_window is not None:
		obj.signal_trace = obj.signal_trace[signal_window[0]: signal_window[1]]
	
	for iT, signal in enumerate(obj.signal_trace):
		print '%s/%s' % (iT + 1, len(obj.signal_trace)), 
		
		# Set estimation dSs values from signal trace and kwargs
		obj.mu_Ss0 = signal		
		obj.sigma_Ss0 = sigma_Ss0
		obj.mu_dSs = mu_dSs + signal*mu_dSs_multiplier
		obj.sigma_dSs = sigma_dSs + signal*sigma_dSs_multiplier
						
		# Encode / decode fully first time; then just update eps and responses
		if iT == 0:
			obj = single_encode_CS(obj, list_dict['run_specs'])
		else:
			obj.set_sparse_signals()
			obj.set_temporal_adapted_epsilon()
			obj.set_measured_activity()
			obj.set_linearized_response()
		
		# Estimate signal at point iT
		obj.decode()
		
		# At first, create data structures of appropriate size
		if iT == 0:
			data = dict()
			for var_name in vars_to_save:
				tmp_str = 'var_shape = obj.%s.shape' % var_name
				exec(tmp_str)
				array_shape = sp.hstack((len(obj.signal_trace), var_shape))
				data[var_name] = sp.zeros(array_shape)
	
		# Save all relevant variables
		for var_name in vars_to_save:
			tmp_str = 'data[var_name][iT, :] = obj.%s' % var_name
			exec(tmp_str)
	
	# Add full object for other static variables that may be needed
	data['CS_obj'] = obj
	dump_objects(data, iter_var_idxs, data_flag)

	
if __name__ == '__main__':
	data_flag = get_flag()
	iter_var_idxs = map(int, sys.argv[2:])
	temporal_CS_run(data_flag, iter_var_idxs)
