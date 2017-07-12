# Using Word Mover's Distance
# Paper citations:
# 1) .. Ofir Pele and Michael Werman, "A linear time histogram metric for
#			improved SIFT matching".
# 2) .. Ofir Pele and Michael Werman, "Fast and robust earth mover's
#			distances".
# 3) .. Matt Kusner et al. "From Word Embeddings To Document Distances".

from gensim.models.word2vec import Word2Vec
from extract_data import articles

try:
	model = Word2Vec.load('./model_word2vec')
	print 'Loaded existing model'
	model.build_vocab(articles(), update=True)
except IOError:
	model = Word2Vec(size=300, alpha=0.1, window=10, min_count=0, workers=8,
		min_alpha=0.01)
	print 'Created new model'
	model.build_vocab(articles())

print "Training..."
model.train(articles(), total_examples=model.corpus_count, epochs=250)
print "Trained"

model.save('/home/rharish/Programs/Python/Articles/model_word2vec')
print "Model saved\nExporting data to disk..."

wordvec_file = open('embeddings.tsv', 'w')
metadata_file = open('metadata.tsv', 'w')
words = model.wv.vocab.keys()
for word in words:
	metadata_file.write(word.encode('utf-8'))
	try:
		vector = model.wv[word]
	except:
		continue
	for i, value in enumerate(vector):
		wordvec_file.write(str(value))
		if i != (len(vector) - 1):
			wordvec_file.write('\t')
	wordvec_file.write('\n')
	metadata_file.write('\n')
print "Exported data"
wordvec_file.close()
metadata_file.close()
