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
	color=cm.Reds(sp.linspace(0,1,10))
	obj = single_encode_CS(vars_to_pass, run_specs)
	for iM in range(obj.Mm):
			sp.random.seed(iM)
			obj.Kk2[iM, :] = sp.random.normal(1e-2, 2e-3, obj.Nn)
			obj.Kk2[iM, :] = obj.Kk2[iM, :].clip(min = 1e-5)
			obj.Kk2[iM, :] = sp.sort(obj.Kk2[iM, :])
			tmp = sp.hstack((obj.Kk2[iM, :], obj.Kk2[iM, ::-1]))
			obj.Kk2[iM, :] = tmp[::2]
			obj.Kk2[iM, :] = sp.roll(obj.Kk2[iM, :], iM)
	import matplotlib.pyplot as plt
	plt.subplot(231)
	plt.imshow(sp.log(obj.Kk2)/sp.log(10))
	plt.colorbar()
	
	for idx, mu_dSs in enumerate(10.**sp.linspace(-2, 3, 10)):
		
		
		obj.dSs = sp.ones(obj.Nn)*0
		obj.Ss0 = sp.ones(obj.Nn)*.0001
		#obj.dSs[0] = mu_dSs
		width = 100
		eps_factor = 120.0
		obj.dSs = mu_dSs*sp.exp(-(sp.arange(obj.Mm)/(obj.Nn/width))**2.0)
		obj.Ss = obj.Ss0 + obj.dSs
		obj.set_random_free_energy()
		obj.eps += (sp.log(mu_dSs)-sp.log(1e-2))*sp.exp(-(sp.arange(obj.Mm)/(obj.Nn/width)/eps_factor)**2.0)
		obj.set_measured_activity()
		obj.set_linearized_response()

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
	
	plt.show()
	
	#dump_objects(obj, iter_vars, iter_var_idxs, data_flag)

	
if __name__ == '__main__':
	data_flag = get_flag()
	iter_var_idxs = map(int, sys.argv[2:])
	plot_tuning_curves(data_flag, iter_var_idxs)