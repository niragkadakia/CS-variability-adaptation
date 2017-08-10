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

