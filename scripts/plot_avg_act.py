"""
Script to plot value of average activity for conditions of
gives minimum error, as a function of outer loop
variable.

Created by Nirag Kadakia at 9:30 08-04-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import sys
sys.path.append('../src')
import matplotlib.pyplot as plt
from load_data import *
from plots import *


try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")

# Plotting options
options = ['plt.xscale("log")',
			"plt.xlabel(r'$\\langle s_i^0 \\rangle $', fontsize = 12)"]

# Load relevant variables from file
vars_to_load = ["outer_var", "inner_var", "outer_vals", "inner_vals"]


# Get errors and other data
errors = load_errors(data_flag)
vars_dict, structs = load_structs(data_flag)
for idx in vars_to_load:
	exec("%s = vars_dict['%s']" %(idx,idx))
nX, nY = len(outer_vals), len(inner_vals)

# Determine average activity at optimal inner var value; plot
avg_act, opt_inner_val = [], []
for idx in range(nX):
	opt_inner_val.append(sp.argmin(errors[idx,:]))
	avg_act.append(sp.average(structs[idx,opt_inner_val[idx]].Yy))
single_plot(outer_vals, avg_act, xlabel = outer_var, ylabel = 'Average activity', options = options)
