"""
Plot tuning curves.

Created by Nirag Kadakia at 09:30 10-03-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
import os
sys.path.append('../src')
from utils import merge_two_dicts, get_flag
from load_specs import read_specs_file, parse_iterated_vars, \
						parse_relative_vars
from encode_CS import single_encode_CS
						
def plot_tuning_curves(data_flag=None, iter_var_idxs=None):
	"""
	Plot the tuning curve for given specifications.
	"""
	
	# Get the five dictionaries of variables and run specs; pass to locals()
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)
	
	vars_to_pass = dict()
	vars_to_pass = parse_iterated_vars(iter_vars, iter_var_idxs, vars_to_pass)
	vars_to_pass = parse_relative_vars(rel_vars, iter_vars, vars_to_pass)
	vars_to_pass = merge_two_dicts(vars_to_pass, fixed_vars)
	vars_to_pass = merge_two_dicts(vars_to_pass, params)
	

	from matplotlib.pyplot import cm 
	import matplotlib.pyplot as plt
	color=cm.Reds(sp.linspace(0,1,10))
	
	for idx, mu_dSs in enumerate(10.**sp.linspace(-2, 2, 10)):
		
		vars_to_pass['mu_dSs'] = mu_dSs
		vars_to_pass['normal_eps_tuning_width_factor'] = 65.#.2
		vars_to_pass['normal_eps_tuning_prefactor'] = sp.log(mu_dSs) - sp.log(1e-2)
		obj = single_encode_CS(vars_to_pass, run_specs)
		
		if idx == 0:
			plt.subplot(231)
			plt.imshow(sp.log(obj.Kk2)/sp.log(10))
			plt.colorbar()
	
		plt.subplot(232)
		plt.ylim(0, 1)
		plt.plot(range(obj.Mm), sp.sort(obj.dYy), color=color[idx])
		plt.plot(range(obj.Mm, obj.Mm*2), sp.sort(obj.dYy)[::-1], color=color[idx])
		
		plt.subplot(233)
		plt.ylim(0, 1)
		plt.plot(range(obj.Mm), sp.sort(obj.Yy), color=color[idx])
		plt.plot(range(obj.Mm, obj.Mm*2), sp.sort(obj.Yy)[::-1], color=color[idx])
		
		
		plt.subplot(234)
		plt.plot(range(obj.Mm), obj.Ss, color=color[idx])
	
		plt.subplot(235)
		plt.plot(range(obj.Mm), obj.eps, color=color[idx])
	
		plt.subplot(236)
		plt.yscale('log')
		plt.plot(range(obj.Mm), obj.dSs*sp.exp(-obj.eps), color=color[idx])
	
	plt.show()
	
	#dump_objects(obj, iter_vars, iter_var_idxs, data_flag)

	
if __name__ == '__main__':
	data_flag = get_flag()
	iter_var_idxs = map(int, sys.argv[2:])
	plot_tuning_curves(data_flag, iter_var_idxs)