import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from pickle import dump
import logging

logging.basicConfig(format='[%(levelname)s %(asctime)s %(name)s]\t%(message)s',filename='application.log',level=logging.INFO)

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
		self.logger = logging.getLogger(__name__)

	#Reading the config file for get the paths of files
	def get_paths_files(self):
		
		self.logger.info("Indexer Inverted List - Lendo arquivo de configuração:" + self.cfg_file + "...")

		files = open(self.cfg_file, 'r')
		
		for line in files.readlines():
			
			splited = line.split('=')

			if len(splited) != 2:
				self.logger.error("ERRO de leitura!!!!")

			command	= splited[0]
			path = splited[1].replace('\n','')

			if command == "LEIA":
				self.paths_reads.append(path)
			elif command == "ESCREVA":
				self.path_write = path
			else:
				self.logger.error("Erro no commando")

		if len(self.paths_reads) == 0:
			self.logger.error("Não tem comandos de LEIA!!!!")

		if len(self.path_write) == 0:
			self.logger.error("Não tem comando de ESCREVA!!!")		

		files.close()

	def create_term_document(self):

		self.logger.info("Indexer Inverted List - Gerando modelo...")

		mod = self.model_type(ngram_range=(1,1))
		self.terms_documents = mod.fit_transform(self.contents.values())

	#Reading csv file that content the inverted list and create term documents frenquecy matrix
	def read_csv_file(self):

		self.logger.info("Indexer Inverted List - Lendo Lista Invertida...")

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
		self.logger.info("Indexer Inverted List - Escrevendo modelo...")
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
		






















