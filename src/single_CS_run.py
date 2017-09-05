

def CS_run(vars_to_pass=dict(), run_specs=dict()):
	
	a = four_state_receptor_CS(**vars_to_pass)
	
	if 'run_type' in run_specs.keys():
		val = run_specs['run_type']
		if val[0] == 'normal_Kk':
			a.encode_normal_Kk()
		elif val[0] == 'normal_activity':
			a.encode_normal_activity()
		elif val[0]  == 'normal_activity_WL':
			WL_rule = dict(eps = float(val[1]) + float(val[2])
							*sp.log(vars_to_pass['mu_Ss0']))
			a.encode_normal_activity_WL(**WL_rule)
		else:
			print ('Run specification %s not recognized' % key)
	else:
		print ('No run type specified, proceeding with normal_activity')
		a.encode_normal_activity()
		
	a.decode()
	return a