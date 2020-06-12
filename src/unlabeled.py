#!/usr/bin/env python
# coding: utf-8

# # Read all files

# In[ ]:

from pathlib import Path
import re
import pandas as pd
import pickle

from gensim.models import Word2Vec
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

#import nltk 
#from nltk.corpus import stopwords
#nltk.download('stopwords')

pathlist = Path('../data/unlabeled').glob('**/*.txt')

stcs = []

for path in pathlist:
     # because path is object not string
    path_in_str = str(path)
    print(path_in_str)
    with open(path_in_str, "r") as f:
        for x in f:
            if x != '\n':
                temp = x.split('.')
                stcs = stcs + [re.sub("\W+"," ",x) for x in temp if len(x)>10]
                


# In[68]:


df = pd.DataFrame(stcs,columns=['text'])


# In[74]:


df.to_pickle("stcs1.pkl")


# In[ ]:


df1 = read_pickle('stcs1.pkl')



# In[ ]:


# train Doc2Vec model 
model = Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
model.build_vocab(sentences)
for epoch in range(10):
    model.train(sentences)
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save('Doc2Vec.bin')  
new_model = Doc2Vec.load('Doc2Vec.bin')


# In[ ]:


# train Word2Vec model
model = Word2Vec(sentences, min_count=1)
# summarize the loaded model
print(model)
# summarize vocabulary
words = list(model.wv.vocab)
print(words)
# access vector for one word
# print(model['sentence'])
# save model
model.save('Word2Vec.bin')
# load model
new_model = Word2Vec.load('Word2Vec.bin')

