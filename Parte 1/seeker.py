from pickle import dump, load
from sklearn.feature_extraction.text import TfidfVectorizer	
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np

class Seeker(object):

	def __init__(self, model, cfg_file):
		self.cfg_file = cfg_file
		self.model_type = model
		self.model_path = ""
		self.queries_path = ""
		self.result_path = ""
		self.queries = {}
		self.query_ids = []
		self.term_document = None
		self.content = None
		self.document_id = []
		self.queries_matrix = None 
		self.distance_matrix = None
		self.ranking = None


	def get_paths_files(self):

		print("Seeker - Lendo arquivo de comfiguração:",self.cfg_file, "..." )
		files = open(self.cfg_file, 'r')
		
		for line in files.readlines():
			
			splited = line.split('=')

			if len(splited) != 2:
				print ("ERRO de leitura!!!!")

			command	= splited[0]
			path = splited[1].replace('\n','')

			if command == "MODELO":
				self.model_path = path
			elif command == "CONSULTAS":
				self.queries_path = path
			elif command == "RESULTADO":
				self.result_path = path
			else:
				print("Erro no commando")

		if len(self.model_path) == 0:
			print("Não tem comandos de MODEL!!!!")

		if len(self.queries_path) == 0:
			print("Não tem comando de CONSULTAS!!!")		

		if len(self.result_path) == 0:
			print("Não tem comando de RESULTADO!!!")		
	
		files.close()


	def read_model(self):

		print("Seeker - Carregando o modelo em memória..." )
		
		model_file = open(self.model_path, "rb")
		data = load(model_file)

		self.term_document = data["matrix"]
		self.content = data["contents"]

		self.document_id.extend(self.content.keys())


	def write_csv(self):

		print("Seeker - Escrevendo arquivo contendo os resultados na extensão csv...")

		with open(self.result_path, "w") as results_file:
			results_file.write(self.generate_csv())


	def read_queries(self):

		print("Seeker - Carregando consultas em memória...")

		queries_file = open(self.queries_path, 'r')

		for line in queries_file.readlines():

			splited = line.split(";")

			query_id = splited[0]
			query_text = splited[1]

			self.queries[query_id] = query_text


		self.query_ids.extend(self.queries.keys())

		queries_file.close()

	def generate_queries_matrix(self):

		print("Seeker - Gerando a matriz de queries...")
		
		typ_model = self.model_type(ngram_range=(1,1))
		typ_model.fit(self.content.values())
		self.queries_matrix = typ_model.transform(self.queries.values())


	def retrieval(self):
		
		print("Seeker - Calculando a distância...")
		self.distance_matrix = pairwise_distances(self.queries_matrix, self.term_document, metric="cosine", n_jobs=4)
		print("Seeer - Fazendo o rankeamento...")
		self.ranking = np.argsort(self.distance_matrix, axis=1)


	def generate_csv(self):

		print("Seeker - Gerando o arquivo de saída .csv...")

		lines = []

		for i in range(self.ranking.shape[0]):
			query_id = self.query_ids[i]
			query_results = []
			for j in range(self.ranking.shape[1]):
				ranking = j
				document_index = self.ranking[i][j]
				document_id = self.document_id[document_index]
				distance = self.distance_matrix[i][document_index]

				query_results.append( (ranking, document_id, distance) )

			lines.append( str(query_id) + ";" + str(query_results) )

		return  "\n".join(lines)


	def execute(self):
		
		self.get_paths_files()
		self.read_queries()
		self.read_model()
		self.generate_queries_matrix()
		self.retrieval()
		self.write_csv()	
		