import scipy as sp
import pickle
import shelve

def load_errors(data_flag, 
	data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation"):
    
	"""
	Load error data from compressed sensing 
	encoding/decoding module 
	"""

	errors = sp.loadtxt('%s/errors_%s.dat' %(data_dir, data_flag))
	return errors
	
def load_structs(data_flag,
	data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation"):

	"""
	Load globals and class structures from 
	compressed sensing encoding/decoding
	"""

	f = '%s/globals_%s.out' % (data_dir, data_flag)
	vars_dict = shelve.open(f,'r')
	nX, nY = vars_dict["nX"], vars_dict["nY"]
	
	f = open('%s/structures_%s.pckl' % (data_dir, data_flag), 'rb')
	structs = sp.asarray(pickle.load(f))
	f.close()
	structs  = structs.reshape((nX, nY))

	return structs, vars_dict
