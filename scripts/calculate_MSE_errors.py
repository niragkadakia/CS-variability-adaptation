"""
Calculate estimation error of inferred signal in compressed sensing 
decoding module CS_run.py.

Created by Nirag Kadakia at 17:00 08-20-2017
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
from save_data import save_MSE_errors
from analysis import MSE_errors

def calculate_MSE_errors(data_flag):

	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)

	iter_vars_dims = []
	for iter_var in iter_vars:
		iter_vars_dims.append(len(iter_vars[iter_var]))		
	it = sp.nditer(sp.zeros(iter_vars_dims), flags = ['multi_index'])	

	print ('Loading object list...')
	CS_object_array = load_aggregated_object_list(iter_vars_dims, data_flag)
	print ('...loaded.')

	errors_nonzero = sp.zeros(iter_vars_dims)
	errors_zero = sp.zeros(iter_vars_dims)
	
	while not it.finished:
		errors = MSE_errors(CS_object_array[it.multi_index])
		errors_nonzero[it.multi_index] = errors['errors_nonzero']
		errors_zero[it.multi_index] = errors['errors_zero']
		it.iternext()
	
	save_MSE_errors(errors_nonzero=errors_nonzero, errors_zero=errors_zero, 
						data_flag=data_flag)

if __name__ == '__main__':
	data_flag = get_flag()
	calculate_MSE_errors(data_flag)
