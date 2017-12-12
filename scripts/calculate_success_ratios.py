"""
Calculate success ratios for CS batch runs, now regarding each CS
estimation as successful or not. 

Created by Nirag Kadakia at 11:00 10-06-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from load_specs import read_specs_file
from load_data import load_binary_errors
from analysis import binary_success
from save_data import save_success_ratios


def calculate_success_ratios(data_flags, threshold_pct_nonzero=85.0, 
							threshold_pct_zero=85.0):
					
	"""
	Calculate success ratios (1 or 0) for a given CS run.
	
	Args:
		data_flags: Identifiers for saving and loading.
		axes_to_plot: 2-element list indicating which of the iterated 
			variables are to be plotted; first one is the iterated 
			variable; second one will form the x-axis of the plot.
		projected_variable_components: dictionary; keys indicated the name
			of variable to be projected down, value is the component along 
			which it is projected.
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

		successes = sp.zeros(iter_vars_dims)
		
		errors = load_binary_errors(data_flag)
		while not it.finished:
			successes[it.multi_index] = binary_success(
						errors['errors_nonzero'][it.multi_index], 
						errors['errors_zero'][it.multi_index], 
						threshold_pct_nonzero=threshold_pct_nonzero,
						threshold_pct_zero=threshold_pct_zero)
			
			it.iternext()
		
		save_success_ratios(successes, data_flag)
		
		
if __name__ == '__main__':
	data_flags = sys.argv[1:]
	calculate_success_ratios(data_flags)