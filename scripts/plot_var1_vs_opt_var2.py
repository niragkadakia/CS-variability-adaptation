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
from load_data import *
from plots import *
from scipy.stats import linregress


try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")

#Plotting options
options = ["plt.xlabel(r'$\\langle s_i - s_i^0 \\rangle $', fontsize = 20)",
			"plt.ylabel(r'Optimal $\\epsilon $', fontsize=20)",
			'plt.xscale("log")', 
			'plt.xticks(fontsize=12)', 'plt.yticks(fontsize=12)']
			
# Relevant variables to load
vars_to_load = ["outer_var", "inner_var", "outer_vals", "inner_vals", 
				"nX", "nY", "fixed_vars", "rel_vars"]
		
# Get data and load relevant variables from file
errors = load_errors(data_flag)
vars_dict = load_structs(data_flag, skip_structs = True)
print (vars_dict)
for idx in vars_to_load:
	exec("%s = vars_dict['%s']" %(idx,idx))
print ("Fixed variables: %s\nRelative variables: %s\n"  % (fixed_vars, rel_vars))


# Plot optimal inner variable for each of the outer variables
opt_inner_vals = sp.zeros(nX)
for idx, nX in enumerate(outer_vals):
	min_idx = sp.argmin(errors[idx,:])
	opt_inner_vals[idx] = inner_vals[min_idx]
single_plot(outer_vals, opt_inner_vals, xlabel = outer_var, ylabel = inner_var, options = options, no_show = True)

# Linear Fitting
beg = 12 #0 #12
end = 38 #35 #38
m, b, r_value, p_value, std_err = linregress(sp.log(outer_vals[beg:end]), opt_inner_vals[beg:end])
single_plot(outer_vals[beg:end], m * sp.log(outer_vals[beg:end]) + b, options = options, no_show = False)
print (r_value**2.)
print (m)
print (b)

#m, b, r_value, p_value, std_err = linregress(sp.log(outer_vals[beg:end]), sp.log(opt_inner_vals[beg:end]))
#single_plot(outer_vals[beg:end], sp.exp(m * sp.log(outer_vals[beg:end]) + b), options = options, no_show = False)
#print (r_value**2.)
#print (m)
#print (b)
