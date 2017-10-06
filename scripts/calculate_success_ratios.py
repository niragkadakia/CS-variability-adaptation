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
from utils import get_flag
from load_specs import read_specs_file
from load_data import load_aggregated_object_list
from analysis import binary_success
from save_data import save_success_ratios

def calculate_success_ratios(data_flag, nonzero_bounds=[0.7, 1.3], 
							zero_bound=1./25.):
	"""
	TODO
	
	Args:
		data_flag: Identifier for saving and loading.
		axes_to_plot: 2-element list indicating which of the iterated 
			variables are to be plotted; first one is the iterated 
			variable; second one will form the x-axis of the plot.
		projected_variable_components: dictionary; keys indicated the name
			of variable to be projected down, value is the component along 
			which it is projected.
	"""
	
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

	successes = sp.zeros(iter_vars_dims)
	
	while not it.finished:
		successes[it.multi_index] = binary_success(
								CS_object_array[it.multi_index], 
								nonzero_bounds=nonzero_bounds,
								zero_bound=zero_bound)
		it.iternext()
	
	save_success_ratios(successes, data_flag)
	
	import matplotlib.pyplot as plt
	plt.plot(iter_vars['mu_dSs'], sp.average(successes, axis = 1))
	plt.show()
	
if __name__ == '__main__':
	data_flag = get_flag()
	calculate_success_ratios(data_flag)