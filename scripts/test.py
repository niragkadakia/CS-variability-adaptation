
import scipy as sp
import sys
sys.path.append('../src')
import matplotlib.pyplot as plt
from load_data import *

try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")


# Get errors and other data
errors = load_errors(data_flag)
structs, vars_dict = load_structs(data_flag)

# Load relevant variables from file
vars_to_load = ["outer_var", "inner_var", "outer_vals", "inner_vals"]
for idx in vars_to_load:
	exec("%s = vars_dict['%s']" %(idx,idx))
nX, nY = len(outer_vals), len(inner_vals)

avg_act = []

for idx in range(nX):
	plt.plot(inner_vals, errors[idx,:])
	min = sp.argmin(errors[idx,:])
	avg_act.append(sp.average(structs[idx,min].Yy))
plt.show()

plt.plot(outer_vals, avg_act)
plt.show()