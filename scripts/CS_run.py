"""
TODO

Created by Nirag Kadakia at 14:40 09-17-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from utils import merge_two_dicts, get_flag
from load_data import check_existing_file, read_specs_file
from save_data import dump_globals, dump_errors, dump_structures
from four_state_receptor_CS import four_state_receptor_CS
import string

data_flag = get_flag()
check_existing_file(data_flag)

# Get the four dictionaries of parameters and variables, pass to globals
list_dict = read_specs_file(data_flag)
for key in list_dict:
	exec("%s = list_dict[key]" % key)

# Check for proper number of command line arguments
assert len(sys.argv) == len(iter_vars) + 2, "Need %s command line args "\
											"(%s supplied)" % (len(iter_vars),
											len(sys.argv) - 2)
											
vars_to_pass = dict()

# Get iterated variable values from range, pass to argument dictionary
print (' -- Running iterated variables with values:\n')
for i_sys_arg, var_name in enumerate(iter_vars.keys()):
	idx = int(sys.argv[2 + i_sys_arg])
	vars_to_pass[var_name] = iter_vars[var_name][idx]
	print ('%s    \t = %s' %  (var_name, vars_to_pass[var_name]))

# Get relative variables, check to ensure dependency is meaningful
print ('\n -- Variables relative to others:\n')
for var_name, var_val in rel_vars.items():
	assert var_name not in vars_to_pass, 'Relative variable %s is already'\
											'being iterated' % var_name
	flag = False
	for iter_var_name in iter_vars.keys():
		if iter_var_name in var_val:
			flag = True
			tmp_str = var_val.replace(iter_var_name, '%s' % vars_to_pass[iter_var_name])
			vars_to_pass[var_name] = eval(tmp_str)
			break
		else:
			continue
	
	assert flag == True, 'Assignment %s <-- %s does not depend on any '\
							'iterated variables' % (var_name, var_val)	
	print ('%s = %s <-- %s' % (var_val, vars_to_pass[var_name], var_name))

# Add fixed variables and overridden parameters

vars_to_pass = merge_two_dicts(vars_to_pass, fixed_vars)
vars_to_pass = merge_two_dicts(vars_to_pass, params)

# Run
a = four_state_receptor_CS(**vars_to_pass)
a.encode()
a.decode()
