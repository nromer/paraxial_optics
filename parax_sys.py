"""
paraxial_system.py

Class for creating a paraxial optical system.

Niko Romer
1/27/2022

Edits
1/27/22: For now, all lenses are in air.

"""

import numpy as np
import pandas as pd  
import thinlens as tl 
import lensspace as sp 


class parax_sys:

	def __init__(self):
		self.name = ""
		self.elements = []
		self.object_dis = 0
		self.system_matrix = np.matrix([[1,0],[0,1]]) #ABCD Matrix - initialize as identity
		self.stop_surface = 0
		self.air = True

		if self.air:
			self.index = 1
		else:
			self.index = 1	# Refractive index that OS is immersed in

		self.A = 0
		self.B = 0
		self.C = 0
		self.D = 0

	def add_lens(self, power):
		"""
			Add a thin lens to the system.
			:param float power: Thin lens power
			:return: None
	   """
		len = tl.lens(power)
		self.elements.append(len)
		self.update_sys_mat()

	def add_mirror(self,power):
		"""
			Add a reflective element to the optical system. To be implemented in the future (NGR 1/28/22).
			:param: None
			:return: None
		"""
		return

	def add_space(self, thickness):
		"""
			Add a lens spacing to the optical system.
			:param: None
			:return: None
		"""
		space = sp.space(thickness)
		self.elements.append(space)
		self.update_sys_mat()

	def set_stop(self, surface_no):
		"""
			Set the stop to be at a certain surface #. Must be a lens. 
			:param: None
			:return: None
		"""
		self.stop_surface = surface_no
		self.update_sys_mat()

	def get_system_matrix(self):
		"""
			Return the system ABCD matrix.
			:param: None
			:return: np.matrix object, system matrix
		"""
		return self.system_matrix

	def update_sys_mat(self):
		"""
			Recalculate the system ABCD matrix.
			:param: None
			:return: None
		"""
		elts = self.elements
		
		if len(elts) == 0:
			self.system_matrix = np.matrix([[1,0],[0,1]]) # Identity Matrix
		else:
			mat = np.matrix([[1,0],[0,1]]) # Identity Matrix
			# mat = self.system_matrix
				# print(mat)
			for i in elts:#[::-1]:
				# if(len(elts) == 3):
				# 	print(mat)
				temp = i.get_matrix()
				mat = np.matmul(mat,temp)
				# if(len(elts) ==3):
				# 	print(i)
				# 	print("temp:\n"+str(temp))
				# 	print(mat)

			self.system_matrix = mat
		
		self.A = self.system_matrix[0,0]
		self.B = self.system_matrix[0,1]
		self.C = self.system_matrix[1,0]
		self.D = self.system_matrix[1,1]

	def get_sys_power(self):
		"""
			Calculate total system power
			:param: None
			:return: float, system power
		"""
		return -self.system_matrix[1,0]

	def rprincpl(self):
		"""
			Calculate rear principal plane location
			:param: None
			:return: float, rear principal plane location from last lens
		"""
		return self.index*(1-self.A)/self.C
	def fprincpl(self):
		"""
			Calculate front principal plane location.
			:param: None
			:return: float, front principal plane location from first lens
		"""
		return self.index*(self.D-1)/self.C
	
	def ffocalpl(self):
		"""
			Calculate front focal plane location.
			:param: None
			:return: float, front focal plane location from first lens
		"""
		return self.index*self.D/self.C
	def rfocalpl(self):	
		"""
			Calculate rear focal plane location.
			:param: None
			:return: float, rear focal plane location from last lens
		"""
		return -self.index*self.A/self.C
	
	def fnodalpl(self):
		"""
			Calculate front nodal plane location.
			:param: None
			:return: float, front nodal plane location from first lens
		"""
		return (self.index*self.D-self.index)/self.C
	def rnodalpl(self):
		"""
			Calculate rear nodal plane location.
			:param: None
			:return: float, rear nodal plane location from last lens
		"""
		return (self.index-self.index*self.A)/self.C

	def cardinal_pts(self):
		"""
			Calculate all the cardinal points and store then in a pandas dataframe.
			:param: None
			:return: pd.Dataframe, cpts
		"""
		fpp = self.fprincpl()
		rpp = self.rprincpl()
		ffp = self.ffocalpl()
		rfp = self.rfocalpl()
		fnp = self.fnodalpl()
		rnp = self.rnodalpl()

		cpts = pd.DataFrame(data={'fpp':fpp,'rpp':rpp,'ffp':ffp,'rfp':rfp,'fnp':fnp,'rnp':rnp},index = [0])
		return cpts


	def system_report(self):
		"""
			Generate a summary of the system that has been added that include the total power, 
			the system ABCD matrix, and the locations of the Cardinal points.
			:param: None
			:return: string, rpt
		"""
		title = "\nParaxial Optical System: "+ self.name+" \n"
		cols = "\nno. type pwr/thi\n=============="
		els = ""
		for j in range(len(self.elements)):
			if isinstance(self.elements[j],tl.lens):
				els = els + "\n" + str(j) + " Lens " + str(self.elements[j].power)
			elif isinstance(self.elements[j],sp.space):
				els = els + "\n" + str(j) + " Space " + str(self.elements[j].thickness)

		matrix = str(self.system_matrix)
		cpts = self.cardinal_pts()

		rpt = title + cols + els + "\n\nSystem Matrix\n==============\n" + matrix + "\n\nCardinal Points\n==============\n" + str(cpts)
		# print(rpt)
		return rpt




def main():
	"""
	ADD YOUR THIN LENSES AND SPACINGS HERE

	"""

	e = 1
	f1 = 1.5*e
	f2 = f1

	new_sys = parax_sys()
	new_sys.name = "Ramsden 323 Eyepiece, e = 1"
	new_sys.add_lens(1/f1)
	new_sys.add_space(e)
	new_sys.add_lens(1/f2)
	print(new_sys.system_report())

if __name__ == "__main__":
    main()