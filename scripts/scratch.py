"""
Testing scripts

Created by Nirag Kadakia at 17:00 08-27-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import sys
sys.path.append('../src')
from utils import get_flag
from load_specs import read_specs_file
from load_data import load_aggregated_object_list
import matplotlib.pyplot as plt
from kinetics import Kk2_eval_normal_activity
	

def scratch(data_flag, axes_to_plot=[0, 1], fixed_axes=dict()):
	
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)

	iter_vars_dims = []
	for iter_var in iter_vars:
		iter_vars_dims.append(len(iter_vars[iter_var]))		
	it = sp.nditer(sp.zeros(iter_vars_dims), flags = ['multi_index'])	

	print ('Loading object list...')
	CS_object_array = load_aggregated_object_list(iter_vars_dims, data_flag)
	print ('...loaded.')

	errors = load_errors(data_flag)
	# Can only handle 2D for now.
	#assert (len(errors.shape) == 2), "Need a rank-2 error array"
	
	# Manually handle for rank-3 array
	errors = errors[0, :,  :]
	CS_object_array = CS_object_array[0, :, :]
	
	
	for idx in range(len(errors[:,0])):
		opt_idx = sp.argmin(errors[idx,:])
		bad_idx = sp.argmax(errors[idx,:])
		bkgrnd = CS_object_array[idx, opt_idx].Ss0
		#plt.plot(CS_object_array[idx, opt_idx].Yy, color='orange')
		#plt.plot(CS_object_array[idx, bad_idx].Yy, color='orange', linestyle = '--')
		#plt.plot(CS_object_array[idx, opt_idx].dYy, color='black')
		#plt.plot(CS_object_array[idx, bad_idx].dYy, color='black', linestyle = '--')
		plt.plot(CS_object_array[idx, bad_idx].dSs + bkgrnd, color='black')
		plt.plot(CS_object_array[idx, opt_idx].dSs_est + bkgrnd, color='red')
		plt.plot(CS_object_array[idx, opt_idx].dSs_est + bkgrnd, color='red', linestyle = '--')
		plt.title(idx)
		plt.show()

def plot_inverse_distr():
	
	Mm = 1
	Nn = 2000
	
	
	eps = sp.ones(Mm)*5.211
	s0 = sp.ones(Mm)*3.359
	C = sp.exp(-eps)*s0

	mus = sp.ones(Mm)*0.5
	sigmas = sp.ones(Mm)*0.1
	shape = sp.array([Mm, Nn])
	Kk2 = Kk2_eval_normal_activity(shape, mus, sigmas, s0, eps, 0)
	for iM in range(Mm):
		plt.hist(Kk2[iM, :], bins = 100, normed=True)
	
	
	normal = sp.random.normal(0.018, 0.005, Nn)
	plt.hist(normal, bins=30, normed=True)
	
	plt.show()
	
	
if __name__ == '__main__':
	data_flag = get_flag()
	#scratch(data_flag, axes_to_plot=[1,2], fixed_axes=dict(mu_Ss0=0))
	plot_inverse_distr()