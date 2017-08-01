import scipy as sp
import sys
sys.path.append('../src')
import matplotlib.pyplot as plt
from four_state_receptor_CS import *


test = sp.linspace(-2,3,20)

errors = []
for iK in test:
	muSs_0 = sp.exp(iK)
	
	a = four_state_receptor_CS(muSs_0 = muSs_0)
	a.encode()
	a.decode()

	errors.append(sp.sum(a.dSs_est - a.dSs)**2.0)
print (a.muSs)
plt.plot(sp.exp(test), errors)
#plt.xscale('log')
plt.show()