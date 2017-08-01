"""
Script to encode and decode sparse signals using compressed sensing
but with passing a sparse odor signal through a sensory system 
described by a 4-state receptor system. Off and on states 
are distinguished here, and binding kinetics are assumed fast 
enough to leave near the steady state limit. 

The response matrix is assumed to be a linearization of the full
nonlinear response. This linearization is essentially the matrix of 
inverse disassociation constants. This script tests the decoding 
fidelity for various choices of the  mean value of the inverse K. 

Created by Nirag Kadakia at 23:30 07-31-2017
This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. 
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import matplotlib.pyplot as plt
import sys
sys.path.append('../src')
from utils import *
from kinetics import *
from signals import *
from decode_CS import *


class four_state_receptor_CS:	

	"""
	Class object for encoding and decoding a 
	four-state receptor model using compressed 
	sensing
	"""

	def __init__(self, **kwargs):
	
		# Set globals
		self.Nn = 50
		self.Kk = 3
		self.Mm = 20

		# Set random seeds
		self.seedSs = 1
		self.seedKk_p = 1
		self.seedKk_m = 1
		
		
		# Fluctuations
		self.muSs = 2
		self.sigmaSs = .1

		# Background
		self.muSs_0 = 2.
		self.sigmaSs_0 = 0

		# K2
		self.muKk_p = .001
		self.sigmaKk_p = 0.0001

		# K1
		self.muKk_m = 1000
		self.sigmaKk_m = 10

		# Non-equilibrium
		self.epsilon = 4

		# Overwrite variables with passed arguments	
		for key in kwargs:
			exec ("self.%s = %s" % (key, kwargs[key]))
			
		## Group the variables
		self.nDims = [self.Nn, self.Kk, self.Mm]
		self.paramsSs = [self.muSs, self.sigmaSs]
		self.paramsSs_0 = [self.muSs_0, self.sigmaSs_0]
		self.paramsKk_p = [self.muKk_p, self.sigmaKk_p]
		self.paramsKk_m = [self.muKk_m, self.sigmaKk_m]
	
	def set_signals(self):
		self.dSs, self.idxs = set_signal(self.nDims[:2], self.paramsSs, seed = self.seedSs)
		self.Ss_0 = set_signal_bkgrnd(self.nDims[:2], self.idxs, self.paramsSs_0, seed = self.seedSs)
		self.Ss = self.dSs + self.Ss_0
		
	def set_kinetics(self):	
		self.Kk_p = random_matrix([self.Mm,self.Nn], self.paramsKk_p, seed = self.seedKk_p)
		self.Kk_m = random_matrix(self.nDims[0::-2], self.paramsKk_m, seed = self.seedKk_m)

	def set_measured_activity(self):
		self.Yy = set_receptor_activity(self.Ss, self.Kk_p, self.Kk_m, self.epsilon)
		self.Yy_0 = set_bkgrnd_activity(self.Ss_0, self.Kk_p, self.Kk_m, self.epsilon)
		self.dYy = self.Yy - self.Yy_0

	def set_linearized_response(self):
		self.Rr = set_gain(self.Ss_0, self.Kk_p, self.Kk_m, self.epsilon)
		
	def encode(self):
		self.set_signals()
		self.set_kinetics()
		self.set_measured_activity()
		self.set_linearized_response()
		
	def decode(self):
		self.dSs_est = decode_CS(self.Rr, self.dYy)	
