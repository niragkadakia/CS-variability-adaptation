"""
Calculate estimation error of inferred signal in compressed sensing 
decoding module CS_run.py, treating zero and nonzero elements on their
own footing, and quantifying coding fidelity via number of correct or 
incorrectly identified components.

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
from utils import get_flag
from load_specs import read_specs_file
from load_data import load_aggregated_object_list
from save_data import save_binary_errors

def calculate_binary_errors(data_flag, nonzero_bounds=[0.6, 1.4], 
							zero_bound=1./30):

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

	errors_nonzero_components = sp.zeros(iter_vars_dims)
	errors_zero_components = sp.zeros(iter_vars_dims)
	
	while not it.finished:
		Nn = CS_object_array[it.multi_index].Nn
		mu_dSs = CS_object_array[it.multi_index].mu_dSs
		nonzero_components =  CS_object_array[it.multi_index].idxs[0]
		for iN in range(Nn):
			if iN in nonzero_components: 
				scaled_component_estimate = \
					CS_object_array[it.multi_index].dSs_est[iN]/ \
					CS_object_array[it.multi_index].dSs[iN]
				if nonzero_bounds[0] < scaled_component_estimate < \
				nonzero_bounds[1]:
					errors_nonzero_components[it.multi_index] += 1
			else:
				if abs(CS_object_array[it.multi_index].dSs_est[iN]) \
				<  abs(mu_dSs*zero_bound):
					errors_zero_components[it.multi_index] += 1
		errors_nonzero_components[it.multi_index] = sp.around(
			errors_nonzero_components[it.multi_index]/ \
			len(nonzero_components)*100., 2)
		errors_zero_components[it.multi_index] = sp.around(
			errors_zero_components[it.multi_index]/ \
			(Nn - len(nonzero_components))*100., 2)
			
		it.iternext()
	
	save_binary_errors(errors_nonzero_components, errors_zero_components, 
						data_flag)
	
if __name__ == '__main__':
	data_flag = get_flag()
	calculate_binary_errors(data_flag)
