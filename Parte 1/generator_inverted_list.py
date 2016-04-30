from lxml import etree	
from nltk import word_tokenize
import re
import unicodedata


path_write = []
paths_reads = []
inverted_list = {}
document_id = ""
tokens = []
no_stopwords_tokens = []


def tokenize_text(text):
	return word_tokenize(unicodedata.normalize('NFKD', text).encode('ascii','ignore').upper().decode('utf-8'))


def contains_number(token):
	p = re.compile('\d+')

	if p.findall(token) == []:
		return False
	else:
		return True		

#Removendo palavras de acordo com o que foi específicado nas instruções descritas no Indexador 2.d
def remove_stopwords(tokens):

	no_stopwords = []

	for token in tokens:
		if len(token) > 2 and contains_number(token) is False:
			no_stopwords.append(token)
		else: 
			pass

	return no_stopwords

def insert_inverted_list(document_id, tokens):

	for token in tokens:
		if not token in inverted_list:
			inverted_list[token] = []
		inverted_list[token].append(document_id)	


def get_paths_files(files_list):
	
	files = open(files_list, 'r')
	
	for line in files.readlines():
		
		splited = line.split('=')

		if len(splited) != 2:
			print ("ERRO de leitura!!!!")

		command	= splited[0]
		path = splited[1].replace('\n','')


		if command == "LEIA":
			paths_reads.append(path)
		elif command == "ESCREVA":
			path_write.append(path)
		else:
			print("Erro no commando")

	if len(paths_reads) == 0:
		print("Não tem comandos de LEIA!!!!")

	if len(path_write) == 0:
		print("Não tem comando de ESCREVA!!!")		

	files.close()

def generate_csv(inverted_list):

	inverted_list_cvs = []

	for token , document_list in inverted_list.items():
		inverted_list_cvs.append(str(token) + ';' + str(document_list))


	return "\n".join(inverted_list_cvs)


def write_csv():

	out_csv = open(path_write[0], "w")
	out_csv.write(generate_csv(inverted_list))
	out_csv.close()

def read_xmls():


	for file in paths_reads:
		for event, element in etree.iterparse(file, tag=["RECORDNUM","ABSTRACT","EXTRACT"]):

		    if element.tag == "RECORDNUM":
		    
		        document_id = element.text
		    
		    if element.tag == "ABSTRACT":
		    
		    	tokens = tokenize_text(element.text)
		    	no_stopwords_tokens = remove_stopwords(tokens)
		    	insert_inverted_list(document_id, no_stopwords_tokens)
		    	
		    if element.tag == "EXTRACT":    
		    	tokens = tokenize_text(element.text)
		    	no_stopwords_tokens = remove_stopwords(tokens)
		    	insert_inverted_list(document_id, no_stopwords_tokens)


get_paths_files("GLI.CFG")
read_xmls()
write_csv()