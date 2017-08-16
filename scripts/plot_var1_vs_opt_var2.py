"""
Script to plot value of inner loop variable that 
gives minimum error, as a function of outer loop
variable.

Created by Nirag Kadakia at 9:30 08-04-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from save_data import save_figure
from load_data import load_errors, load_explicit_vars
from plots import plot_var1_vs_opt_var2
from utils import get_flag
from stats import power_law_regress, lognormal_regress
import matplotlib.pyplot as plt
sp.set_printoptions(precision = 4, threshold = 5)


data_flag = get_flag()

vars_to_load = ['nX', 'nY', 'outer_vals', 'inner_vals', 'outer_var', 
				'inner_var', 'fixed_vars', 'rel_vars']

vars_dict = load_explicit_vars(data_flag, vars_to_load)
for key in vars_dict: print ('%s = %s' % (key, vars_dict[key]))
errors = load_errors(data_flag)

outer_vals = vars_dict['outer_vals']
inner_vals = vars_dict['inner_vals']

# Find optimal values in inner variables
opt_inner_vals = []
beg, end = 0, -1
for idx, val in enumerate(outer_vals):
	opt_inner_vals.append(inner_vals[sp.argmin(errors[idx,beg:end])])

# Update dictionary
vars_dict['errors'] = errors
vars_dict['opt_inner_vals'] = opt_inner_vals

# Plot
fig = plot_var1_vs_opt_var2(**vars_dict)
plt.yscale('log')

# Add regression line(s)
beg, end = 0,10
#lognormal_regress(outer_vals[beg:end], opt_inner_vals[beg:end])
power_law_regress(outer_vals[beg:end], opt_inner_vals[beg:end])

save_figure(fig, data_flag, 'var1_vs_opt_var2')

