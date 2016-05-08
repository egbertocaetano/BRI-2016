from lxml import etree	
from nltk import word_tokenize
import re
import unicodedata




class GeneratorInvertedList(object):

	def __init__(self, cfg_file):
		self.cfg_file = cfg_file
		self.write_path = ""
		self.read_paths = []
		self.inverted_list = {}
		self.document_id = None
		self.no_stopwords_tokens = []
		self.inverted_list_csv = None


	def tokenize_text(self, text):
		return word_tokenize(unicodedata.normalize('NFKD', text).encode('ascii','ignore').upper().decode('utf-8'))


	def contains_number(self,token):
		p = re.compile('\d+')

		if p.findall(token) == []:
			return False
		else:
			return True		

	#Removendo palavras de acordo com o que foi específicado nas instruções descritas no Indexador 2.d
	def remove_stopwords(self,tokens):
		no_stopwords = []

		for token in tokens:
			if len(token) > 1 and self.contains_number(token) is False:
				no_stopwords.append(token)
			else: 
				pass

		return no_stopwords

	def insert_inverted_list(self, document_id, tokens):

		for token in tokens:
			if not token in self.inverted_list:
				self.inverted_list[token] = []
				#self.terms_number +=  1
			self.inverted_list[token].append(document_id)	

	def get_paths_files(self):
		
		print("Generator Inverted List - Lendo arquivo de configuração:", self.cfg_file,"...")

		files = open(self.cfg_file, 'r')
		
		for line in files.readlines():
			
			splited = line.split('=')

			if len(splited) != 2:
				print ("ERRO de leitura!!!!")

			command	= splited[0]
			path = splited[1].replace('\n','')

			if command == "LEIA":
				self.read_paths.append(path)
			elif command == "ESCREVA":
				self.write_path = path
			else:
				print("Erro no commando")

		if len(self.read_paths) == 0:
			print("Não tem comandos de LEIA!!!!")

		if len(self.write_path) == 0:
			print("Não tem comando de ESCREVA!!!")		

		files.close()

	def generate_csv(self, inverted_list):

		print("Generator Inverted List - Gerando o arquivo de saída .csv...")

		inverted_list_cvs = []

		for token , document_list in self.inverted_list.items():
			inverted_list_cvs.append(str(token) + ";" + str(document_list))

		self.inverted_list_cvs = "\n".join(inverted_list_cvs)


	def write_csv(self):

		print("Generator Inverted List - Escrevendo arquivo de saída contendo lista invertida na extensão csv...")
		out_csv = open(self.write_path, "w")
		out_csv.write(self.inverted_list_cvs)
		out_csv.close()

	def read_xmls(self):
		print("Generator Inverted List - Iniciando a leitura dos arquivos xmls e gerando a list invertida...")
		for file in self.read_paths:
			print("Generator Inverted List - Lendo o arquivo:",file)
			for event, element in etree.iterparse(file, tag=["RECORDNUM","ABSTRACT","EXTRACT"]):

			    if element.tag == "RECORDNUM":
			    
			        self.document_id = int(element.text)
			        #self.documents_number += 1

			    if element.tag == "ABSTRACT":
			    
			    	tokens = self.tokenize_text(element.text)
			    	self.no_stopwords_tokens = self.remove_stopwords(tokens)
			    	self.insert_inverted_list(self.document_id, self.no_stopwords_tokens)
			    	
			    if element.tag == "EXTRACT":    
			    	tokens = self.tokenize_text(element.text)
			    	self.no_stopwords_tokens = self.remove_stopwords(tokens)
			    	self.insert_inverted_list(self.document_id, self.no_stopwords_tokens)


	def execute(self):
		
		self.get_paths_files()
		self.read_xmls()
		self.generate_csv(self.inverted_list)
		self.write_csv()
		

