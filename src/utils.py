import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import sys

			
##################
###   Signal   ###
##################	
			
			
def set_signal(nDims, params, type ='normal', seed = 0):
	
	"""
	Set sparse stimulus with given statistics
	"""
	
	Nn, Kk = nDims
	Ss = sp.zeros(Nn)
	
	sp.random.seed(seed)
	
	for iK in range(Kk): 
		if type == "normal":
			mu, sigma = params
			Ss[iK] = sp.random.normal(mu, sigma)
		elif type == "uniform":
			lo, hi = params
			Ss[iK] = sp.random.uniform(lo,hi)
	
	sp.random.shuffle(Ss)
	idxs = sp.nonzero(Ss)
	
	return Ss, idxs

	
def set_signal_bkgrnd(nDims, idxs, params, type ='normal', seed = 0):

	"""
	Set sparse stimulus background on nonzero components
	"""

	Nn, Kk = nDims
	Ss = sp.zeros(Nn)
	
	sp.random.seed(seed)

	for iK in idxs: 
		if type == "normal":
			mu, sigma = params
			if sigma != 0:
				Ss[iK] += sp.random.normal(mu, sigma)
			else:
				Ss[iK] += mu
		elif type == "uniform":
			lo, hi = params
			Ss[iK] += sp.random.uniform(lo, hi)
	
	return Ss

def noisify(Ss, params):

	"""
	Adds noise to any vector
	"""
	
	mu, sigma = params
	size = Ss.shape
	Ss += sp.random.normal(mu, sigma, size)
	return Ss
	
	
####################
###   Matrices   ###
####################	
	
	
def random_matrix(size, params, type = 'normal', seed = 0):

	"""
	Generate random matrix with given distribution
	"""
	
	if type == 'normal':
		sp.random.seed(seed)
		mean, sigma = params
		return sp.random.normal(mean, sigma, size)
	elif type == 'uniform':
		sp.random.seed(seed)
		lo, hi = params
		return sp.random.normal(lo, hi, size)
	else:
		print ('No proper matrix type!')
		exit()
			

#####################
###   Responses   ###
#####################			
	
	
def set_bind_act_response(Rr, Ss, args):

	"""
	Set binding and activation response 
	"""
	
	noise, mean, sigma, seed = args 
	Yy = sp.dot(Rr, Ss)
	if noise == True:
		sp.random.seed(seed)
		Yy += sp.random.normal(mean, sigma, size=Yy.shape)
	return Yy
	

def set_bkgrnd_act(Ss_0, Kk_p, Kk_m, epsilon):

	"""
	Set background activity
	"""
	
	Kk_p_sum = sp.dot(Kk_p**-1., Ss_0)
	Aa_0 = Kk_p_sum / (Kk_p_sum + sp.exp(epsilon))
	return Aa_0
	

def set_bind_act_gain(Ss_0, Kk_p, Kk_m, epsilon):

	"""
	Set linearized binding and activation gain
	"""
		
	num = sp.exp(epsilon)*Kk_p**-1.
	Kk_p_sum = sp.dot(Kk_p**-1., Ss_0)
	den = (sp.exp(epsilon) + Kk_p_sum )**2.0
	dAadSs_0 = (num.T/den).T
	return dAadSs_0
	
	
########################
### Binding kinetics ###
########################	
	
	
def set_rec_resp_bind_only(Ss, Kk):
	Kk_sum = sp.dot(Kk**-1.0, Ss)
	Pb = Kk_sum/(1. + Kk_sum)
	return Pb
	

def set_receptor_activity(Ss, Kk_p, Kk_m, epsilon):
	
	"""
	Steady state activity with binding and activation 
	Kk_p is the activated disassociation constants (K2)
	Kk_m is the inactivated disassociation constants (K1)
	K1 = KK_m >> S_0 >> Kk_p = K2
	"""
	
	Kk_p_sum = sp.dot(Kk_p**-1.0, Ss)
	Kk_m_sum = sp.dot(Kk_m**-1.0, Ss)
	Aa = (1. + sp.exp(epsilon)*(1 + Kk_m_sum)/(1 + Kk_p_sum))**-1.0
	
	return Aa

	
########################
###    Decoding      ###
########################
	
	
	
def decode_CS(Rr, Yy, opt_type = "L1_strong", precision = 'None', init_params = [0,1]):
	
	"""
	CS with binding and activation kinetics
	"""		

	def L1_strong(x):
		return sp.sum(abs(x))

	def L1_weak(x,*args):
		Rr, Yy, precision = args
		tmp1 = sp.sum(abs(x))
		tmp2 = precision*sp.sum((sp.dot(Rr, x) - Yy)**2.0)
		return tmp1+tmp2

	Nn = len(Rr[0,:])
	
	if opt_type == "L1_strong":
		constraints = ({'type': 'eq', 'fun': lambda x: sp.dot(Rr, x) - Yy})
		res = minimize(L1_strong, sp.random.normal(init_params[0], init_params[1], Nn), method='SLSQP',constraints = constraints)
	elif opt_type == "L1_weak":
		res = minimize(L1_weak, sp.random.normal(init_params[0], init_params[1], Nn), args = (Rr, Yy, precision), method='SLSQP')
	
	return res.x
	
	
