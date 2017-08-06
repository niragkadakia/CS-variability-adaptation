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
import matplotlib.pyplot as plt
from four_state_receptor_CS import *
import shelve
import gzip
import cPickle


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
	
# Saving options 0--save both loops; 1--save outer loop only
pickle_capacity = 0

# Variables to sweep and ranges
outer_var = "muSs_0"
inner_var = "epsilon"
outer_vals = 10.**(sp.linspace(-1, 1, 5))
inner_vals = sp.linspace(0, 20, 30)

# Parameters to hold fixed
fixed_vars = dict(sigmaSs_0 = 0.01, muSs = .1, sigmaSs = 0.05, Kk = 5, Mm = 20, Nn = 50)

# Stimuli statistics
iterations = 1

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
			
			# Gather all the variables to pass
			exec("sweep_vars = dict(%s = %s, %s = %s, seedSs = %s)" 
				% (outer_var, iX, inner_var, iY, iT))
			params = merge_two_dicts(fixed_vars, sweep_vars)
			
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
for idx, iX in enumerate(outer_vals):
	plt.plot(inner_vals, errors[idx,:])
plt.yscale('log')
plt.show()


