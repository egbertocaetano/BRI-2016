import generator_inverted_list as gil
import indexer as idx
import seeker as skr
import processor as proc
from sklearn.feature_extraction.text import TfidfVectorizer
import time

print("Iniciando Sistema de Recuperação em Memória.")


print("\nIniciando Gerador de Lista Invertida...")
time_start = time.clock()
generator = gil.GeneratorInvertedList("GLI.CFG")
generator.execute()
time_end = time.clock()
print("Finalizando Gerador de Lista Invertida...")
print("===========================================Tempo em segundos da Execução do Gerador: ", (time_end - time_start))

print("\nIniciando Indexador...")
time_start = time.clock()
indexer = idx.IndexerInvertedList(TfidfVectorizer,"INDEX.CFG")
indexer.execute()
time_end = time.clock()
print("Finalizando Indexador...")
print("===========================================Tempo em segundos da Execução do Indexador: ", (time_end - time_start))

print("\nIniciando Processador...")
time_start
processor = proc.Processor("PC.CFG")
processor.execute()
time_end = time.clock()
print("Finalizando Processador...")
print("===========================================Tempo em segundos da Execução do Processador: ", (time_end - time_start))

print("\nIniciando Buscador...")
time_start = time.clock()
seeker = skr.Seeker(TfidfVectorizer,"BUSCA.CFG")
seeker.execute()
time_end = time.clock()
print("Finalizando Buscador...")
print("===========================================Tempo em segundos da Execução do Buscador: ", (time_end - time_start))

