"""
Script to plot the pdfs of the activity levels given
a normally-distributed Kk2 disassociation constant.

Created by Nirag Kadakia at 13:00 8-16-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')

from local_methods import def_data_dir
from kinetics import A0_dist_norm_Kk

from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


data_dir = def_data_dir()

mu_Kk2 = 5
sigma_Kk2 = 1.3
Ss0 = 60

# We will plot for various epsilons on a single plot
epsilons = sp.linspace(1,4,3) 
Xx = sp.arange(0.001,1.0,0.0001)

# Set color scheme
fig = plt.figure()
fig.set_size_inches(4,3)
cNorm  = colors.Normalize(vmin = 0, vmax = 1)
scalarMap = cmx.ScalarMappable(norm = cNorm, cmap = 'Reds')
color_vals = sp.arange(len(epsilons))*1./(len(epsilons) + 1) + 0.3

# Instantiate random variable class
A0_dist = A0_dist_norm_Kk()

for idx, eps in enumerate(epsilons):
	args_dict = dict(Ss0 = Ss0, eps = eps, mu_Kk2 = mu_Kk2, sigma_Kk2 = sigma_Kk2)
	plt.plot(Xx, A0_dist.pdf(Xx, **args_dict), 
				color = scalarMap.to_rgba(color_vals[idx]), 
				label = r'$\epsilon = %s$' % eps)

plt.xlabel(r'$x$', fontsize = 20)
plt.ylabel(r'$p(K_* = x)$', fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(0, 10)
plt.legend()
plt.tight_layout()
plt.savefig('%s/A0_dist_norm_Kk/pdf_Ss0=%s,mu=%s,sigma=%s.pdf' 
			% (data_dir, args_dict['Ss0'], args_dict['mu_Kk2'], args_dict['sigma_Kk2']))