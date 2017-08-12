"""
General, miscellaneous functions for statistical analysis of data.

Created by Nirag Kadakia at 18:03 08-11-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license,
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
from scipy.stats import linregress
import matplotlib.pyplot as plt

def power_law_regress(x, y, **kwargs):
	"""
	Plot a power law fit on an existing figure
	"""
	slope, y_int, r_value, p_value, std_err = linregress(sp.log(x), sp.log(y))
	plt.plot(x, sp.exp(slope*sp.log(x) + y_int), color = 'orangered', 
				linestyle='--', linewidth = 3)
	
	print ('Power Law: slope = %.5f...r_value = %.5e...p_value = '\
			'%.5e...std_err = %.5e' % (slope, r_value, p_value, std_err))
	
	return slope, y_int, r_value, p_value, std_err

def lognormal_regress(x, y, **kwargs):
	"""
	Plot a lognormal fit on an existing figure
	"""

	slope, y_int, r_value, p_value, std_err = linregress(sp.log(x), y)
	plt.plot(x, slope*sp.log(x) + y_int, color = 'orangered', 
				linestyle='--', linewidth = 3)

	print ('Lognormal: slope = %.5f...r_value = %.5e...p_value = '\
			'%.5e...std_err = %.5e' % (slope, r_value, p_value, std_err))
	
	return slope, y_int, r_value, p_value, std_err
