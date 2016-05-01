from lxml import etree	
from nltk import word_tokenize
import re
import unicodedata




class GeneratorInvertedList(object):

	def __init__(self):
		self.path_write = ""
		self.paths_reads = []
		self.inverted_list = {}
		self.document_id = None
		self.tokens = []
		self.no_stopwords_tokens = []
		self.documents_number = 0
		self.terms_number = 0


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
			if len(token) > 2 and self.contains_number(token) is False:
				no_stopwords.append(token)
			else: 
				pass

		return no_stopwords

	def insert_inverted_list(self, document_id, tokens):

		for token in tokens:
			if not token in self.inverted_list:
				self.inverted_list[token] = []
				self.terms_number +=  1
			self.inverted_list[token].append(document_id)	

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

	def generate_csv(self, inverted_list):

		inverted_list_cvs = []

		inverted_list_cvs.append("TOTAL;[" + str(self.terms_number) + "," + str(self.documents_number) + "]")

		for token , document_list in self.inverted_list.items():
			inverted_list_cvs.append(str(token) + ";" + str(document_list))

		return "\n".join(inverted_list_cvs)


	def write_csv(self):

		out_csv = open(self.path_write, "w")
		out_csv.write(self.generate_csv(self.inverted_list))
		out_csv.close()

	def read_xmls(self):

		for file in self.paths_reads:
			for event, element in etree.iterparse(file, tag=["RECORDNUM","ABSTRACT","EXTRACT"]):

			    if element.tag == "RECORDNUM":
			    
			        self.document_id = int(element.text)
			        self.documents_number += 1

			    if element.tag == "ABSTRACT":
			    
			    	tokens = self.tokenize_text(element.text)
			    	self.no_stopwords_tokens = self.remove_stopwords(tokens)
			    	self.insert_inverted_list(self.document_id, self.no_stopwords_tokens)
			    	
			    if element.tag == "EXTRACT":    
			    	tokens = self.tokenize_text(element.text)
			    	self.no_stopwords_tokens = self.remove_stopwords(tokens)
			    	self.insert_inverted_list(self.document_id, self.no_stopwords_tokens)