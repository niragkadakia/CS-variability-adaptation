"""
Script to encode and decode sparse signals using compressed sensing
but with passing a sparse odor signal through a sensory system 
described by a 2-state bound/unbound receptor system. Off and on states 
are treated equally here, and binding kinetics are assumed fast 
enought to leave near the steady state limit. 

The response matrix is assumed to be a linearization of the full
nonlinear response. This linearization is essentially the matrix of 
inverse disassociation constants. This script tests the decoding 
fidelity for various choices of the  mean value of the inverse K. 

Created by Nirag Kadakia at 17:30 07-31-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""


import scipy as sp
import matplotlib.pyplot as plt
import sys
sys.path.append('../src')
from utils import *

## Set globals
nSignal = 50
nSparsity = 3
nSensor = 15
seedSs = 1
seedRr = 10
seedYy = 1
lowSs = 0
highSs = 1
typeSs = 'uniform'
meanKk = .5
sigmaKk = 0.005
miss_threshold = 0.001
SNR = 10
iterations = 50
meanKk_range_log = sp.linspace(-4, -1, 31)

## Set data directory
data_dir = "C:\Users/nk479/Dropbox (emonetlab)/users/nirag_kadakia/data/CS-variability-adaptation/meanKk"

## Ranges to test over
meanKk_range = 10.**(meanKk_range_log)
seedSs_range = sp.arange(iterations)

## Data structures to hold results
errors = sp.zeros((len(meanKk_range),len(seedSs_range),2))
misses = sp.zeros((len(meanKk_range),len(seedSs_range),2))


## Run the loops to encode and decode
for idx, meanKk in enumerate(meanKk_range):	
	print (meanKk)
	for idy, seedSs in enumerate(seedSs_range):
		seedRr = seedSs
		
		sigmaKk = meanKk/SNR
		Ss, Rr, Yy, res_trad = decode_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 meanRr = meanKk, sigmaRr = sigmaKk, seedRr = seedRr, 
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)
		
		errors[idx,idy,0] = (sp.sum((res_trad.x - Ss)**2.0)/nSignal)
		if errors[idx,idy,0] > miss_threshold: 
			misses[idx,idy,0] = 1.
		
		Ss, Rr, Yy, res_rec_strong = decode_rec_bind_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 typeKk = 'normal', meanKk = meanKk, sigmaKk = sigmaKk, seedKk = seedRr,
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)
		errors[idx,idy,1] = (sp.sum((res_rec_strong.x - Ss)**2.0)/nSignal)
		if errors[idx,idy,1] > miss_threshold: 
			misses[idx,idy,1] = 1.
		
		#plt.plot(Ss, label = 'true')
		#plt.plot(res_rec_strong.x, label = 'straong')
		#plt.plot(res_trad.x, label = 'trad')
		#plt.legend()
		#plt.show()
		
		
## Save the data
errors_to_save = sp.vstack((meanKk_range.T, sp.average(errors, axis = 1).T)).T
sp.savetxt('%s/errors.dat' %data_dir, errors_to_save, delimiter = "\t", fmt = "%.6e")
misses_to_save = sp.vstack((meanKk_range.T, sp.average(misses, axis = 1).T)).T
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
