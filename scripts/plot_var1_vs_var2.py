"""
Script to plot value of inner loop variable that 
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

try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")


	# Relevant variables to load
vars_to_load = ["outer_var", "inner_var", "outer_vals", "inner_vals", "iterations"]

# Get data and load relevant variables from file
errors = load_errors(data_flag)
structs, vars_dict = load_structs(data_flag)

for idx in vars_to_load:
	exec("%s = vars_dict['%s']" %(idx,idx))
nX, nY = len(outer_vals), len(inner_vals)
min_inner_vals = sp.zeros(nX)

# We require a unique stimulus for all runs
assert iterations == 1, "Require 1 iteration of stimulus; iterations = %s" % iterations

# Plot estimated and true stimulus for each of the outer variables
for idx, nX in enumerate(outer_vals):
	min_idx = sp.argmin(errors[idx,:])
	min_inner_vals[idx] = inner_vals[min_idx]

#plt.title('%s = %.2e, max %s = %.2e, error = %.2e' 
#		% (outer_var, nX, inner_var, inner_vals[min_idx], errors[idx, min_idx]))
plt.plot(outer_vals, min_inner_vals)
plt.show()
