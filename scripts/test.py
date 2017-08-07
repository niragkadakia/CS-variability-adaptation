
import scipy as sp
import sys
sys.path.append('../src')
import matplotlib.pyplot as plt
from load_data import *


try:
	data_flag = str(sys.argv[1])
except:
	raise Exception("Need to specify a tag for the data")

# Load relevant variables from file
vars_to_load = ["outer_var", "inner_var", "outer_vals", "inner_vals"]


# Get errors and other data
errors = load_errors(data_flag)
structs, vars_dict = load_structs(data_flag)
for idx in vars_to_load:
	exec("%s = vars_dict['%s']" %(idx,idx))
nX, nY = len(outer_vals), len(inner_vals)

# Plot
avg_act = []
opt_outer_val = []
for idx in range(nX):
	plt.plot(inner_vals, errors[idx,:])
	opt_outer_val.append(sp.argmin(errors[idx,:]))
	avg_act.append(sp.average(structs[idx,opt_outer_val[idx]].Yy))
plt.show()

plt.plot(outer_vals, avg_act)
plt.show()


plt.plot(outer_vals, opt_outer_val)
plt.xlabel("%s" % outer_var)
plt.ylabel("optimal %s" % inner_var)
plt.show()