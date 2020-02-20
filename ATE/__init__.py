import math
import numpy as np
import matplotlib.pyplot as plt
import requests 
import json
import csv
import subprocess
import os

from .file import CSVFile
from .param import Parameter


class Samplerun:
	'''
	Holds sampling methods and data for TBR docker run.
	'''
	def __init__(self, numsamples):
		'''
		Collects sampling parameters
		'''
		assert (numsamples > 0), "Input error, nonpositive number of samples."
		self.numsamples = numsamples
		self.params = []
		self.paramvalues = np.matrix([])
		self.tbr = []

	def setup_model(self):
		'''
		Generates array of input parameters for model in use.
		'''
		FWT  = Parameter('firstwall_thickness',      		valuerange=[0,20])
		FWAM = Parameter('firstwall_amour_material', 		values=['tungsten'])
		FWSM = Parameter('firstwall_structural_material', 	values=['SiC', 'eurofer'])
		FWCM = Parameter('firstwall_coolant_material]',		values=['H2O', 'He', 'D2O'])
		BSM = Parameter('blanket_structural_material',		values=['SiC', 'eurofer'])
		BBM = Parameter('blanket_breeder_material ',		values=['Li4SiO4', 'Li2TiO3'])
		BMM = Parameter('blanket_multiplier_material',		values=['Be', 'Be12Ti'])
		BCM = Parameter('blanket_coolant_material',			values=['H2O', 'He', 'D2O'])
		BBEF = Parameter('blanket_breeder_li6_enrichment_fraction', 	valuerange=[0,1])
		BBPF = Parameter('blanket_breeder_packing_fraction', 			valuerange=[0,1])
		BMPF = Parameter('blanket_multiplier_packing_fraction', 		valuerange=[0,1]) 
		BMF = Parameter('blanket_multiplier_fraction', 					valuerange=[0,1]) 
		BBF = Parameter('blanket_breeder_fraction', 					valuerange=[0,1])
		BSF = Parameter('blanket_structural_fraction', 					valuerange=[0,1])
		# BCF = 1 - BMF - BBF - BSF (blanket_coolant_fraction)
		
		self.params = [FWT,FWAM,FWSM,FWCM,BSM,BBM,BMM,BCM,BBEF,BBPF,BMPF,BMF,BBF,BSF]
		self.numparams = len(self.params)
		
		
			
	
	def perform_sample(self, savefile="default.csv", verb=True):
		'''
		Interfaces with Docker to perform sample and saves to csv file
		'''
		savedir = "ATE/tests/output/"
		savefile = savedir + savefile
		self.paramvalues = np.matrix([param.gen_uniform(self.numsamples) for param in self.params])
		
		dockerchk = subprocess.Popen(['docker','ps'], stdout=subprocess.PIPE)
		dockerlist = dockerchk.communicate()
		if "openmcworkshop/find-tbr" not in str(dockerlist):
			os.system("docker run -p 8080:8080 -i openmcworkshop/find-tbr > /dev/null 2>&1 &")
			if verb: print("Starting openmcworkshop/find-tbr docker container")
		else:
			if verb: print("openmcworkshop/find-tbr docker container already running")
			
		output = []
		for i in range(self.numsamples):
			print("Performing sample " + str(i+1) + " of " + str(self.numsamples))
			runinput = self.paramvalues[:,i]
			
			reqstr = "http://localhost:8080/find_tbr_model_sphere_with_firstwall?"
			for j in range(self.numparams):	
				reqstr += self.params[j].name + "=" + runinput.item(j) + "&"
			
			#print(reqstr)
			r = requests.get(reqstr)
			output += [json.loads(r.text)]		#Forms a list of dictionaries
			if verb: print(output[i]['tbr'])
			
		with open(savefile, 'w', encoding='utf8', newline='') as output_file:
			dict_writer = csv.DictWriter(output_file, fieldnames=output[0].keys())
			dict_writer.writeheader()
			dict_writer.writerows(output)
			
			
		

				
			
		
		
