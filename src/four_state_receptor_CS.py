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
This work is licensed under the 
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
International License. 
To view a copy of this license, 
visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
"""

import scipy as sp
import sys
sys.path.append('../src')
from lin_alg_structs import random_matrix, sparse_vector, sparse_vector_bkgrnd
from kinetics import bkgrnd_activity, linear_gain, receptor_activity, \
						free_energy, Kk2_samples
from decode_CS import decode_CS


class four_state_receptor_CS:	
	"""	
	Encoding and decode a four-state receptor model using compressed sensing
	"""

	def __init__(self, **kwargs):
	
		# Set system parameters
		self.Nn = 300
		self.Kk = 5
		self.Mm = 20

		# Set random seeds
		self.seed_Ss0 = 1
		self.seed_dSs = 1
		self.seed_Kk1 = 1
		self.seed_Kk2 = 1
		self.seed_eps = 1
		self.seed_receptor_activity = 1
		
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
		
		# Free energy statistics
		self.mu_eps = 5.0
		self.sigma_eps = 0.0
		
		# Fixed tuning curve statistics for set activity levels
		self.receptor_tuning_center = [0.2, .0]
		self.receptor_tuning_range = [0.0, 0.3]
		
		# Overwrite variables with passed arguments	
		for key in kwargs:
			exec ('self.%s = kwargs[key]' % key)
		
		# Group the variables
		self.params_dSs = [self.mu_dSs, self.sigma_dSs]
		self.params_Ss0 = [self.mu_Ss0, self.sigma_Ss0]
		self.params_Kk1 = [self.mu_Kk1, self.sigma_Kk1]
		self.params_Kk2 = [self.mu_Kk2, self.sigma_Kk2]
		self.params_eps = [self.mu_eps, self.sigma_eps]
		
	
	def set_signals(self):
		self.dSs, self.idxs = sparse_vector([self.Nn, self.Kk], 
											self.params_dSs, 
											seed = self.seed_dSs)
		
		# Ss0 is the ideal (learned) background stimulus without noise
		self.Ss0, self.Ss0_noisy = sparse_vector_bkgrnd([self.Nn, self.Kk], 
														self.idxs, 
														self.params_Ss0, 
														seed = self.seed_Ss0)
		
		# The true signal, including background noise
		self.Ss = self.dSs + self.Ss0_noisy
	
	def set_adapted_free_energy(self):
		# Set free energy based on adapted activity activity
		self.eps = free_energy(self.Ss0, self.Kk1, self.Kk2, self.activity)
		
	def set_random_free_energy(self):
		# Free energy as random vector if assigned as such
		self.eps = random_matrix([self.Mm], self.params_eps, 
									seed = self.seed_eps)

	def set_gaussian_Kk(self):	
		"""
		Define class object numpy array of Kk1 and Kk2 atrix, given 
		prescribed Gaussian statistics.
		"""
		
		self.Kk1 = random_matrix([self.Mm,self.Nn], 
									self.params_Kk1, 
									seed = self.seed_Kk1)
		self.Kk2 = random_matrix([self.Mm,self.Nn], 
									self.params_Kk2, 
									seed = self.seed_Kk2)
	
	def set_Kk2_Gaussian_activity(self):
		"""
		Define numpy array of Kk2 matrix, given prescribed monomolecular 
		tuning curve statistics, and Kk1 matrix from a Gaussian	prior.
		"""
		
		self.receptor_activity_mus = random_matrix([self.Mm], 
										params=self.receptor_tuning_center,
										type='normal', 
										seed = self.seed_receptor_activity)
		self.receptor_activity_sigmas = random_matrix([self.Mm], 
										params=self.receptor_tuning_range,
										type='uniform', 
										seed = self.seed_receptor_activity)
		self.Kk2 = Kk2_samples([self.Mm, self.Nn], self.receptor_activity_mus,
								self.receptor_activity_sigmas, self.mu_Ss0, 
								self.mu_eps, self.seed_Kk2)
		
		self.Kk1 = random_matrix([self.Mm,self.Nn], self.params_Kk1, 
									seed = self.seed_Kk1)
		
		
		
	def set_measured_activity(self):
		# True receptor activity
		self.Yy = receptor_activity(self.Ss, self.Kk1, self.Kk2, self.eps)
		
		# Learned background activity only utilizes average background signal 
		self.Yy0 = bkgrnd_activity(self.Ss0, self.Kk1, self.Kk2, self.eps)
		
		# Measured response above background
		self.dYy = self.Yy - self.Yy0

	def set_linearized_response(self):
		# Linearized response can only use the learned background
		self.Rr = linear_gain(self.Ss0, self.Kk1, self.Kk2, self.eps)
		
	def encode(self):
		self.set_signals()
		self.set_gaussian_Kk()
		self.set_random_free_energy()
		self.set_measured_activity()
		self.set_linearized_response()
		
	def decode(self):
		self.dSs_est = decode_CS(self.Rr, self.dYy)	
