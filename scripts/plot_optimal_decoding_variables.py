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
from utils import get_flag
from load_specs import read_specs_file
from save_data import save_figure
from load_data import load_errors
from plot_formats import optimal_decoding_formatting


def plot_optimal_decoding_variables(data_flag,  axes_to_plot=[0, 1], fixed_axes=dict()):
	"""
	Plot optimally decoded variables versus one another.
	
	Args:
		data_flag: Identifier for saving and loading.
		axes_to_plot: List indicating which of the iterated variables are
			to be plotted; first one is the iterated variable which will
			form the x-axis of the plot; the second variable is that over
			which the decoding error is minimized.
	"""
	
	data_flag = get_flag()
	
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)
		
	iter_plot_var = iter_vars.keys()[axes_to_plot[0]]
	optimize_var = iter_vars.keys()[axes_to_plot[1]]
	
	errors = load_errors(data_flag)
	
	#TODO Put this in a methods
	for idx, name in enumerate(iter_vars.keys()):
		if idx == axes_to_plot[0]:
			iter_plot_var = iter_vars.keys()[idx]
		elif idx == axes_to_plot[1]:
			x_axis_var = iter_vars.keys()[idx]
		else:
			proj_axis = iter_vars.keys().index(name)
			
			try:
				print ('Setting %s fixed..' % name)
				proj_element = fixed_axes[name]
			except:
				print ('Need to specify iterated variable values that ' \
						'are not being plotted in fixed_axes dictionary')
				quit()
			
			assert (proj_element < len(iter_vars[name])), \
					'Fixed index out of range, %s >= %s'\
					% (proj_element, len(iter_vars[name]))
			proj_vec = sp.zeros(len(iter_vars[name]))
			proj_vec[proj_element] = 1.0
			
			errors = sp.tensordot(errors, proj_vec, [proj_axis, 0])
	
	if axes_to_plot[0] == 1:    # Switch axes if necessary
		errors = errors.T
		
	optimal_values = []
	for idx, val in enumerate(iter_vars[iter_plot_var]):
		optimal_values.append(iter_vars[optimize_var] \
								[sp.argmin(errors[idx, :])])

	fig = optimal_decoding_formatting(iter_plot_var, optimize_var)
	plt.plot(iter_vars[iter_plot_var], optimal_values, color = 'darkslategray')
	plt.xscale('log')
	save_figure(fig, 'optimal_decoding_%s' % axes_to_plot, data_flag)

	
if __name__ == '__main__':
	data_flag = get_flag()
	plot_optimal_decoding_variables(data_flag, axes_to_plot=[0,1], fixed_axes=dict(mu_eps=50))
