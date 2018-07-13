"""
Aggregate CS objects from for nn runs; this saves
the salient data structures rather than each CS object, 
due to space limitations and redundancy.

Created by Nirag Kadakia at 22:50 07-13-2018
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
from load_data import load_objects
from save_data import save_aggregated_temporal_objects
from utils import get_flags


def aggregate_nn_objects(data_flags):
	
	structs_to_save = ['test_data_in', 'test_data_labels', 'test_data_calc']
	
	# Convert single element list to list
	if isinstance(data_flags, str):
		data_flags = [data_flags]
	
	for data_flag in data_flags:
		list_dict = read_specs_file(data_flag)
		iter_vars = list_dict['iter_vars']
		iter_vars_dims = []
		for iter_var in iter_vars:
			iter_vars_dims.append(len(iter_vars[iter_var]))		
		it = sp.nditer(sp.zeros(iter_vars_dims), flags = ['multi_index'])
		
		CS_init_array = load_objects(list(it.multi_index), data_flag)

		data = dict()
		
		# Assign data structures of appropriate shape for the variables to save
		for struct_name in structs_to_save:
			try:
				tmp_str = 'struct = CS_init_array.%s' % struct_name
				exec(tmp_str)
			except:
				print('%s not an attribute of the CS object' % struct_name)
				continue

			# shape is (iterated var ranges, variable shape); 
			struct_shape = tuple(iter_vars_dims)
			if hasattr(struct, 'shape'):
				struct_shape += (struct.shape)
			data['%s' % struct_name] = sp.zeros(struct_shape)

		# Iterate over all objects to be aggregated
		while not it.finished:
			
			print('Loading index:', it.multi_index)
			nn_obj_array = load_objects(list(it.multi_index), data_flag)
			
			for struct_name in structs_to_save:
				tmp_str = 'struct = nn_obj_array.%s' % struct_name
				exec(tmp_str)
				data[struct_name][it.multi_index] = struct
			
			it.iternext()
		
		# Save one copy of last array for other variables common to all runs
		data['CS_obj'] = nn_obj_array
		
		save_aggregated_nn_objects(data, data_flag)

if __name__ == '__main__':
	data_flags = get_flags()
	aggregate_nn_objects(data_flags)
