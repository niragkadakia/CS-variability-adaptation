import scipy as sp


def set_bkgrnd_activity(Ss_0, Kk_1, Kk_2, eps):

	"""
	Set background activity
	"""
	
	Kk_2_sum = sp.dot(Kk_2**-1., Ss_0)
	Aa_0 = Kk_2_sum / (Kk_2_sum + sp.exp(eps))
	return Aa_0
	

def set_gain(Ss_0, Kk_1, Kk_2, eps):

	"""
	Set linearized binding and activation gain
	"""
	
	num = ((Kk_2.T**-1.)*sp.exp(eps)).T
	Kk_2_sum = sp.dot(Kk_2**-1., Ss_0)
	den = (sp.exp(eps) + Kk_2_sum)**2.0
	dAadSs_0 = (num.T/den).T
	return dAadSs_0
	
	

def set_receptor_activity(Ss, Kk_1, Kk_2, eps):
	
	"""
	Steady state activity with binding and activation 
	Kk_2 is the activated disassociation constants (K2)
	Kk_1 is the inactivated disassociation constants (K1)
	K1 = Kk_1 >> Ss+Ss_0 >> Kk_2 = K2
	"""
	
	Kk_2_sum = sp.dot(Kk_2**-1.0, Ss)
	Kk_1_sum = sp.dot(Kk_1**-1.0, Ss)
	Aa = (1. + sp.exp(eps)*(1 + Kk_1_sum)/(1 + Kk_2_sum))**-1.0
	
	return Aa
