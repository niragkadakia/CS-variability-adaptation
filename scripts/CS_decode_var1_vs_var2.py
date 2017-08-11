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
from utils import merge_two_dicts, get_flag
from load_data import check_existing_file
from save_data import dump_globals, dump_errors, dump_structures
import string


data_flag = get_flag()
check_existing_file(data_flag, prefix = 'structures_')
	
# Parameters to sweep and their respective ranges
iterations = 1
outer_var = "mu_Ss0"
inner_var = "mu1_eps"
outer_vals = 10.**sp.linspace(-2, 1, 5) 
inner_vals = sp.linspace(0, 20, 5) 

# Fixed and relative parameters throughout run
fixed_vars =  dict(sigma1_eps = 0., sigma_Ss0=1e-2, sigma_dSs = 1e-3)
rel_vars = [['mu_dSs', 'mu_Ss0/1.0']]
#rel_vars = [['mu1_eps', '2*sp.log(mu_Ss0)'], ['sigma_dSs', 'mu_dSs/5.']]

nX = len(outer_vals)
nY = len(inner_vals)
errors = sp.zeros((nX, nY))
structures = []

dump_globals(globals(), data_flag)
params = dict()

for idx, iX in enumerate(outer_vals):
	print ("%s = %s" %(outer_var, iX))
	for idy, iY in enumerate(inner_vals):
		for iT in range(iterations):
		
			# Gather swept variables in dictionary
			params[outer_var] = iX
			params[inner_var] = iY
			params['seed_dSs'] = iT
			
			# Add manually fixed variables
			if fixed_vars != None: 
				params = merge_two_dicts(fixed_vars, params)
			
			# Add relative variables
			if rel_vars != None:
				for iVar in rel_vars:
					tmp_str = string.replace(string.replace(iVar[1], 
												"%s" % outer_var, 'iX'), 
												"%s" % inner_var, 'iY')
					params[iVar[0]] = eval(tmp_str)
					
			# Encode, decode, and quantify
			a = four_state_receptor_CS(**params)
			a.encode()
			a.decode()
			errors[idx, idy] += (sp.sum((a.dSs_est - a.dSs)**2.0)/a.Nn)/iterations	
		
			# Save object and its data to file
			structures.append(a)
			
	dump_structures(structures, data_flag)
	dump_errors(errors, data_flag)
