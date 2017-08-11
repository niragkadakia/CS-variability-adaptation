"""
Script to calculate errors in two variables, one as a function of one another 
to minimize decoding errors in 4-state receptor model of compressed 
sensing.

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from four_state_receptor_CS import four_state_receptor_CS
from utils import merge_two_dicts
from load_data import check_existing_file
from save_data import dump_globals, dump_errors, dump_structures
from plots import iter_plots
import string


try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")
check_existing_file(data_flag, prefix = 'structures_')
	

# Parameters to sweep and their respective ranges
iterations = 1
outer_var = "mu_Ss0"
inner_var = "mu1_eps"
outer_vals = 10.**sp.linspace(-2, 1, 5) 
inner_vals = sp.linspace(0, 20, 5) 

# Parameters to hold fixed
fixed_vars =  dict(sigma1_eps = 0., sigma_Ss0=1e-2, sigma_dSs = 1e-3)

# Relative paramaters as a function of swept parameters
#rel_vars = [['mu1_eps', '2*sp.log(mu_Ss0)'], ['sigma_dSs', 'mu_dSs/5.']]
rel_vars = [['mu_dSs', 'mu_Ss0/1.0']]

# Data structures
nX = len(outer_vals)
nY = len(inner_vals)
errors = sp.zeros((nX, nY))
structures = []

# Shelve the namespace
dump_globals(globals(), data_flag)


for idx, iX in enumerate(outer_vals):
	print ("%s = %s" %(outer_var, iX))
	for idy, iY in enumerate(inner_vals):
		for iT in range(iterations):
		
			# Gather swept variables in dictionary
			exec("params = dict(%s = %s, %s = %s, seed_dSs = %s)" 
					% (outer_var, iX, inner_var, iY, iT))
			
			# Add manually fixed variables
			if fixed_vars != None: 
				params = merge_two_dicts(fixed_vars, params)
			
			# Add relative variables
			if rel_vars != None:
				for iVar in rel_vars:
					tmp_str = string.replace(string.replace(iVar[1], 
												"%s" % outer_var, 'iX'), 
												"%s" % inner_var, 'iY')
					exec("sweep_vars_rel = dict(%s = %s)"% (iVar[0], tmp_str))
					params = merge_two_dicts(params, sweep_vars_rel)
			
			# Encode, decode, and quantify
			a = four_state_receptor_CS(**params)
			a.encode()
			a.decode()
			errors[idx, idy] += (sp.sum((a.dSs_est - a.dSs)**2.0)/a.Nn)/iterations	
		
			# Save object and its data to file
			structures.append(a)
			
	dump_structures(structures, data_flag)
	dump_errors(errors, data_flag)
	
# Quick plot	
iter_plots(inner_vals, errors.T, options = ['yscale("log")'], 
			ylabel = 'Error', xlabel = '%s' % inner_var)
