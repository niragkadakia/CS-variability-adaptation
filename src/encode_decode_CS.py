"""
Run CS encoding and decoding via four_state_receptor_CS; single iteration.


Created by Nirag Kadakia at 10:30 09-05-2017
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

from four_state_receptor_CS import four_state_receptor_CS


def single_encode_decode_CS(vars_to_pass=dict(), run_specs=dict()):
	"""
	Run CS encoding and decoding via four_state_receptor_CS; single iteration.
	
	Optional args:
		vars_to_pass: dictionary; any overriden arguments to 
						four_state_receptor_CS.
		run_specs: dictionary; parameters of the run.
	"""		
	
	a = four_state_receptor_CS(**vars_to_pass)
	
	if 'run_type' in run_specs.keys():
		val = run_specs['run_type']
		if val[0] == 'normal_Kk':
			a.encode_normal_Kk()
		elif val[0] == 'normal_activity':
			a.encode_normal_activity()
		elif val[0]  == 'exponential_activity':
			a.encode_exponential_activity()
		else:
			print ('Run specification %s not recognized' % key)
	else:
		print ('No run type specified, proceeding with normal_activity')
		a.encode_normal_activity()
		
	a.decode()
	return a