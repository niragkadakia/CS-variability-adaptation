import scipy as sp

def merge_two_dicts(x, y):
   	"""
	Given two dicts, merge them into a 
	new dict as a shallow copy.
	"""

	z = x.copy()
	z.update(y)
	
	return z
		
def noisify(Ss, params):
	"""
	Adds noise to any vector
	"""
	
	mu, sigma = params
	size = Ss.shape
	Ss += sp.random.normal(mu, sigma, size)
	
	return Ss
	
	
def random_matrix(size, params, type = 'normal', seed = 0):
	"""
	Generate random matrix with given distribution
	"""
	
	if type == 'normal':
		sp.random.seed(seed)
		mean, sigma = params[:2]
		if sigma != 0.:
			return sp.random.normal(mean, sigma, size)
		else:
			return mean*sp.ones(size)
	
	elif type == 'uniform':
		sp.random.seed(seed)
		lo, hi = params[:2]
		return sp.random.normal(lo, hi, size)
	
	elif type == "gaussian_mixture":
		
		mean1, sigma1, mean2, sigma2, prob_1 = params[:5]
		assert prob_1 <= 1., "Gaussian mixture needs p < 1" 
		
		sp.random.seed(seed)
		mixture_idxs = sp.random.binomial(1, prob_1, size)
		it = sp.nditer(mixture_idxs, flags=['multi_index'])
		out_vec = sp.zeros(size)
		
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

def sparse_vector(nDims, params, type ='normal', seed = 0):
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
	
def sparse_vector_bkgrnd(nDims, idxs, params, type ='normal', seed = 0):
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
