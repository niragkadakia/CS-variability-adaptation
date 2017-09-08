"""
Error quantification, analysis, etc. methods. 

Created by Nirag Kadakia at 18:00 09-07-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp

def binary_errors(CS_object, nonzero_bounds=[0.7, 1.3], zero_bound=1./25):

	Nn = CS_object.Nn
	mu_dSs = CS_object.mu_dSs
	sparse_idxs =  CS_object.idxs[0]

	errors_nonzero = 0
	errors_zero = 0
	
	for iN in range(Nn):
		if iN in sparse_idxs: 
			scaled_estimate = 1.*CS_object.dSs_est[iN]/CS_object.dSs[iN]
			if nonzero_bounds[0] < scaled_estimate < nonzero_bounds[1]:
				errors_nonzero += 1
		else:
			if abs(CS_object.dSs_est[iN]) <  abs(mu_dSs*zero_bound):
				errors_zero += 1

	errors = dict()
	errors['errors_nonzero'] = sp.around(1.*errors_nonzero/ \
											len(sparse_idxs)*100., 2)
	errors['errors_zero'] = sp.around(1.*errors_zero/ \
											(Nn - len(sparse_idxs))*100., 2)
										
	return errors

def MSE_errors(CS_object):

	Nn = CS_object.Nn
	sparse_idxs =  CS_object.idxs[0]

	errors_nonzero = 0
	errors_zero = 0
	
	for iN in range(Nn):
		if iN in sparse_idxs: 
			errors_zero += (CS_object.dSs[iN] - CS_object.dSs_est[iN])**2.0
		else:
			errors_nonzero += (CS_object.dSs[iN] - CS_object.dSs_est[iN])**2.0
	
	errors = dict()
	errors['errors_nonzero'] = errors_nonzero/Nn
	errors['errors_zero'] = errors_zero/Nn
										
	return errors