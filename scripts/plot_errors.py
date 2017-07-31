"""
Script to plot error vectors from the compressed sensing schemes

Created by Nirag Kadakia at 17:30 07-31-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import matplotlib.pyplot as plt
import sys

subdir = sys.argv[1]

data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation/%s" % subdir

errors = sp.loadtxt('%s/errors.dat' %data_dir)
misses = sp.loadtxt('%s/misses.dat' %data_dir)


plt.plot(errors[:,0],errors[:,1],label='traditional CS')
plt.plot(errors[:,0],errors[:,2],label='receptors')
plt.xlabel(r'$\mu_-$')
plt.ylabel(r'$|\hat s - s|^2$')
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.savefig('%s/errors.png' % data_dir)
plt.show()

plt.plot(misses[:,0],misses[:,1],label='traditional CS')
plt.plot(misses[:,0],misses[:,2],label='receptors')
plt.xlabel(r'$\mu_-$')
plt.ylabel(r'Number of error components (averaged)')
plt.xscale('log')
plt.legend()
plt.savefig('%s/misses.png' % data_dir)
plt.show()