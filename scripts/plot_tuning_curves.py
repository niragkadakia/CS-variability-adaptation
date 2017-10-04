"""
Plot tuning curves, using given stimulus file.

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
	
	runs = 3
	
	from matplotlib.pyplot import cm 
	import matplotlib.pyplot as plt
	color=cm.Reds(sp.linspace(.2,1,runs))
	
	
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)
	
	
	epsilons = sp.zeros((runs, params['Mm']))
	responses = sp.zeros((params['Mm'], params['Nn']))
	errors = sp.zeros(runs)
	for idx in range(runs):
	
		iter_var_idxs = [idx, 1]
		vars_to_pass = dict()
		vars_to_pass = parse_iterated_vars(iter_vars, iter_var_idxs, vars_to_pass)
		vars_to_pass = parse_relative_vars(rel_vars, iter_vars, vars_to_pass)
		vars_to_pass = merge_two_dicts(vars_to_pass, fixed_vars)
		vars_to_pass = merge_two_dicts(vars_to_pass, params)
	
		for iN in range(params['Nn']):
			vars_to_pass['manual_dSs'] = sp.array([iN])
			obj = single_encode_CS(vars_to_pass, run_specs)
			#obj.decode()
			obj.dSs_est = sp.zeros(obj.Nn)
			errors[idx] += sp.average(sp.sum((obj.dSs_est - obj.dSs)**2.0/obj.Nn))/obj.Nn
			#if iN == 25:
		#		plt.subplot(232)
		#		plt.plot(range(obj.Nn), obj.dSs)
		#		plt.plot(range(obj.Nn), obj.dSs_est, color=color[idx])
			responses[:, iN] = obj.dYy
			
		epsilons[idx, :] = obj.eps
		
		c1=cm.Reds(sp.linspace(0.2, 1,obj.Mm))
		c2=cm.Greens(sp.linspace(0.2, 1,obj.Mm))
		c3=cm.Blues(sp.linspace(0.2, 1,obj.Mm))
		colormaps = [c1, c2, c3]
		
		plt.subplot(2, 3, 2+idx)
		plt.ylim(0, 1)
		for iM in range(obj.Mm):
			responses[iM, :] = sp.sort(responses[iM, :])
		responses = responses[responses[:,-1].argsort()]
		responses = sp.flipud(responses)
		for iM in range(obj.Mm):
			if iM % 5 == 0:
				plt.plot(sp.arange(obj.Nn), responses[iM,:], color=colormaps[idx][iM], linewidth=1)
				plt.plot(sp.arange(obj.Nn, obj.Nn*2), responses[iM,::-1], color=colormaps[idx][iM], linewidth=1)
		
		plt.subplot(235)
		plt.plot(range(obj.Mm), obj.eps, color=color[idx])
	
	plt.subplot(236)
	plt.imshow(sp.log(obj.Kk2)/sp.log(10), aspect=obj.Nn/obj.Mm)
	plt.colorbar()

	plt.subplot(231)
	plt.imshow(epsilons, aspect=obj.Mm/runs)
	
		
	plt.show()
	
	#dump_objects(obj, iter_vars, iter_var_idxs, data_flag)

	
if __name__ == '__main__':
	data_flag = get_flag()
	iter_var_idxs = map(int, sys.argv[2:])
	plot_tuning_curves(data_flag, iter_var_idxs)