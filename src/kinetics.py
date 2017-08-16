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
from scipy.stats import rv_continuous


def bkgrnd_activity(Ss0, Kk_1, Kk_2, eps):
	"""
	Set background activity
	"""
	
	Kk_2_sum = sp.dot(Kk_2**-1., Ss0)
	Aa_0 = Kk_2_sum / (Kk_2_sum + sp.exp(eps))
	
	return Aa_0
	
def linear_gain(Ss0, Kk_1, Kk_2, eps):
	"""
	Set linearized binding and activation gain
	"""
	
	num = ((Kk_2.T**-1.)*sp.exp(eps)).T
	Kk_2_sum = sp.dot(Kk_2**-1., Ss0)
	den = (sp.exp(eps) + Kk_2_sum)**2.0
	dAadSs0 = (num.T/den).T
	
	return dAadSs0
	

def receptor_activity(Ss, Kk_1, Kk_2, eps):
	"""
	Steady state activity with binding and activation 
	Kk_2 is the activated disassociation constants (K2)
	Kk_1 is the inactivated disassociation constants (K1)
	K1 = Kk_1 >> Ss+Ss0 >> Kk_2 = K2
	"""
	
	Kk_1_sum = sp.dot(Kk_1**-1.0, Ss)
	Kk_2_sum = sp.dot(Kk_2**-1.0, Ss)
	Aa = (1. + sp.exp(eps)*(1 + Kk_1_sum)/(1 + Kk_2_sum))**-1.0
	
	return Aa

def free_energy(Ss, Kk_1, Kk_2, A0):
	"""
	Adapted steady state free energy for given 
	stimulus level, disassociation constants, and 
	adapted steady state activity level
	"""
	
	Kk_1_sum = sp.dot(Kk_1**-1.0, Ss)
	Kk_2_sum = sp.dot(Kk_2**-1.0, Ss)
	epsilon = sp.log((1.-A0)/A0*(1. + Kk_2_sum)/(1. + Kk_1_sum))
	
	return epsilon
	
class Kk_dist_norm_activity(rv_continuous):
	"""
	Distribution of Kk_2 = K2 (activated disassociation 
	constants) given a normally-distributed activity 
	level for a given stimulus, adapted epsilon, and
	adapted activity statistics
	"""

	def _argcheck(self, *args):
		# Override argument checking
		return 1

	def _pdf(self, Aa, Ss0, eps, mu_A0, sigma_A0):
		#_argcheck = False
	
		C = sp.exp(-eps)*Ss0
		prefactor = C*(2*sp.pi*sigma_A0**2.0)**.5
		exp_arg = (mu_A0 - 1./(Aa/C + 1))/(2*sigma_A0**2.0)**.5
		
		return 1/prefactor*sp.exp(-exp_arg**2.0)/(Aa/C + 1)**2.0