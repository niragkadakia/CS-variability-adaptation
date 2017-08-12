"""
Script to plot errors given run_errors_2vars.py run, 
looped over the outer variable.

Created by Nirag Kadakia at 9:30 08-04-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from save_data import save_figure
from load_data import load_errors, load_explicit_vars
from utils import get_flag
from plots import plot_errors
import matplotlib.pyplot as plt


data_flag = get_flag()

vars_to_load = ['nX', 'nY', 'outer_vals', 'inner_vals', 'outer_var', 
				'inner_var', 'fixed_vars', 'rel_vars']

# Load variables
vars_dict = load_explicit_vars(data_flag, vars_to_load)
errors = load_errors(data_flag)
vars_dict['errors'] = errors

fig = plot_errors(**vars_dict)
save_figure(fig, data_flag, 'errors')
