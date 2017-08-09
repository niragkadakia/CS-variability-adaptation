"""
Script to calculate errors in two variables, one as a function of one another 
to minimize decoding errors in 4-state receptor model of compressed 
sensing.

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
import os
sys.path.append('../src')
from four_state_receptor_CS import *
from plots import *
import shelve
import gzip
import cPickle
import string


# Data saving
try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")

data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation"

if os.path.isfile("%s/structures_%s.pklz" % (data_dir, data_flag)) == True:
	overwrite = None
	while overwrite != ('n' or 'y'):
		overwrite = raw_input('Overwrite, y or n? ')
		if overwrite == 'y':
			break
		elif overwrite == 'n':
			print ('Specify different data flag')
			exit()
	

# Parameters to sweep and their respective ranges
outer_var = "mu_Ss0"
inner_var = "mu_eps"
outer_vals = 10.**sp.linspace(-1, 0, 10)
inner_vals = sp.linspace(0, 20, 150)

# Parameters to hold fixed
fixed_vars = None

# Relative paramaters versus swept parameters
rel_vars = [['sigma_Ss0', 'mu_Ss0/50.'],['mu_dSs', 'mu_Ss0/3.'],['sigma_dSs', 'mu_Ss0/6.'],['sigma_eps', 'mu_eps/5.']]

# Stimuli statistics
iterations = 5

# Saving options 0--save both loops; 1--save outer loop only
pickle_capacity = 0

# Data structures
nX, nY = len(outer_vals), len(inner_vals)
errors = sp.zeros((nX, nY))
structs = []

# Shelve the globals, ignore modules, etc.
f = '%s/globals_%s.out' % (data_dir, data_flag)
vars_file = shelve.open(f, 'n') 
for key in dir():
	try:
		vars_file[key] = globals()[key]
	except:
		pass
vars_file.close()


for idx, iX in enumerate(outer_vals):		
	print ("%s = %s" %(outer_var, iX))
	
	for idy, iY in enumerate(inner_vals): 	
		
		for iT in range(iterations):
			
			# Gather swept variables in dictionary
			exec("params = dict(%s = %s, %s = %s, seed_dSs = %s, seed_eps = %s)" 
				% (outer_var, iX, inner_var, iY, iT, iT))
			
			# Add manually fixed variables
			if fixed_vars != None: 
				params = merge_two_dicts(fixed_vars, params)
			
			# Add relative variables
			if rel_vars != None:
				for iVar in rel_vars:
					tmp_str = string.replace(string.replace(iVar[1], "%s" % outer_var, 'iX'), "%s" % inner_var, 'iY')
					exec("sweep_vars_rel = dict(%s = %s)"% (iVar[0], tmp_str))
					params = merge_two_dicts(params, sweep_vars_rel)
			
			# Encode, decode, and quantify
			a = four_state_receptor_CS(**params)
			a.encode()
			a.decode()
			errors[idx, idy] += (sp.sum((a.dSs_est - a.dSs)**2.0)/a.Nn)/iterations
		
		# Only keep one dataset per iteration set -- statistics data not needed
		if pickle_capacity == 0:
			structs.append(a)
	
	if pickle_capacity == 1:
		structs.append(a)
	
	# Pickle the full data and save errors periodically
	f = gzip.open('%s/structures_%s.pklz' % (data_dir, data_flag), 'wb')
	cPickle.dump(structs, f, protocol=2)
	f.close()
	sp.savetxt('%s/errors_%s.dat' % (data_dir, data_flag), errors, fmt = "%.5e", delimiter = "\t")	

# Quick plot	
iter_plots(inner_vals, errors.T, options = ['yscale("log")'], 
			ylabel = 'Error', xlabel = '%s' % inner_var)
