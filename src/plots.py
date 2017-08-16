"""
Scripts for plotting.

Created by Nirag Kadakia at 21:46 08-06-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
from local_methods import def_data_dir
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
import matplotlib.pyplot as plt

					
data_dir = def_data_dir()

var_names = dict(mu_Ss0 = '$\langle s_0 \\rangle$', 
					mu_dSs = '$\langle s \\rangle$',
					mu1_eps = '$\epsilon$',
					sigma_Ss0 = '$s_0$',
					sigma_dSs = '$\Delta s$',
					sigma1_eps = '$\langle \epsilon^\mu -' 
						'\langle \epsilon \\rangle \\rangle$',
					A0 = '$a_0$',
					sigma_A0 = '$\sigma_{a_0}$', 
					mu_A0 = '$\mu_{a_0}$')
					
def plot_var1_vs_opt_var2(**kwargs):
	""" 
	Script to generate plots of single outer loop
	variable versus optimized inner loop variable.
	"""

	for key in kwargs:
		exec("%s = kwargs[key]" % key)
		
	fig = plt.figure()
	fig.set_size_inches(3.5,3.5)
	plt.plot(outer_vals, opt_inner_vals, color = 'darkslategray')
	
	plt.xlabel(r'%s' % var_names[outer_var], fontsize = 20)
	plt.ylabel(r'Optimal %s' % var_names[inner_var], fontsize=20)
	plt.xticks(fontsize=14)
	plt.yticks(fontsize=14)
	plt.xscale('log')
	
	return fig	

def plot_errors(**kwargs):
	""" 
	Script to generate plots of errors versus inner
	loop variable, for each outer variable
	"""
	
	for key in kwargs:
		exec("%s = kwargs[key]" % key)
	
	fig = plt.figure()
	fig.set_size_inches(3.5,3.5)
	ax = plt.subplot(111)
	#ax.set_prop_cycle('color', sns.color_palette("coolwarm_r",nX))
	
	for idx in range(nX):
		plt.plot(inner_vals, errors[idx,:], linewidth = 0.5)
	
	plt.yscale('log')
	plt.xlabel(r'%s' % var_names[inner_var], fontsize = 20)
	plt.ylabel(r'MSE', fontsize = 20)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	
	return fig
	