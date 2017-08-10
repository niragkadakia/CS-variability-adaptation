"""
Object to encode and decode sparse signals using compressed sensing
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
		self.Kk = 5
		self.Mm = 20

		# Set random seeds
		self.seed_Ss0 = 1
		self.seed_dSs = 1
		self.seed_Kk1 = 1
		self.seed_Kk2 = 1
		self.seed_eps = 1
		
		# Fluctuations
		self.mu_dSs = 0.3
		self.sigma_dSs = 0.1
		
		# Background
		self.mu_Ss0 = 1.
		self.sigma_Ss0 = 0.001
		
		# K1
		self.mu_Kk1 = 1e4
		self.sigma_Kk1 = 1e3
		
		# K2
		self.mu_Kk2 = 1e-3
		self.sigma_Kk2 = 1e-4
		
		# Non-equilibrium
		self.mu1_eps = 5.0
		self.sigma1_eps = 0.1
		self.mu2_eps = 5.0
		self.sigma2_eps = 0.1
		self.prob_1_eps = 0.5
		self.eps_type = 'normal'
		
		# Overwrite variables with passed arguments	
		for key in kwargs:
			exec ('self.%s = kwargs[key]' % key)
		
		# Group the variables
		self.params_dSs = [self.mu_dSs, self.sigma_dSs]
		self.params_Ss0 = [self.mu_Ss0, self.sigma_Ss0]
		self.params_Kk1 = [self.mu_Kk1, self.sigma_Kk1]
		self.params_Kk2 = [self.mu_Kk2, self.sigma_Kk2]
		self.params_eps = [self.mu1_eps, self.sigma1_eps, self.mu2_eps, self.sigma2_eps, self.prob_1_eps]
	
	
	def set_signals(self):
		self.dSs, self.idxs = set_signal([self.Nn, self.Kk], self.params_dSs, seed = self.seed_dSs)
		
		# Ss_0 is the ideal (learned) background stimulus without noise
		self.Ss_0, self.Ss_0_noisy = set_signal_bkgrnd([self.Nn, self.Kk], self.idxs, self.params_Ss0, seed = self.seed_Ss0)
		
		# The true signal, including background noise
		self.Ss = self.dSs + self.Ss_0_noisy
		
	def set_kinetics(self):	
		self.Kk_1 = random_matrix([self.Mm,self.Nn], self.params_Kk1, seed = self.seed_Kk1)
		self.Kk_2 = random_matrix([self.Mm,self.Nn], self.params_Kk2, seed = self.seed_Kk2)
		
	def set_measured_activity(self):
	
		# free energy as random vector if assigned as such
		self.eps = random_matrix([self.Mm], self.params_eps, type = self.eps_type, seed = self.seed_eps)
		
		# True receptor activity
		self.Yy = set_receptor_activity(self.Ss, self.Kk_1, self.Kk_2, self.eps)
		
		# Learned background activity can only utilize the average background signal -- this has errors
		self.Yy_0 = set_bkgrnd_activity(self.Ss_0, self.Kk_1, self.Kk_2, self.eps)
		
		# Measured response above background
		self.dYy = self.Yy - self.Yy_0

	def set_linearized_response(self):
	
		# Again, can only use the learned background
		self.Rr = set_gain(self.Ss_0, self.Kk_1, self.Kk_2, self.eps)
		
	def encode(self):
		self.set_signals()
		self.set_kinetics()
		self.set_measured_activity()
		self.set_linearized_response()
		
	def decode(self):
		self.dSs_est = decode_CS(self.Rr, self.dYy)	
