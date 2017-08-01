import scipy as sp
import sys
sys.path.append('../src')
import matplotlib.pyplot as plt
from four_state_receptor_CS import *


test = sp.linspace(1,3,20)

test2 = sp.linspace(-2,3,20)

errors = sp.zeros((len(test), len(test2)))

for idxK, iK in enumerate(test):
	epsilon = sp.exp(iK)
	
	print (epsilon)
	
	for idxL, iL in enumerate(test2):

		muSs_0 = sp.exp(iL)
		
		a = four_state_receptor_CS(epsilon = epsilon, muSs_0 = muSs_0)
		
		a.encode()
		a.decode()
		
		errors[idxK, idxL] = (sp.sum((a.dSs_est - a.dSs)**2.0)/a.Nn)

	sp.savetxt('errors.dat', errors)

mins = []
for idxK, iK in enumerate(test):
	mins.append(min(errors[idxK,:]))
	plt.plot(test2, errors[idxK,:])
plt.show()

plt.plot(sp.exp(test), mins)
plt.show()
	