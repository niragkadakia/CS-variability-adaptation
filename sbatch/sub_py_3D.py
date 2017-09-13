import scipy as sp
import sys
sys.path.append('../src')
sys.path.append('../scripts')
from utils import get_flag
from CS_run import CS_run

data_flag = get_flag()
fir_range = sp.arange(0, 20)
sec_range = sp.arange(0, 20)
thi_range = sp.arange(0, 25)

for idx in fir_range:
	for idy in sec_range:
		for idz in thi_range:
			iter_vars_idxs = [idx, idy, idz]
			CS_run(data_flag, iter_vars_idxs)

