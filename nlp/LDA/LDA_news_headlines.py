
import pandas as pd


###################################################################################
path_env = "/Users/gabrielpundrich/Dropbox/finance_accounting_data_science/mate/"
###################################################################################

path_env = path_env + "/NLP/LDA/"

data = pd.read_csv(path_env+'/data/abcnews-date-text.csv', error_bad_lines=False);
data_text = data[['headline_text']]
data_text['index'] = data_text.index

#restrict just to top 100
documents = data_text.head(1000)

len(documents)

documents[:5]


# ### Data Preprocessing
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)

import nltk
nltk.download('wordnet')


# #### Lemmatize example

print(WordNetLemmatizer().lemmatize('went', pos='v'))

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

###############################################################################
#Just to be used as an example, does not alter the file in any form
#Get a single observation: Check this Sam!
###############################################################################

# #### Stemmer Example
stemmer = SnowballStemmer('english')
original_words = ['caresses', 'flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned', 
           'humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational', 
           'traditional', 'reference', 'colonizer','plotted']
singles = [stemmer.stem(plural) for plural in original_words]
pd.DataFrame(data = {'original word': original_words, 'stemmed': singles})


#Lemmatize
documents.columns
doc_sample = documents[documents['index'] == 80].values[0][0]

print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))


###############################################################################


#Map all documents (lemmatize, stemmer)
processed_docs = documents['headline_text'].map(preprocess)
processed_docs[:10]



###############################################################################
# ### Create Dictionary based on Bag of words on the dataset
#less than no_below documents (absolute number) or
#more than no_above documents (fraction of total corpus size, not absolute number).
#after (1) and (2), keep only the first keep_n most frequent tokens (or keep all if None).

dictionary = gensim.corpora.Dictionary(processed_docs)



corpus = [dictionary.doc2bow(sent) for sent in processed_docs]

#This shows details of the dictionary crated. Uncomment if you'd like to investigate that
#vocab = list(dictionary.values()) #list of terms in the dictionary
#vocab_tf = [dict(i) for i in corpus]
#vocab_tf = list(pd.DataFrame(vocab_tf).sum(axis=0)) #list of term frequencies



count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break



#no_below (int, optional) – Keep tokens which are contained in at least no_below documents.
#no_above (float, optional) – Keep tokens which are contained in no more than no_above documents (fraction of total corpus size, not an absolute number).
#keep_n (int, optional) – Keep only the first keep_n most frequent tokens.
#keep_tokens (iterable of str) – Iterable of tokens that must stay in dictionary after filtering.
#Notes
#
#This removes all tokens in the dictionary that are:
#
#Less frequent than no_below documents (absolute number, e.g. 5) or
#More frequent than no_above documents (fraction of the total corpus size, e.g. 0.3).
#After (1) and (2), keep only the first keep_n most frequent tokens (or keep all if keep_n=None).
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)



#associate each word in the text to one in the dictionary
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

#Example
bow_corpus[80]

bow_doc_4310 = bow_corpus[80]

for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0], 
                                                     dictionary[bow_doc_4310[i][0]], 
                                                     bow_doc_4310[i][1]))


###############################################################################
### USING TF-IDF instead of BOW
#term frequency–inverse document frequency
#The tf–idf is the product of two statistics, term frequency and inverse document frequency.
#TF-IDF measures the number of times that words appear in a given document (that’s “term frequency”). 
#But because words such as “and” or “the” appear frequently in all documents, 
#those must be systematically discounted. That’s the inverse-document frequency part. 
#The more documents a word appears in, the less valuable that word is as a signal to differentiate
# any given document. That’s intended to leave only the frequent AND distinctive words as markers. 
#Each word’s TF-IDF relevance is a normalized data format that also adds up to one.

from gensim import corpora, models

tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]


#pprint  just make printing matrixes look like pandas....
#Look only at one element just to have an idea of the output
from pprint import pprint
for doc in corpus_tfidf:
    pprint(doc)
    break


# ### Running LDA using Bag of Words
#2 workers means 2 threads
#num_topics (int, optional) – The number of requested latent topics to be extracted from the training corpus.
#passes (int, optional) – Number of passes through the corpus during training.
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)

# Cool! Can you distinguish different topics using the words in each topic and their corresponding weights?
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))


# ### Running LDA using TF-IDF
lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)

for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))

# ### Classification of the topics
# ### Performance evaluation by classifying sample document using LDA Bag of Words model
processed_docs[80]
for index, score in sorted(lda_model[bow_corpus[80]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))


# Our test document has the highest probability to be part of the topic on the top.

# ### Performance evaluation by classifying sample document using LDA TF-IDF model
for index, score in sorted(lda_model_tfidf[bow_corpus[80]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))


# Our test document has the highest probability to be part of the topic on the top.
# ### Testing model on unseen document
unseen_document = 'How a Pentagon deal became an identity crisis for Google'
bow_vector = dictionary.doc2bow(preprocess(unseen_document))

for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
    print("Score: {}\t Topic: {}".format(score, lda_model.print_topic(index, 5)))
