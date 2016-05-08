import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from pickle import dump


class IndexerInvertedList(object):

	def __init__(self, model, cfg_file):
		self.cfg_file = cfg_file
		self.path_write = ""
		self.paths_reads = []
		self.contents = {}
		self.model_type = model
		self.terms_documents = None
		self.tf = []
		self.idf = []
		self.tf_idf = []

	#Reading the config file for get the paths of files
	def get_paths_files(self):
		
		print("Indexer Inverted List - Lendo arquivo de configuração:", self.cfg_file,"...")

		files = open(self.cfg_file, 'r')
		
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

	def create_term_document(self):

		print("Indexer Inverted List - Gerando modelo...")

		mod = self.model_type(ngram_range=(1,1))
		self.terms_documents = mod.fit_transform(self.contents.values())

	#Reading csv file that content the inverted list and create term documents frenquecy matrix
	def read_csv_file(self):

		print("Indexer Inverted List - Lendo Lista Invertida...")

		for file in self.paths_reads:

			csv_file = open(file, 'r')

			for line in csv_file.readlines():

				splited = line.split(";")

				token = splited[0]
				documents = splited[1][1:-2].split(",")

				for did in documents:
					did = int(did)
					if did not in self.contents:
						self.contents[did] = ""

					self.contents[did] += token + " "

			csv_file.close()		

	def write_model(self):
		print("Indexer Inverted List - Escrevendo modelo...")
		export = {}
		export["matrix"] = self.terms_documents
		export["contents"] = self.contents
		with open(self.path_write, "wb") as file:
			dump(export, file)		
		
	def execute(self):
		
		self.get_paths_files()
		self.read_csv_file()
		self.create_term_document()
		self.write_model()	
		






















