"""
Simple tests and data generation.
"""

from ATE import Samplerun, Parameter
import os

def test_samplerun():
	"""
	Sets up uniform geemeration of data points and csv output.
	"""

	numsamples = 100
	
	run1 = Samplerun(numsamples)
	run1.setup_model()
	run1.perform_sample(savefile="100uniform.csv")
		
	

if __name__== "__main__":
	test_samplerun()

