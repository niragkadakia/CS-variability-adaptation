"""
Aggregate CS objects from separate .pklz files to a single file.

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
from save_data import save_aggregated_objects
import cPickle
import gzip

def aggregate_objects():
	"""
	Aggregate CS objects from separate .pklz files to a single .pklz file.
	"""

	data_flag = get_flag()						
	
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)

	iter_vars_dims = []
	for iter_var in iter_vars:
		iter_vars_dims.append(len(iter_vars[iter_var]))		
	it = sp.nditer(sp.zeros(iter_vars_dims), flags = ['multi_index'])

	obj_list  = []
	while not it.finished:
		CS_obj = load_objects(list(it.multi_index), data_flag)
		obj_list.append(CS_obj)
		it.iternext()

	save_aggregated_objects(obj_list, data_flag)

if __name__ == '__main__':
	aggregate_objects()
