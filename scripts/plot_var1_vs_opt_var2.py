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
from load_data import load_errors, load_structures
from plots import plot_var1_vs_opt_var2
from utils import merge_two_dicts, get_flag
from stats import power_law_regress, lognormal_regress
import matplotlib.pyplot as plt


data_flag = get_flag()

# Load shelved variables and errors from run
errors = load_errors(data_flag)
vars_dict = load_structures(data_flag, skip_structures = True)
vars_to_load = ['nX', 'nY', 'outer_vals', 'inner_vals', 'outer_var', 
				'inner_var', 'fixed_vars', 'rel_vars']
for idx in vars_to_load:
	exec("%s = vars_dict[idx]" % idx)
print ("Fixed: %s\nRelative: %s\n"  % (fixed_vars, rel_vars))

# Find optimal values in inner vector
opt_inner_vals = sp.zeros(nX)
for idx, nX in enumerate(outer_vals):
	min_idx = sp.argmin(errors[idx,:])
	opt_inner_vals[idx] = inner_vals[min_idx]

# Plot
fig = plot_var1_vs_opt_var2(outer_vals, opt_inner_vals, **vars_dict)
plt.xscale('log')

# Add regression line
beg, end = 2, 36
#power_law_regress(outer_vals[beg:end], opt_inner_vals[beg:end])
lognormal_regress(outer_vals[beg:end], opt_inner_vals[beg:end])

# Save figure 
save_figure(fig, data_flag, 'var1_vs_opt_var2')

