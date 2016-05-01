import math
import numpy as np




class IndexerInvertedList(object):

	def __init__(self):
		self.path_write = ""
		self.paths_reads = []
		self.terms = []
		self.terms_documents = []
		self.terms_number = None
		self.documents_number = None
		self.tf = []
		self.idf = []
		self.tf_idf = []

	#Reading the config file for get the paths of files
	def get_paths_files(self, files_list):
		
		files = open(files_list, 'r')
		
		for line in files.readlines():
			
			splited = line.split('=')

			if len(splited) != 2:
				print ("ERRO de leitura!!!!")

			command	= splited[0]
			path = splited[1].replace('\n','')

			if command == "LEIA":
				self.paths_reads.append(path)
			elif command == "ESCREVA":
				self.path_write = path
			else:
				print("Erro no commando")

		if len(self.paths_reads) == 0:
			print("Não tem comandos de LEIA!!!!")

		if len(self.path_write) == 0:
			print("Não tem comando de ESCREVA!!!")		

		files.close()

	#Recovering the quantity of terms and documents, and create the terms documents matrix
	def create_matrices(self, line):


		splited = line.split(";")

		quantities = splited[1][1:-2].split(",")

		self.terms_number = int(quantities[0])
		self.documents_number = int(quantities[1])

		self.terms_documents = np.zeros((self.terms_number, self.documents_number)) #term-document matrix

		self.tf =  np.zeros((self.terms_number, self.documents_number)) #tf matrix

		self.idf = np.zeros((self.terms_number, 1)) #idf list 

	#Reading csv file that content the inverted list and create matrices
	def read_csv_file(self, csv_file_path):

		csv_file = open(csv_file_path, 'r')

		self.create_matrices(csv_file.readline())

		for line in csv_file.readlines():

			splited = line.split(";")

			self.terms.append(splited[0])

			term_index = self.terms.index(splited[0])

			documents = splited[1][1:-2].split(",")

			self.idf[term_index] = math.log(self.documents_number/len(documents))

			
			for dci in documents:
				self.terms_documents[term_index, (int(dci)-1)] += 1 #Filling the matrix with frequency of terms in documents
				self.tf[term_index, (int(dci)-1)] = 1 + math.log(self.terms_documents[term_index, (int(dci)-1)]) #Filling the tf matrix


		print(self.tf[9][499])
		print(self.idf[9])		


		
i = IndexerInvertedList()
i.get_paths_files("INDEX.CFG")
i.read_csv_file('data/inverted_list.csv')





















