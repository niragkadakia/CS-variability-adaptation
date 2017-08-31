"""
Plot variable for which the decoding error is optimized (minimum), 
as a function of another variable.

Created by Nirag Kadakia at 23:50 08-20-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import get_flag, project_tensor
from load_specs import read_specs_file
from save_data import save_figure
from load_data import load_errors
from plot_formats import optimal_decoding_formatting


def plot_optimal_decoding_variables(data_flag,  axes_to_plot=[0, 1], 
									projected_variable_components=dict()):
	"""
	Plot optimally decoded variables versus one another.
	
	Args:
		data_flag: Identifier for saving and loading.
		axes_to_plot: List indicating which of the iterated variables are
			to be plotted; first one is the iterated variable which will
			form the x-axis of the plot; the second variable is that over
			which the decoding error is minimized.
		projected_variable_components: dictionary; keys indicated the name
			of variable to be projected down, value is the component along 
			which it is projected.
	"""
	
	data_flag = get_flag()
	
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)
		
	iter_plot_var = iter_vars.keys()[axes_to_plot[0]]
	optimize_var = iter_vars.keys()[axes_to_plot[1]]
	
	errors = load_errors(data_flag)
	nAxes = len(errors.shape)
	if nAxes > 2:
		errors = project_tensor(errors, iter_vars, 
								projected_variable_components, axes_to_plot)
	
	#Switch axes if necessary
	if axes_to_plot[0] > axes_to_plot[1]:    
		errors = errors.T
			
	optimal_values = []
	for idx, val in enumerate(iter_vars[iter_plot_var]):
		optimal_values.append(iter_vars[optimize_var] \
								[sp.argmin(errors[idx, :])])

	fig = optimal_decoding_formatting(iter_plot_var, optimize_var)
	plt.plot(iter_vars[iter_plot_var], optimal_values, color = 'darkslategray')
	plt.xscale('log')
	plt.yscale('log')
	if nAxes < 3:
		save_figure(fig, 'optimal_decoding_%s' % axes_to_plot, data_flag)
	else:
		tmp_str = ''
		for key, value in projected_variable_components.items():
			tmp_str += '%s=%s' % (key, value)
		save_figure(fig, 'optimal_decoding_%s[%s]' % (axes_to_plot, tmp_str), data_flag)
	

	
if __name__ == '__main__':
	data_flag = get_flag()
	plot_optimal_decoding_variables(data_flag, axes_to_plot=[0, 1], 
						projected_variable_components=dict(mu_Ss0=4))
