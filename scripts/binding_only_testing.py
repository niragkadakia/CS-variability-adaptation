import scipy as sp
import matplotlib.pyplot as plt
import sys
sys.path.append('../src')
from utils import *

nSignal = 100
nSparsity = 6
nSensor = 25
seedSs = 1
seedRr = 2242
seedYy = 13
lowSs = 0
highSs = 2
typeSs = 'normal'
meanKk_f = 20
sigmaKk_f = 0.5
meanKk_b = 5
sigmaKk_b = 0.5


Ss, Rr, Yy, res_rec_weak = decode_rec_bind_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 typeKk_f = 'normal', meanKk_f = meanKk_f, sigmaKk_f = sigmaKk_f, seedKk_f = 1,
                     typeKk_b = 'normal', meanKk_b = meanKk_b, sigmaKk_b = sigmaKk_b, seedKk_b = 1,
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_weak", precision = 1e1)
				
Ss, Rr, Yy, res_rec_strong = decode_rec_bind_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 typeKk_f = 'normal', meanKk_f = meanKk_f, sigmaKk_f = sigmaKk_b, seedKk_f = 1,
                     typeKk_b = 'normal', meanKk_b = meanKk_b, sigmaKk_b = sigmaKk_b, seedKk_b = 1,
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)

Ss, Rr, Yy, res_trad = decode_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 meanRr = 0, sigmaRr = 1, seedRr = seedRr, 
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

error_trad = sp.sum((res_trad.x - Ss)**2.0)/nSignal
error_rec_weak = sp.sum((res_rec_weak.x - Ss)**2.0)/nSignal
error_rec_strong = sp.sum((res_rec_strong.x - Ss)**2.0)/nSignal

print ("Errors tradition = %s" % error_trad)
print ("Errors receptor weak = %s" % error_rec_weak)
print ("Errors receptor strong = %s" % error_rec_strong)


errors = []
errors2 = []
test_range = sp.arange(1, 50,2)
for meanKk_b in test_range:
	print (meanKk_b)

	Ss, Rr, Yy, res_trad = decode_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 meanRr = 0, sigmaRr = 2, seedRr = seedRr, 
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)
	errors.append(sp.sum((res_trad.x - Ss)**2.0)/nSignal)
	
	Ss, Rr, Yy, res_rec_strong = decode_rec_bind_CS(nSparsity, nSignal, nSensor,
                     typeSs = typeSs, lowSs = lowSs, highSs = highSs, seedSs = seedSs,
					 typeKk_f = 'normal', meanKk_f = meanKk_f, sigmaKk_f = sigmaKk_b, seedKk_f = 1,
                     typeKk_b = 'normal', meanKk_b = meanKk_b, sigmaKk_b = sigmaKk_b, seedKk_b = 1,
                     noiseYy = False, meanYy = 0, sigmaYy = 2, seedYy = seedYy,
					 opt_type = "L1_strong", precision = None)
	errors2.append(sp.sum((res_rec_strong.x - Ss)**2.0)/nSignal)

plt.plot(test_range,errors)
plt.plot(test_range,errors2)
plt.yscale('log')
plt.show()
					 