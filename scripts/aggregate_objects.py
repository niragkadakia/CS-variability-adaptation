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
from load_specs import read_specs_file, parse_iterated_vars
						
list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)

vars_to_pass = dict()
vars_to_pass = parse_iterated_vars(iter_vars, iter_var_idxs, vars_to_pass)

for iter_var in iter_vars:
	print (iter_var)