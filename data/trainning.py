#Trainning


def tokenize(document_content):
    return document_content.lower().split(' ')




documents = ["Human machine interface for Lab ABC computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user-perceived response time to error measurement"]


tokenized_documents = [ tokenize(di) for di in documents]
print(tokenized_documents)


stop_words = ("a", "about", "above", "across", "after", "of", "the", "in", "an", "or")
no_stop_documents = []

for documenti in tokenized_documents:
    no_stop_doci = []
    for tokenj in documenti:
        if tokenj not in stop_words: # tokenj is a stop word?
            no_stop_doci.append(tokenj)
    no_stop_documents.append(no_stop_doci)
    
print(no_stop_documents)

vocabulary = {}

for documenti in no_stop_documents:
    for tokenj in documenti:
            vocabulary[tokenj] = 1           
print(vocabulary)

inverted_index = {}
for wordi in vocabulary.keys():
    inverted_index[wordi] = []
    for i in range(0,len(no_stop_documents)):
        if wordi in no_stop_documents[i]:
            inverted_index[wordi].append(i)
            
from pprint import pprint
pprint(inverted_index)

q = "survey of computer system or computer applications"

q_tokens = tokenize(q)
print("query tokenized:",q_tokens)


