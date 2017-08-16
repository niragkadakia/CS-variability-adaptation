"""
Script to calculate errors in two variables, one as a function of one another 
to minimize decoding errors in 4-state receptor model of compressed sensing. 
This script assumes a constant background adapted activity, which is set to 
a given value or distribution. The background free energies are derived 
from this given value. The activity is then generated and CS is used to 
decode around the background value.


Created by Nirag Kadakia at 22:30 08-14-2017
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
from plots import plot_var1_vs_opt_var2
import string


data_flag = get_flag()
check_existing_file(data_flag, prefix = 'structures_')
	
# Parameters to sweep and their respective ranges
iterations = 1
outer_var = "mu_Ss0"
inner_var = "mu1_eps"
outer_vals = 10.**sp.linspace(-2,0,10)
inner_vals = sp.linspace(0.2, .8, 50)

# Fixed parameters and values, and list of iteration-dependent parameters
# If no fixed parameters, set fixed_vars = None; iter_vars needs at least 1
fixed_vars =  None
iter_vars = ['seed_dSs', 'seed_Ss0', 'seed_Kk1', 'seed_Kk2', 'seed_eps']
 
# Relative parameter that depend on either of swept parameters
# For each entry iVar[,] in rel_vars, we enforce iVar[0] = iVar[1]
# If no relative parameters, set rel_vars = None
rel_vars = [['mu_dSs', 'mu_Ss0/2.']]

nX = len(outer_vals)
nY = len(inner_vals)
errors = sp.zeros((nX, nY))
params = dict()
structures = []

dump_globals(globals(), data_flag)

for idx, iX in enumerate(outer_vals):
	print ("%s = %s" %(outer_var, iX))
	for idy, iY in enumerate(inner_vals):
		for iT in range(iterations):
		
			# Gather swept and iterated variables in params dictionary
			params[outer_var] = iX
			params[inner_var] = iY
			for key in iter_vars:
				params[key] = iT
				
			# Add manually fixed variables
			if fixed_vars != None: 
				params = merge_two_dicts(fixed_vars, params)
			
			# Parse strings for relative variables
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
			errors[idx, idy] += (sp.sum((a.dSs_est - 
									a.dSs)**2.0)/a.Nn)/iterations	
		
			structures.append(a)
			
	dump_structures(structures, data_flag)
	dump_errors(errors, data_flag)
