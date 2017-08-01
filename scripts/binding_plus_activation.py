"""
Script to encode and decode sparse signals using compressed sensing
but with passing a sparse odor signal through a sensory system 
described by a 4-state receptor system. Off and on states 
are distinguished here, and binding kinetics are assumed fast 
enough to leave near the steady state limit. 

The response matrix is assumed to be a linearization of the full
nonlinear response. This linearization is essentially the matrix of 
inverse disassociation constants. This script tests the decoding 
fidelity for various choices of the  mean value of the inverse K. 

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import matplotlib.pyplot as plt
import sys
sys.path.append('../src')
from utils import *

## Set data directory
data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation/meanKk"

## Set globals
Nn = 50
Kk = 3
Mm = 20
seedSs = 340
seedRr = 1
seedYy = 1

# Fluctuations
muSs = 2
sigmaSs = .1

# Background
muSs_0 = 2.
sigmaSs_0 = 0

# K2
muKk_p = .001
sigmaKk_p = 0.0001

# K1
muKk_m = 1000
sigmaKk_m = 10

# Non-equilibrium
epsilon = 4

test = sp.linspace(-1,3,20)

for iK in test:

	muSs_0 = sp.exp(iK)
	print (muSs_0)
	sigmaSs_0 = muSs_0/10
	
	nDims = [Nn, Kk, Mm]
	paramsSs = [muSs, sigmaSs]
	paramsSs_0 = [muSs_0, sigmaSs_0]
	paramsKk_p = [muKk_p, sigmaKk_p]
	paramsKk_m = [muKk_m, sigmaKk_m]

	# Set signals
	dSs, idxs = set_signal(nDims[:2], paramsSs, seed = seedSs)
	Ss_0 = set_signal_bkgrnd(nDims[:2], idxs, paramsSs_0, seed = seedSs)
	Ss = dSs + Ss_0
	#Ss = noisify(Ss, [0, sigmaSs])

	# Set kinetics
	Kk_p = random_matrix([Mm,Nn], paramsKk_p)
	Kk_m = random_matrix(nDims[0::-2], paramsKk_m)

	# Set measured activity
	Yy = set_receptor_activity(Ss, Kk_p, Kk_m, epsilon)
	Yy_0 = set_bkgrnd_act(Ss_0, Kk_p, Kk_m, epsilon)
	dYy = Yy - Yy_0

	# Set linearization for CS
	Rr = set_bind_act_gain(Ss_0, Kk_p, Kk_m, epsilon)

	# Decode!
	dSs_est = decode_CS(Rr, dYy)	

	plt.plot(dSs_est)
	plt.plot(dSs)
	plt.show()	

"""
## Save the data
errors_to_save = sp.vstack((meanKk_p_range.T, sp.average(errors, axis = 1).T)).T
sp.savetxt('%s/errors.dat' %data_dir, errors_to_save, delimiter = "\t", fmt = "%.6e")
misses_to_save = sp.vstack((meanKk_p_range.T, sp.average(misses, axis = 1).T)).T
sp.savetxt('%s/misses.dat' %data_dir, misses_to_save, delimiter = "\t", fmt = "%.4e")

## Save metadata 
meta = '''
nSignal = %s\n
nSparsity = %s\n
nSensor = %s\n
lowSs = %s\n
highSs = %s\n
typeSs = %s\n
miss_threshold = %s\n
SNR = %s\n
iterations = %s\n
''' %(nSignal, nSparsity, nSensor, lowSs, highSs, typeSs, miss_threshold, SNR, iterations)
text_file = open("%s/metadata.dat" % (data_dir), "w")
text_file.write(meta)
text_file.close()
"""