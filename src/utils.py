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

def set_signal_with_bkgrnd(args):
	nSparsity, nSignal, typeSs, low, high, bkgrndMean, bkgrndDev, seed = args
	Ss = sp.zeros(nSignal)
	sp.random.seed(seed)
	for iK in range(nSparsity): 
		if typeSs == "normal":
			Ss[iK] = sp.random.normal(low,high)
		elif typeSs == "uniform":
			Ss[iK] = sp.random.uniform(low,high)
	for iK in range(nSignal):
		Ss[iK] += sp.random.normal(bkgrndMean, bkgrndDev)
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

def set_response_minus_bkgrnd(Rr, Ss, args):
	noise, mean, sigma, bkgrnd, seed = args 
	Ss -= bkgrnd
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
		
	
## Set receptor response in fast binding limit, no (in)activation
def set_receptor_response(Ss, Kk):
	Kk_sum = sp.dot(Kk, Ss)
	Pb = Kk_sum/(1. + Kk_sum)
	return Pb
	
def set_receptor_response_minus_bkgrnd(Ss, Kk, args):
	bkgrnd = args
	Ss -= bkgrnd
	Kk_sum = sp.dot(Kk, Ss)
	Pb = Kk_sum/(1. + Kk_sum)
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
		   meanKk, sigmaKk, seedKk,
		   noiseYy, meanYy, sigmaYy, seedYy,
		   opt_type, precision):
	
	Ss = set_signal((nSparsity, nSignal, typeSs, lowSs, highSs, seedSs))
	Rr = set_response_matrix((meanKk, sigmaKk, nSensor, nSignal, seedKk))
	Yy = set_receptor_response(Ss, Rr)
	
	if opt_type == "L1_strong":
		constraints = ({'type': 'eq', 'fun': lambda x: sp.dot(Rr,x) - Yy})
		res = minimize(L1_strong, sp.random.normal(0,1,nSignal), method='SLSQP' ,constraints=constraints)
	elif opt_type == "L1_weak":
		res = minimize(L1_weak, sp.random.normal(0,1,nSignal), args=(Rr,Yy,precision), method='SLSQP')
		
	return [Ss, Rr, Yy, res]
	