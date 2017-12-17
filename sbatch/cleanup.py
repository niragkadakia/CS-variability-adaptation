"""
Find files that may have not been estimated and do the estimation
"""

import scipy as sp
import sys
sys.path.append('../scripts')
import os.path
from CS_run import CS_run

data_dir = "/home/fas/emonet/nk479/project/data/CS-variability-adaptation"
data_flag = str(sys.argv[1])
filename = "%s/%s.txt" % (data_dir, data_flag)

obj_idxs = [100, 100]

for idx in range(obj_idxs[0]):
	for idy in range(obj_idxs[1]):
		filename = "%s/objects/%s/[%s, %s].pklz" % (data_dir, data_flag, idx, idy)
		if not os.path.isfile(filename):
			CS_run(data_flag, iter_var_idxs=[idx, idy])
