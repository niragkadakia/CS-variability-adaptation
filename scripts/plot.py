import scipy as sp
import matplotlib.pyplot as plt
#test = sp.linspace(0,15, 30) #epsilons
#epsilons = test
#test2 = sp.linspace(-8,18,100) #bkgrnd stimulus
errors = sp.loadtxt('errors.dat')
#errors = sp.loadtxt('errors_muSs=1,sigmaSs=0.1,0-15-30,-8-15-100.dat')

#sigma = 0
errors = sp.loadtxt('errors_sigmaSs_0=0.dat')
test = sp.linspace(10, 30, 50) #background stimulus
muSs_0_s = test
test2 = sp.linspace(-40,20,100) #epsilon
epsilons = test2

#sigma = 1
#errors = sp.loadtxt('errors_sigmaSs_0=1.dat')
#test = sp.linspace(5, 20, 50) #background stimulus
#muSs_0_s = test
#test2 = sp.linspace(-40,20,100) #epsilon
#epsilons = test2

#sigma = 2
#test = sp.linspace(2, 15, 50) #background stimulus
#muSs_0_s = test
#test2 = sp.linspace(-40,20,100) #epsilon
#epsilons = test2

iterations = 1

mins = []
idx = 0
beg = 0
end = 50
test = test[beg:end]
for idxK, iK in enumerate(test):
	mins.append(test2[idx+sp.argmin(errors[idxK+beg,idx:])])
	plt.plot(test2, errors[idxK+beg,:], label  = "%s" % iK)
plt.ylim(1e-6,1e1)
plt.yscale('log')
plt.legend()
plt.show()
mins = sp.asarray(mins)

plt.plot(test, mins)
#plt.plot(test, (1.+sp.exp(mins))**-1.)
plt.show()