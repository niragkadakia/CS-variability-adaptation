import scipy as sp


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
