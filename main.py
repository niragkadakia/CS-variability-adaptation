import scipy as sp
import matplotlib.pyplot as plt
from utils import *

nSignal = 100
nSparsity = 7
nSensor = 30
seedSs = 111
seedRr = 22
seedYy = 13

Ss, Rr, Yy, res_rec_weak = decode_rec_bind_CS(nSparsity, nSignal, nSensor,
                     lowSs = 1, highSs = 2, seedSs = seedSs,
					 typeKk = 'normal', meanKk = 0, sigmaKk = 2, seedKk = 1,
                     meanRr = 0, sigmaRr = 1, seedRr = seedRr, 
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_weak", precision = 1e2)
					
Ss, Rr, Yy, res_rec_strong = decode_rec_bind_CS(nSparsity, nSignal, nSensor,
                     lowSs = 1, highSs = 2, seedSs = seedSs,
					 typeKk = 'normal', meanKk = 0, sigmaKk = 2, seedKk = 1,
                     meanRr = 0, sigmaRr = 1, seedRr = seedRr, 
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)

Ss, Rr, Yy, res_trad = decode_CS(nSparsity, nSignal, nSensor,
                     lowSs = 1, highSs = 2, seedSs = seedSs,
					 meanRr = 0, sigmaRr = 2, seedRr = seedRr, 
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)
fig = plt.figure()
fig.set_size_inches(15,4)
plt.plot(Ss,linewidth=3,color='orange',label='true')
plt.plot(res_trad.x, linewidth =4, linestyle = '--', color = 'blue', label = 'tradition')
plt.plot(res_rec_weak.x, linewidth =4, linestyle = '--', color = 'green', label = 'receptors weak')
plt.plot(res_rec_strong.x, linewidth =4, linestyle = '--', color = 'red', label = 'receptors strong')
plt.legend()
plt.show()

error_trad = sp.sum(res_trad.x - Ss)**2.0/nSignal
error_rec_weak = sp.sum(res_rec_weak.x - Ss)**2.0/nSignal
error_rec_strong = sp.sum(res_rec_strong.x - Ss)**2.0/nSignal

print ("Errors tradition = %s" % error_trad)
print ("Errors receptor weak = %s" % error_rec_weak)
print ("Errors receptor strong = %s" % error_rec_strong)