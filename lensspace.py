"""
lens_space.py

Class for lens spacing in thin lens calculator.

Niko Romer
1/27/2022

"""
import numpy as np 


class space:
	def __init__(self, thickness):
		self.thickness = thickness
		self.index = 1
		self.matrix = np.matrix([[1, self.thickness/float(self.index)], [0, 1]])

	def get_matrix(self):
		return self.matrix