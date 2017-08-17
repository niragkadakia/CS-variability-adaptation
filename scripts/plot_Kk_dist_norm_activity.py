"""
Script to plot the pdfs of the disassociation constant distributions 
which gives rise to a normally-distributed activity level.

Created by Nirag Kadakia at 12:30 8-15-2017
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
from kinetics import Kk_dist_norm_activity

from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx


data_dir = def_data_dir()

mu_A0 = 0.99
sigma_A0 = 0.0001
Ss0 = 200

# We will plot for various epsilons on a single plot
epsilons = sp.linspace(1,4,3) 
Xx = sp.arange(0,20,0.0001)

# Set color scheme
fig = plt.figure()
fig.set_size_inches(4,3)
cNorm  = colors.Normalize(vmin = 0, vmax = 1)
scalarMap = cmx.ScalarMappable(norm = cNorm, cmap = 'Reds')
color_vals = sp.arange(len(epsilons))*1./(len(epsilons) + 1) + 0.3

# Instantiate random variable class
K_dist = Kk_dist_norm_activity()

for idx, eps in enumerate(epsilons):
	args_dict = dict(Ss0 = Ss0, eps = eps, mu_A0 = mu_A0, sigma_A0 = sigma_A0)
	plt.plot(Xx, K_dist.pdf(Xx, **args_dict), 
				color = scalarMap.to_rgba(color_vals[idx]), 
				label = r'$\epsilon = %s$' % eps)

plt.xlabel(r'$x$', fontsize = 20)
plt.ylabel(r'$p(K_* = x)$', fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
#plt.ylim(0, 5)
plt.legend()
plt.tight_layout()
plt.savefig('%s/Kk_dist_norm_activity/pdf_Ss0=%s,mu=%s,sigma=%s.pdf' 
			% (data_dir, args_dict['Ss0'], args_dict['mu_A0'], args_dict['sigma_A0']))