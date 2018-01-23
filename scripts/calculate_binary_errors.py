"""
Calculate estimation error of inferred signal in compressed sensing 
decoding module CS_run.py, treating zero and nonzero elements on their
own footing, and quantifying coding fidelity via number of correct or 
incorrectly identified components. Script calls source code from 
analysis.py

Created by Nirag Kadakia at 15:00 09-05-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import sys
sys.path.append('../src')
from load_specs import read_specs_file
from load_data import load_aggregated_object_list
from save_data import save_binary_errors
from analysis import binary_errors


def calculate_binary_errors(data_flags, nonzero_bounds=[0.75, 1.25], 
							zero_bound=1./10.):
	"""
	Calculate whether or not a CS estimation is above or below a threshold, 
	depending on both the nonzero and zero components of the signal.
	
	Args:
		data_flags: strings identifying the data objects.
		nonzero_bounds: floats for lower and upper bound as a factor of 
			the true signal. Thus, 0.5 to 1.5 implies that the estimated 
			signal for that component must be no less than the half the
			true signal component and no greater than one-and-half times 
			the true signal component.
		zero_bound: float for lower bounds on the zero components, as a 
			factor of mu_dSs, the average of the signal components.
	"""
	
	
	# Convert single element list to list
	if not hasattr(data_flags,'__iter__'):
		data_flags = [data_flags]
	
	for data_flag in data_flags:
	
		list_dict = read_specs_file(data_flag)
		for key in list_dict:
			exec("%s = list_dict[key]" % key)

		iter_vars_dims = []
		for iter_var in iter_vars:
			iter_vars_dims.append(len(iter_vars[iter_var]))		
		it = sp.nditer(sp.zeros(iter_vars_dims), flags = ['multi_index'])	

		print ('Loading object list...'),
		CS_object_array = load_aggregated_object_list(iter_vars_dims, data_flag)
		print ('...loaded.')

		errors_nonzero = sp.zeros(iter_vars_dims)
		errors_zero = sp.zeros(iter_vars_dims)
		
		while not it.finished:
			errors = binary_errors(CS_object_array[it.multi_index], 
									nonzero_bounds=nonzero_bounds,
									zero_bound=zero_bound)
			errors_nonzero[it.multi_index] = errors['errors_nonzero']
			errors_zero[it.multi_index] = errors['errors_zero']
			it.iternext()
		
		save_binary_errors(errors_nonzero, errors_zero, data_flag)
		
		
if __name__ == '__main__':
	data_flags = sys.argv[1:]
	calculate_binary_errors(data_flags)
