"""
Aggregate all saved objects from a CS decoding run into a single file for 
analysis.

Created by Nirag Kadakia at 22:50 08-19-2017
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
from load_specs import read_specs_file, parse_iterated_vars
from local_methods import def_data_dir
from load_data import load_objects

def aggregate_objects():

	data_flag = get_flag()						
	

	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)

	iter_vars_dims = []
	for iter_var in iter_vars:
		iter_vars_dims.append(len(iter_vars[iter_var]))

	it = sp.nditer(sp.empty(iter_vars_dims), flags = ['multi_index'])

	while not it.finished:
		load_objects(list(it.multi_index), data_flag)
		it.iternext()

if __name__ == '__main__':
	aggregate_objects()
