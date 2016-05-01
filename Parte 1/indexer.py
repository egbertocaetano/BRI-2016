import numpy as np



class IndexerInvertedList(object):

	def __init__(self):
		self.path_write = ""
		self.paths_reads = []
		self.terms = []
		self.terms_documents = []
		self.terms_number = None
		self.documents_number = None

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

	#Recorving the quantity of terms and documents	
	def get_border(self, line):


		splited = line.split(";")

		quantities = splited[1][1:-2].split(",")

		self.terms_number = int(quantities[0])
		self.documents_number = int(quantities[1])


	#Reading csv file that content the inverted list	
	def read_csv_file(self, csv_file_path):

		csv_file = open(csv_file_path, 'r')

		self.get_border(csv_file.readline())

		for line in csv_file.readlines():

			splited = line.split(";")

			self.terms.append
			


		
i = IndexerInvertedList()
i.get_paths_files("INDEX.CFG")
i.read_csv_file('data/inverted_list.csv')





















