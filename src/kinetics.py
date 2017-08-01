import scipy as sp


def set_bkgrnd_activity(Ss_0, Kk_p, Kk_m, epsilon):

	"""
	Set background activity
	"""
	
	Kk_p_sum = sp.dot(Kk_p**-1., Ss_0)
	Aa_0 = Kk_p_sum / (Kk_p_sum + sp.exp(epsilon))
	return Aa_0
	

def set_gain(Ss_0, Kk_p, Kk_m, epsilon):

	"""
	Set linearized binding and activation gain
	"""
		
	num = sp.exp(epsilon)*Kk_p**-1.
	Kk_p_sum = sp.dot(Kk_p**-1., Ss_0)
	den = (sp.exp(epsilon) + Kk_p_sum )**2.0
	dAadSs_0 = (num.T/den).T
	return dAadSs_0
	
	

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
