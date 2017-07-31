import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import sys

	
## Set entries in response matrix, chosen normally about zero
def set_response_matrix(args):
	mean, sigma, nSensor, nSignal, seed = args
	sp.random.seed(seed)
	return sp.random.normal(mean, sigma, size=(nSensor,nSignal))
	
## Set signal with sparsity
def set_signal(args):
	nSparsity, nSignal, typeSs, low, high, seed = args
	Ss = sp.zeros(nSignal)
	sp.random.seed(seed)
	for iK in range(nSparsity): 
		if typeSs == "normal":
			Ss[iK] = sp.random.normal(low,high)
		elif typeSs == "uniform":
			Ss[iK] = sp.random.uniform(low,high)
	sp.random.shuffle(Ss)
	return Ss
	
## Generate response 
def set_response(Rr, Ss, args):
	noise, mean, sigma, seed = args 
	Yy = sp.dot(Rr, Ss)
	if noise == True:
		sp.random.seed(seed)
		Yy += sp.random.normal(mean, sigma, size=Yy.shape)
	return Yy

	
########################
### Binding kinetics ###
########################	
	
	
## Set kinetic binding rate matrix
def set_rate_matrix(args):
	sample_type, mean, sigma, nSensor, nSignal, seed = args
	if sample_type == "normal":
		sp.random.seed(seed)
		return sp.random.normal(mean, sigma, size=(nSensor,nSignal))
	elif sample_type == "uniform":
		sp.random.seed(seed)
		return sp.random.uniform(mean, sigma, size=(nSensor,nSignal))
	else:
		print ("Unknown rate matrix sampling scheme!")
		
## Set linearized response matrix for steady state responses in fast binding limit (no activation/inactivation)
def set_linearized_response_matrix(Kk_f, Kk_b):
	nSensor = len(Kk_f[:,0])
	nSignal = len(Kk_f[0,:])
	Rr = sp.zeros(Kk_f.shape)
	for idx in range(nSensor):
		den = sp.sum(Kk_b[idx,:])
		for idy in range(nSignal):
			Rr[idx,idy] = Kk_f[idx,idy]/den
	return Rr

	
## Set receptor response in fast binding limit, no (in)activation
def set_receptor_response(Ss, Kk_f, Kk_b):
	nSensor = len(Kk_f[:,0])
	nSignal = len(Kk_f[0,:])
	Kk_f_sum = sp.dot(Kk_f, Ss)
	Kk_b_sum = sp.sum(Kk_b, axis = 1)
	Pb = Kk_f_sum/(Kk_f_sum + Kk_b_sum)
	return Pb
	
	

########################
###    Decoding      ###
########################
	
	
## Define compressed sensing objective function and constraints
def L1_strong(x):
	tmp = sp.sum(abs(x))
	return tmp

def L1_weak(x,*args):
	Rr, Yy, precision = args
	tmp1 = sp.sum(abs(x))
	tmp2 = precision*sp.sum((sp.dot(Rr, x) - Yy)**2.0)
	return tmp1+tmp2
	
	
## Run optimization with either strong or weak constraints in usual CS scheme
def decode_CS(nSparsity, nSignal, nSensor,
		   typeSs, lowSs, highSs, seedSs,
		   meanRr, sigmaRr, seedRr,
		   noiseYy, meanYy, sigmaYy, seedYy,
		   opt_type, precision):
	
	Ss = set_signal((nSparsity, nSignal, typeSs, lowSs, highSs, seedSs))
	Rr = set_response_matrix((meanRr, sigmaRr, nSensor, nSignal, seedRr))
	Yy = set_response(Rr, Ss, (noiseYy, meanYy, sigmaYy, seedYy))
	
	if opt_type == "L1_strong":
		constraints = ({'type': 'eq', 'fun': lambda x: sp.dot(Rr,x) - Yy})
		res = minimize(L1_strong, sp.random.normal(0,1,nSignal), method='SLSQP' ,constraints=constraints)
	elif opt_type == "L1_weak":
		res = minimize(L1_weak, sp.random.normal(0,1,nSignal), args=(Rr,Yy,precision), method='SLSQP')
	
	return [Ss, Rr, Yy, res]

	
## Run optimization with either strong or weak constraints in nonlinear CS
def decode_rec_bind_CS(nSparsity, nSignal, nSensor,
		   typeSs, lowSs, highSs, seedSs,
		   typeKk_f, meanKk_f, sigmaKk_f, seedKk_f,
		   typeKk_b, meanKk_b, sigmaKk_b, seedKk_b,
		   noiseYy, meanYy, sigmaYy, seedYy,
		   opt_type, precision):
	
	Ss = set_signal((nSparsity, nSignal, typeSs, lowSs, highSs, seedSs))
	Kk_f = set_rate_matrix((typeKk_f, meanKk_f, sigmaKk_f, nSensor, nSignal, seedKk_f))
	Kk_b = set_rate_matrix((typeKk_b, meanKk_b, sigmaKk_b, nSensor, nSignal, seedKk_b))
	Yy = set_receptor_response(Ss, Kk_f, Kk_b)
	
	Rr = set_linearized_response_matrix(Kk_f, Kk_b)
	
	if opt_type == "L1_strong":
		constraints = ({'type': 'eq', 'fun': lambda x: sp.dot(Rr,x) - Yy})
		res = minimize(L1_strong, sp.random.normal(0,1,nSignal), method='SLSQP' ,constraints=constraints)
	elif opt_type == "L1_weak":
		res = minimize(L1_weak, sp.random.normal(0,1,nSignal), args=(Rr,Yy,precision), method='SLSQP')
		
	return [Ss, Rr, Yy, res]
	