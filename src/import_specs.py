"""
Module to gather information from specifications file about how a particular 
run is to be performed for the CS decoding scheme. 


Created by Nirag Kadakia at 9:30 08-17-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
from local_methods import def_data_dir
import os


data_dir = def_data_dir()

def read_specs_file(data_flag, data_dir = data_dir):
	filename = '%s/specs/%s.txt' % (data_dir, data_flag)
	
	try:
		os.stat(filename)
	except:
		print ("There is no input file %s/specs/%s.txt" 
				% (data_dir, data_flag))
		exit()
	
	fixed_vars = dict()
	iter_vars = dict()
	rel_vars = dict()
	params = dict()
	
	specs_file = open(filename, 'r')

	print ('Reading input file...')
	for line in specs_file:
		if line.strip():
			if not line.startswith("#"):
				
				keys = line.split()
				var_type = keys[0]
				var_name = keys[1]
				
				if var_type == 'iter_var':
					scaling = float(keys[2]):
					lo = float(keys[3])
					hi = float(keys[4])
					dl = float(keys[5])
					if scaling == 'lin':
						iter_vars.update({var_name:sp.arange(lo, hi, dl)})
					elif scaling == 'exp':
						base = keys[6]
						iter_vars.update({var_name: base**sp.arange(lo, hi, dl)})
				elif var_type == 'fixed_var':
					fixed_vars.update({var_name: keys[2]})
				elif var_type == 'rel_var':
					rel_vars.update({var_name: keys[2]})
				elif var_type == 'param':
					params.update({var_name: keys[2]})
				
	specs_file.close()
	print ('...Input parameters loaded')
	
	return [iter_vars, fixed_vars, rel_vars, params]
