"""
Functions for generating plot formats for various types of plots.

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

					
DATA_DIR = def_data_dir()
VAR_STRINGS = dict(mu_Ss0 = '$\langle s_0 \\rangle$', 
					mu_dSs = '$\langle s \\rangle$',
					mu_eps = '$\epsilon$',
					sigma_Ss0 = '$s_0$',
					sigma_dSs = '$\Delta s$',
					sigma_eps = '$\langle \epsilon^\mu -' 
						'\langle \epsilon \\rangle \\rangle$',
					A0 = '$a_0$',
					sigma_A0 = '$\sigma_{a_0}$', 
					mu_A0 = '$\mu_{a_0}$')
					
def optimal_decoding_formatting(iter_plot_var, optimize_var):
	""" 
	Script to generate plots of optimally-decoded variable versus another
	variable.
	
	Args:
		iter_plot_var: The iterated variable which will form the x-axis.
		optimize_var: The variable over which the decoding error is optimized.
				
	Returns:
		fig: The figure object.
	"""
	
	fig = generic_plots()
	try:
		plt.xlabel(r'%s' % VAR_STRINGS[iter_plot_var], fontsize = 20)
		plt.ylabel(r'Optimal %s' % VAR_STRINGS[optimize_var], fontsize=20)
	except:
		print ('No formatted x or y-label in dictionary, using generic' \
				'labels instead')
		plt.xlabel(r'$x$')
		plt.xlabel(r'Optimal $y$')
	return fig	

def error_plots_formatting(x_axis_var):
	""" 
	Script to generate plots of errors versus inner loop variable, 
	for each outer variable.
	
	Args:
		x_axis_var: The inner loop variable, x-axis of each plot.
				
	Returns:
		fig: The figure object.
	"""
	
	fig = generic_plots()
	
	plt.yscale('log')
	plt.ylabel(r'MSE', fontsize = 20)
	try:
		plt.xlabel(r'%s' % VAR_STRINGS[x_axis_var], fontsize = 20)
	except:
		print ('No formatted x-label in dictionary, using generic x-axis ' \
					'label instead')
		plt.xlabel(r'$x$')
	
	return fig
	
def generic_plots():
	"""
	Generate generic plot format in reasonably pretty layout.
	
	Returns: 
		fig: The figure object.
	"""
	
	fig = plt.figure()
	fig.set_size_inches(3.5,3.5)
	ax = plt.subplot(111)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	
	return fig