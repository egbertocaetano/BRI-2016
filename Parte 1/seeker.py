from pickle import dump, load
from pprint import pformat
from sklearn.feature_extraction.text import TfidfVectorizer	


class Seeker(object):

	def __init__(self, cfg_file, model):
		self.cfg_file = cfg_file
		self.model_type = model
		self.model_path = ""
		self.queries_path = ""
		self.result_path = ""
		self.queries = {}
		self.term_document = None
		self.content = None
		self.queries_matrix = None 
	
	def get_paths_files(self):

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
		
		model_file = open(self.model_path, "rb")
		data = load(model_file)

		self.term_document = data["matrix"]
		self.content = data["contents"]


	def read_queries(self):

		queries_file = open(self.queries_path, 'r')

		for line in queries_file.readlines():

			splited = line.split(";")

			query_id = splited[0]
			query_text = splited[1]

			self.queries[query_id] = query_text


		queries_file.close()

	def generate_queries_matrix(self):
		
		typ_model = self.model_type(ngram_range=(1,1))
		typ_model.fit(self.content.values())
		self.queries_matrix = typ_model.transform(self.queries.values())


s = Seeker("BUSCA.CFG", TfidfVectorizer)
s.get_paths_files()
s.read_queries()
s.read_model()
s.generate_queries_matrix()
