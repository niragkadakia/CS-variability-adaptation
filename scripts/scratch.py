"""
Scratch script to test code before writing new scripts.

Created by Nirag Kadakia at 16:00 8-16-2017
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
from kinetics import A0_dist_norm_Kk, Kk_dist_norm_activity, bkgrnd_activity
from lin_alg_structs import random_matrix, sparse_vector
from four_state_receptor_CS import four_state_receptor_CS
from local_methods import def_data_dir

from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
import matplotlib.pyplot as plt


data_dir = def_data_dir()


def test_rowwise_matrix():
	"""
	Plot a K_d matrix that is composed of both narrow and broad tuning curves.
	That is, every row is chosen from a Gaussian with differing sigmas, same 
	mean.
	"""

	Nn = 100
	Mm = 10
	
	mean = 10.0
	sigma_spread = 4.0
	
	means = sp.ones(Mm)*mean
	
	# Choose sigmas from uniform prior distribution
	sigmas = sp.random.uniform(0, sigma_spread, size = Mm)

	a = random_matrix([Mm, Nn], [means, sigmas], type = "rank2_row_gaussian")

	for iRow in range(Mm):
		sp.random.shuffle(a[iRow, :])

	plt.imshow(a, cmap="hot")
	plt.show()


def monomolecular_normal_overall_act():
	"""
	Consider a matrix consisting of K_d chosen such that the activity to 
	monomolecular components is Gaussian. Then each entry will be chosen
	from a reciprocal normal. Q: What does the overall activity of any 
	particular receptor look like?
	"""
	
	Nn = 1
	Mm = 1500
	Kk = 1

	mu_A0 = 0.5
	sigma_A0 = 0.05
	Ss0 = 100
	eps = 3
	
	Kk_mean = 10
	
	Ss_params = [Ss0, 0]
	
	signal = sparse_vector([Nn, Kk], Ss_params)
	
	# Preserve normal activity 
	#Kk_rv = Kk_dist_norm_activity()
	#Kk_dict = dict(Ss0 = Ss0, eps = eps, mu_A0 = mu_A0, sigma_A0 = sigma_A0, size = [Mm, Nn])
	#Kk_matrix = Kk_rv.rvs(**Kk_dict)
	
	# Simple Gaussian 
	#Kk_matrix = random_matrix([Mm, Nn], [Kk_mean, 1])
	
	# Row-wise -- each neuron responds with a Gaussian tuning curves
	# whose variance is chosen from a uniform prior in 0, sigma_spread_Kk
	#sigma_spread_Kk = 0.1
	#means = sp.ones(Mm)*Kk_mean
	#sigmas = sp.random.uniform(0, sigma_spread_Kk, size = Mm)
	#Kk_matrix = random_matrix([Mm,Nn], [means, sigmas], type = "rank2_row_gaussian")
	
	# Make each receptor give a normal activity for single stimuli, 
	# but with different variances
	sp.random.seed(3)
	Kk_rv = Kk_dist_norm_activity()
	sigma_spread_A0 = 0.2
	#sigmas_A0 = sp.random.binomial(1, 0.5, size = Mm)*0.05 + 0.15
	#means_A0 = sp.random.binomial(1, 0.5, size = Mm)*0.25 + 0.5
	#sigmas_A0 = sp.ones(Mm)*0.02
	sigmas_A0 = sp.random.uniform(0.01, sigma_spread_A0, size = Mm)
	means_A0 = sp.ones(Mm)*0.5
	Kk_matrix = sp.zeros((Mm, Nn))
	for iM in range(Mm):
		Kk_dict = dict(Ss0 = Ss0, eps = eps, mu_A0 = means_A0[iM], sigma_A0 = sigmas_A0[iM], size = [Nn])
		Kk_matrix[iM, :] = Kk_rv.rvs(**Kk_dict)
		sp.random.shuffle(Kk_matrix[iM, :])
	
	#plt.imshow(Kk_matrix)
	#plt.colorbar()
	#plt.show()
	#plt.hist(Kk_matrix, bins = 20, normed = 1)
	#plt.show()
	
	activity = bkgrnd_activity(signal[0], Kk_matrix, Kk_matrix, eps)
	plt.hist(activity, bins = 100)
	plt.show()
	
	
monomolecular_normal_overall_act()
	
