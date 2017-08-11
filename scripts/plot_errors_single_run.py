"""
Script to plot errors given run_errors_2vars.py run, 
looped over the outer variable.

Created by Nirag Kadakia at 9:30 08-04-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
import matplotlib.pyplot as plt
from load_data import *

try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")


# Relevant variables to load
vars_to_load = ["nX", "nY", "outer_var", "inner_var", "outer_vals", "inner_vals", "iterations"]

# Get data and load relevant variables from file
errors = load_errors(data_flag)
vars_dict, structures = load_structures(data_flag)
for idx in vars_to_load:
	exec("%s = vars_dict['%s']" %(idx,idx))
#nX, nY = len(outer_vals), len(inner_vals)

# Plot errors for each outer variable
for idx, nX in enumerate(outer_vals):
	plt.plot(inner_vals, errors[idx,:], label = "%s" % nX)
plt.yscale('log')
plt.legend()
plt.show()

# Plot minimum errors as a function of outer looped
for idx, nX in enumerate(outer_vals):
	min_error = sp.amin(errors[idx,:])
	plt.scatter(nX, min_error, label = "%s = %s" % (outer_var, nX))
plt.yscale('log')
plt.xlabel('%s' % outer_var)
plt.ylabel('Errors')
plt.legend()
plt.show()
