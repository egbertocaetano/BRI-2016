from lxml import etree
from nltk.corpus import stopwords	
from nltk import word_tokenize
import re
import unicodedata
import pprint


invert_list = {}

def tokenize_text(text):
	return word_tokenize(unicodedata.normalize('NFKD', text).encode('ascii','ignore').upper().decode('utf-8'))


def contains_number(token):
	p = re.compile('\d+')

	if p.findall(token) != []:
		return True
	else:
		return False		


def remove_stopwords(tokens):

	no_stopwords = []

	for token in tokens:
		if (len(token) > 2) and (contains_number(token) is False):
			no_stopwords.append(token)
		else: 
			pass

	return no_stopwords

def insert_invert_list(document_id, tokens):

	for token in tokens:
		if not token in invert_list:
			invert_list[token] = []
		invert_list[token].append(document_id)	


for event, element in etree.iterparse("cf74.xml", tag=["RECORDNUM","ABSTRACT","EXTRACT"]):
    if element.tag == "RECORDNUM":
    
        document_id = element.text
    
    if element.tag == "ABSTRACT":
    
    	tokens = tokenize_text(element.text)
    	no_stopwords_tokens = remove_stopwords(tokens)
    	insert_invert_list(document_id, no_stopwords_tokens)
    	
    elif element.tag == "EXTRACT":    
        
        tokens = tokenize_text(element.text)
    	no_stopwords_tokens = remove_stopwords(tokens)
    	insert_invert_list(document_id, no_stopwords_tokens)
   