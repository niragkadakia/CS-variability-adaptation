"""
Scripts for plotting.

Created by Nirag Kadakia at 21:46 08-06-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import matplotlib.pyplot as plt
import scipy as sp

def single_plot(X, Y, xlabel = 'X', ylabel = 'Y', options = ['yscale("log")']):
	
	""" 
	Script to generate a single plot
	"""
	
	plt.plot(X, Y)
	
	for idx in options:
		exec("plt.%s" % idx)
		
	plt.xlabel('%s' % xlabel)
	plt.ylabel('%s' % ylabel)
	
	plt.show()


def iter_plots(X, Ys, xlabel = 'X', ylabel = 'Y', iter_label = None , options = []):
	
	""" 
	Script to plot an iteration of plots,
	along the last axis
	"""
	
	for idx in range(len(Ys[0,:])):
		plt.plot(X, Ys[:,idx])
		if iter_label != None:
			plt.ylabel("%s" % iter_label[idx])
	
	for idx in options:
		exec("plt.%s" % idx)
		
	plt.xlabel('%s' % xlabel)
	plt.ylabel('%s' % ylabel)
	
	plt.show()
