"""
Functions for loading data to plot and analyze data.

Created by Nirag Kadakia at 23:30 08-02-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import cPickle
import shelve
import gzip
import os
from collections import OrderedDict
from local_methods import def_data_dir


data_dir = def_data_dir()
					
def check_existing_file(data_flag, data_dir = data_dir, 
						prefix = 'structures_', **kwargs):
	"""
	Check if file exists by data flag; prompt to overwrite.
	
	Args: 
		data_flag: Name of saved structures file.
		data_dir: Data folder, if different than in local_methods.	
		prefix: Prefix name for structures file; extension is pklz.	
	"""

	if os.path.isfile("%s/%s%s.pklz" % (data_dir, prefix, data_flag)) == True:
		overwrite = None
		while overwrite != ('n' or 'y'):
			overwrite = raw_input('Overwrite, y or n? ')
			if overwrite == 'y':
				break
			elif overwrite == 'n':
				print ('Specify different data flag')
				exit()	

def load_errors(data_flag, data_dir = data_dir, **kwargs):
	"""
	Load error data from compressed sensing encoding/decoding module.
	
	Args: 
		data_flag: Name of shelved file of globals (.out).
		load_structures: Boolean flag for whether to load just the shelved
							globals, or the full saved objects as well.
		data_dir: Data folder, if different than in local_methods.	
	
	Returns:
		errors: numpy array of errors loaded from file.
	"""

	errors = sp.loadtxt('%s/errors_%s.dat' %(data_dir, data_flag))
	return errors

def load_structures_globals(data_flag, load_structures = True, 
					data_dir = data_dir, **kwargs):
	"""
	Load globals and class objects from compressed sensing encoding/decoding.

	Args: 
		data_flag: Name of shelved file of globals (.out).
		load_structures: Boolean flag for whether to load just the shelved
							globals, or the full saved objects as well.
		data_dir: Data folder, if different than in local_methods.	
	
	Returns:
		vars_dict: The dictionary of variables from the globals file.
		structures: The full CS objects for each run.
	"""

	f = '%s/globals_%s.out' % (data_dir, data_flag)
	shelf_file = shelve.open(f,'r')
	vars_dict = dict()
	for key in shelf_file:
		try:
			vars_dict[key] = shelf_file[key]
		except:
			continue
	
	if load_structures == False:
		return vars_dict
	else:
		f = gzip.open('%s/structures_%s.pklz' % (data_dir, data_flag), 'rb')
		structures = sp.asarray(cPickle.load(f))
		f.close()
		nX, nY = vars_dict["nX"], vars_dict["nY"]
		structures  = structures.reshape((nX, nY))

		return vars_dict, structures
		
def load_explicit_vars(data_flag, vars_to_load, data_dir = data_dir, 
						**kwargs):
	"""
	Load an explicitly defined set of variables from externally shelved 
	file of variables into a dictionary.
	
	Args: 
		data_flag: Name of shelved file of globals (.out).
		vars_to_load: List of variable names as strings to load into 
						the dictionary.
		data_dir: Data folder, if different than in local_methods.
	
	Returns:
		out_dict: Dictionary of keyed items and their respective values.
	"""
	
	vars_dict = load_structures_globals(data_flag, load_structures = False)
	out_dict = dict()
	for idx in vars_to_load:
		out_dict[idx] = vars_dict[idx]

	return out_dict
	

def read_specs_file(data_flag, data_dir = data_dir):
	""" 
	Function to read a specifications file.
	
	Module to gather information from specifications file about how a 
	particular 	run is to be performed for the CS decoding scheme. 
	Specs file should have format .txt and the format is as listed here:

	iter_var     sigmaSs     lin     1     10      100
	fixed_var    slkd        2
	param        nX          3
	rel_var      sigmaSs     5

	It accepts these 4 types of inputs, labeled by the first column: iterated 
	variables, fixed variables, parameters to override, and relative variables.
	For iter_var, the possible types of scaling (3rd column) are lin or exp, 
	whether the range is the direct range or 10** the range. For relative 
	variables, the 3rd column simply gives a string stating the functional 
	dependency upon an independent variable. iter_vars are also put in an 
	ordered dictionary, the keys appearing in the order listed in the specs
	file.
	
	Args: 
		data_flag: Name of specifications file.
		data_dir: Data folder, if different than in local_methods.
	
	Returns:
		list_dict: Dictionary of 4 items keyed by 'rel_vars', 
					'fixed_vars', 'params', and 'iter_vars'.	

	TODO: 
		Add variables (e.g. seeds) to be averaged over (statistics)
	"""

	filename = '%s/specs/%s.txt' % (data_dir, data_flag)	
	try:
		os.stat(filename)
	except:
		print ("There is no input file %s/specs/%s.txt" 
				% (data_dir, data_flag))
		exit()
	specs_file = open(filename, 'r')

	fixed_vars = dict()
	iter_vars = OrderedDict()
	rel_vars = dict()
	params = dict()
	
	for line in specs_file:
		if line.strip():
			if not line.startswith("#"):
				
				keys = line.split()
				var_type = keys[0]
				var_name = keys[1]
					
				if var_type == 'iter_var':
					scaling = str(keys[2])
					lo = float(keys[3])
					hi = float(keys[4])
					Nn = float(keys[5])
					if scaling == 'lin':
						iter_vars[var_name] = sp.linspace(lo, hi, Nn)
					elif scaling == 'exp':
						base = float(keys[6])
						iter_vars[var_name] = base**sp.linspace(lo, hi, Nn)
				elif var_type == 'fixed_var':
					fixed_vars[var_name] = float(keys[2])
				elif var_type == 'rel_var':
					rel_vars[var_name] = keys[2]
				elif var_type == 'param':
					params[var_name] = float(keys[2])
				else:
					print ('nothing')
					
	specs_file.close()
	print ('\n -- Input vars and params loaded from %s.txt\n' % data_flag)
	
	list_dict =  dict()
	for i in ('rel_vars', 'fixed_vars', 'params', 'iter_vars'):
		list_dict[i] = locals()[i]
	
	return list_dict
