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
		mean, sigma = params
		if sigma != 0.:
			return sp.random.normal(mean, sigma, size)
		else:
			return mean*sp.ones(size)
	elif type == 'uniform':
		sp.random.seed(seed)
		lo, hi = params
		return sp.random.normal(lo, hi, size)

	else:
		print ('No proper matrix type!')
		exit()

