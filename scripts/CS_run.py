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
from load_data import check_existing_file
from save_data import dump_globals, dump_errors, dump_structures
from load_specs import read_specs_file, parse_iterated_vars, \
						parse_relative_vars
from four_state_receptor_CS import four_state_receptor_CS
import string

data_flag = get_flag()
check_existing_file(data_flag)
vars_to_pass = dict()

# Get the four dictionaries of parameters and variables, pass to locals()
list_dict = read_specs_file(data_flag)
vars_to_pass = parse_iterated_vars(list_dict['iter_vars'], sys.argv[2:], vars_to_pass)
vars_to_pass = parse_relative_vars(list_dict['rel_vars'], iter_vars, vars_to_pass)
vars_to_pass = merge_two_dicts(vars_to_pass, list_dict['fixed_vars'])
vars_to_pass = merge_two_dicts(vars_to_pass, list_dict['params'])

# Run
a = four_state_receptor_CS(**vars_to_pass)
a.encode()
a.decode()
