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
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
import matplotlib.pyplot as plt


def single_plot(X, Y, xlabel = 'X', ylabel = 'Y', options = [], no_show = False):
	
	""" 
	Script to generate a single plot
	"""
	
	plt.plot(X, Y)
	
	plt.xlabel(r'%s' % xlabel)
	plt.ylabel(r'%s' % ylabel)
	plt.tight_layout()
	
	for idx in options:
		exec(idx)
	
	
	if no_show == False:
		plt.show()
		


def iter_plots(X, Ys, xlabel = 'X', ylabel = 'Y', iter_label = None , options = [], no_show = False):
	
	""" 
	Script to plot an iteration of plots,
	along the last axis
	"""
	
	for idx in range(len(Ys[0,:])):
		plt.plot(X, Ys[:,idx])
		if iter_label != None:
			plt.ylabel("%s" % iter_label[idx])
	
	plt.xlabel('%s' % xlabel)
	plt.ylabel('%s' % ylabel)

	for idx in options:
		exec("plt.%s" % idx)
			
	if no_show == False:
		plt.show()
