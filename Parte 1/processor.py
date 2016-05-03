from lxml import etree	
from nltk import word_tokenize
import re
import unicodedata



class Processor(object):


	def __init__ (self, cfg_file):

		self.cfg_file = cfg_file
		self.read_paths = []
		self.queries_path = ""
		self.expecteds_path = ""
		self.query_id = None
		self.query_text = ""
		self.no_stopwords_tokens =[]
		self.queries = {}


	def tokenize_text(self, text):
		return word_tokenize(unicodedata.normalize('NFKD', text).encode('ascii','ignore').upper().decode('utf-8'))

	def remove_stopwords(self,tokens):

		no_stopwords = set()

		for token in tokens:
			if len(token) > 1:
				no_stopwords.add(token)
			else: 
				pass

		return " ".join(no_stopwords)
	

	def get_paths_files(self):

		files = open(self.cfg_file, 'r')
		
		for line in files.readlines():
			
			splited = line.split('=')

			if len(splited) != 2:
				print ("ERRO de leitura!!!!")

			command	= splited[0]
			path = splited[1].replace('\n','')

			if command == "LEIA":
				self.read_paths.append(path)
			elif command == "CONSULTAS":
				self.queries_path = path
			elif command == "ESPERADOS":
				self.expecteds_path = path
			else:
				print("Erro no commando")

		if len(self.read_paths) == 0:
			print("Não tem comandos de LEIA!!!!")

		if len(self.queries_path) == 0:
			print("Não tem comando de CONSULTAS!!!")		

		if len(self.expecteds_path) == 0:
			print("Não tem comando de ESPERADOS!!!")		
	
		files.close()

	#Write files on espcified path	
	def write_csv(self):
		queries_csv, expecteds_csv = self.generate_csv()

		queries_out = open(self.queries_path, "w")
		queries_out.write(queries_csv)
		queries_out.close()

		expected_out = open(self.expecteds_path, "w")
		expected_out.write(expecteds_csv)	
		expected_out.close()

	#Load e read data from especified xml	
	def read_xmls(self):

		for file in self.read_paths:
			for event, element in etree.iterparse(file, tag=["QueryNumber","QueryText","Item"]):

			    if element.tag == "QueryNumber":
			    
			        self.query_id = int(element.text)
			        self.queries[self.query_id] = {}
			        self.queries[self.query_id]["query"] = ""
			        self.queries[self.query_id]["expecteds"] = [] 
			       
			    if element.tag == "QueryText":
			    
			    	query_text = self.tokenize_text(element.text)
			    	self.no_stopwords_tokens = self.remove_stopwords(query_text)
			    	self.query_text = self.no_stopwords_tokens
			    	self.queries[self.query_id]['query'] = self.query_text
			    	
			    if element.tag == "Item":    
			    	doc_id = int(element.text)
			    	score = int(element.attrib.values()[0])
			    	self.queries[self.query_id]["expecteds"].append((doc_id,score))

	def generate_csv(self):

		queries_lines = []
		expecteds_lines = []

		for qid, query_attr in self.queries.items():
			queries_lines.append( str(qid) + ";" + str(query_attr['query']) )
			expecteds_lines.append( str(qid) + ";" + str(query_attr['expecteds']) )

		return "\n".join(queries_lines), "\n".join(expecteds_lines)	    	

p = Processor("PC.CFG")
p.get_paths_files()
p.read_xmls()
p.write_csv()