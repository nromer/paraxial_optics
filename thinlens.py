"""
thinlens.py

Class adding thin lenses to paraxial optics calculator.

Niko Romer
1/27/2022

"""
import numpy as np 


class lens:
	def __init__(self, power):
		self.power = power
		self.matrix = np.matrix([[1, 0], [-self.power, 1]])

	def get_matrix(self):
		return self.matrix

	



