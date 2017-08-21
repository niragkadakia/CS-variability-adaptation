"""
Plot estimation error of inferred signal in compressed sensing 
from error objects (.npz) generated by calculate_errors.py.

Created by Nirag Kadakia at 20:00 08-20-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from utils import get_flag
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from load_specs import read_specs_file
from save_data import save_figure
from load_data import load_errors
from plot_formats import error_plots_formatting


def plot_errors(data_flag, axes_to_plot = [0, 1]):
	"""
	Plot estimation error of inferred signal in compressed sensing 
	from error objects (.npz) generated by calculate_errors.py.	Requires
	a rank-2 array. 

	Args:
		data_flag: Identifier for saving and loading.
		axes_to_plot: List indicating which of the iterated variables are
			to be plotted; first one is the iterated variable; second one 
			will form the x-axis of the plot.
	"""
	
	data_flag = get_flag()
	
	list_dict = read_specs_file(data_flag)
	for key in list_dict:
		exec("%s = list_dict[key]" % key)
		
	assert len(iter_vars.keys()) == 2, 'Error: Plot ' \
				'axes must for rank-2 error array'
	iter_plot_var = iter_vars.keys()[axes_to_plot[0]]
	x_axis_var = iter_vars.keys()[axes_to_plot[1]]
	
	errors = load_errors(data_flag)
	if axes_to_plot[0] == 1:    # Switch axes if necessary
		errors = errors.T
	
	fig = error_plots_formatting(x_axis_var)
	for idx, val in enumerate(iter_vars[iter_plot_var]):
		plt.plot(iter_vars[x_axis_var], errors[idx,:], linewidth = 0.5)
	save_figure(fig, 'errors', data_flag)

	
if __name__ == '__main__':
	data_flag = get_flag()
	plot_errors(data_flag)
