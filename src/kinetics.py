"""
Function definitions for receptor-state activity, response, 
and gain in CS decoding scheme for olfaction.

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
from stats import Kk_dist_Gaussian_activity
import warnings
import sys


def bkgrnd_activity(Ss0, Kk1, Kk2, eps):
	"""
	Set background activity
	"""
	
	Kk2_sum = sp.dot(Kk2**-1., Ss0)
	A0 = Kk2_sum / (Kk2_sum + sp.exp(eps))
	
	return A0
	
def linear_gain(Ss0, Kk1, Kk2, eps):
	"""
	Set linearized binding and activation gain
	"""
	
	num = ((Kk2.T**-1.)*sp.exp(eps)).T
	Kk2_sum = sp.dot(Kk2**-1., Ss0)
	den = (sp.exp(eps) + Kk2_sum)**2.0
	dAadSs0 = (num.T/den).T
	
	return dAadSs0
	

def receptor_activity(Ss, Kk1, Kk2, eps):
	"""
	Steady state activity with binding and activation 
	Kk2 is the activated disassociation constants (K2)
	Kk1 is the inactivated disassociation constants (K1)
	K1 = Kk1 >> Ss+Ss0 >> Kk2 = K2
	"""
	
	Kk1_sum = sp.dot(Kk1**-1.0, Ss)
	Kk2_sum = sp.dot(Kk2**-1.0, Ss)
	Aa = (1. + sp.exp(eps)*(1 + Kk1_sum)/(1 + Kk2_sum))**-1.0
	
	return Aa

def free_energy(Ss, Kk1, Kk2, A0):
	"""
	Adapted steady state free energy for given 
	stimulus level, disassociation constants, and 
	adapted steady state activity level
	"""
	
	Kk1_sum = sp.dot(Kk1**-1.0, Ss)
	Kk2_sum = sp.dot(Kk2**-1.0, Ss)
	epsilon = sp.log((1.-A0)/A0*(1. + Kk2_sum)/(1. + Kk1_sum))
	
	return epsilon
		
def Kk2_samples(shape, receptor_activity_mus, receptor_activity_sigmas, 
				Ss0, eps, seed):
	"""
	Generate K_d matrices, assuming known statistics of tuning curves for 
	individual receptors. 
	
	Args:
		shape: shape of K_d matrices.
		receptor-activity_mus: Length Mm vector for average activity response
			of receptor to monomolecular odorant.
		receptor_activity_sigmas: Length Mm vector for averages spread of 
			activity response of monomolecular odorants.
	"""

	Mm, Nn = shape
	Kk2 = sp.zeros(shape)
	
	assert Mm == len(receptor_activity_mus), \
			"Mean receptor activity vector dimension != measurement "\
			"dimension %s" % Mm
	assert Mm == len(receptor_activity_sigmas), \
			"St dev receptor activity vector dimension != measurement "\
			"dimension %s" % Mm
	
	warnings.filterwarnings('error')
	sp.random.seed(seed)
	
	print ("Generating Kk2 matrix rows from Gaussian tuning curves...")
	for iM in range(Mm):
		print ('\nRow %s..' % iM)
		sample_lower_bnd  = -10000
		sample_upper_bnd = 10000
		bounds_too_lax = True
		while (bounds_too_lax == True):
			try:
				args_dict = dict(activity_mu=receptor_activity_mus[iM], 
								activity_sigma=receptor_activity_sigmas[iM], 
								Ss0=Ss0, eps=eps, size=Nn)
				Kk2_rv_object = Kk_dist_Gaussian_activity(a=sample_lower_bnd, 
															b=sample_upper_bnd)
				Kk2[iM, :]  = (Kk2_rv_object.rvs(**args_dict))
				assert sp.all(Kk2[iM, :] != sample_lower_bnd), 
											"Lower bound hit"
				assert sp.all(Kk2[iM, :] != sample_upper_bnd), 
											"Upper bound hit"
				assert sp.all(Kk2[iM, :] != 0), "zero"
				bounds_too_lax = False
			except Warning as e:
				sample_lower_bnd = sample_lower_bnd/5.
				sample_upper_bnd = sample_upper_bnd/5.
				print ('No convergence; bounds --> %s, %s..   ' 
						% (sample_lower_bnd, sample_upper_bnd))
				pass
			except AssertionError as e:
				sample_lower_bnd = sample_lower_bnd/5.
				sample_upper_bnd = sample_upper_bnd/5.
				print ('%s; bounds --> %s, %s..   ' 
						% (e, sample_lower_bnd, sample_upper_bnd))
				pass
		print ('..OK')
	print ("\nKk2 matrix successfully generated\n")
	
	return Kk2