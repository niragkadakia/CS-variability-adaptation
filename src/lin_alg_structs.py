"""
Functions for creating random and non-random linear algebraic
structures.

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp

def random_matrix(shape, params, type='normal', seed=0):
	"""
	Generate random matrix with given distribution
	"""
	
	if type == 'normal':
		sp.random.seed(seed)
		mean, sigma = params[:2]
		if sigma != 0.:
			return sp.random.normal(mean, sigma, shape)
		else:
			return mean*sp.ones(shape)
	
	elif type == "rank2_row_gaussian":
		sp.random.seed(seed)
		means, sigmas = params[:2]
		
		assert len(shape) == 2, "rank2_row_gaussian method needs a 2x2 matrix"
		nRows, nCols = shape
		assert len(means) == nRows, "rank2_row_gaussian needs " \
										"mu vector of proper length"
		assert len(sigmas) == nRows, "rank2_row_gaussian needs " \
										"sigma vector of proper length"
		out_matrix = sp.zeros(shape)
		
		for iRow in range(nRows):
			out_matrix[iRow, :] = sp.random.normal(means[iRow], sigmas[iRow], 
													nCols)
		return out_matrix
	
	elif type == 'uniform':
		sp.random.seed(seed)
		lo, hi = params[:2]
		return sp.random.normal(lo, hi, shape)
	
	elif type == "gaussian_mixture":
		mean1, sigma1, mean2, sigma2, prob_1 = params[:5]
		assert prob_1 <= 1., "Gaussian mixture needs p < 1" 
		
		sp.random.seed(seed)
		mixture_idxs = sp.random.binomial(1, prob_1, shape)
		it = sp.nditer(mixture_idxs, flags=['multi_index'])
		out_vec = sp.zeros(shape)
		
		while not it.finished:
			if mixture_idxs[it.multi_index] == 1: 
				out_vec[it.multi_index] = sp.random.normal(mean1, sigma1)
			else:
				out_vec[it.multi_index] = sp.random.normal(mean2, sigma2)
			it.iternext()
		
		return out_vec
	
	else:
		print ('No proper matrix type!')
		exit()

def sparse_vector(nDims, params, type='normal', seed=0):
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
	
def sparse_vector_bkgrnd(nDims, idxs, params, type='normal', seed=0):
	"""
	Set sparse stimulus background on nonzero components
	of a sparse vector, componenents in list 'idxs'
	"""

	Nn, Kk = nDims
	Ss = sp.zeros(Nn)
	Ss_noisy = sp.zeros(Nn)
	
	sp.random.seed(seed)

	for iK in idxs: 
		if type == "normal":
			mu, sigma = params
			Ss[iK] = mu
			if sigma != 0:
				Ss_noisy[iK] += sp.random.normal(mu, sigma)
			else:
				Ss_noisy[iK] += mu
		elif type == "uniform":
			lo, hi = params
			Ss[iK] = lo + (hi - lo)/2.
			Ss_noisy[iK] += sp.random.uniform(lo, hi)
	
	return Ss, Ss_noisy
