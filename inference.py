import pandas as pd
import numpy as np
import pickle
from nltk.corpus import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Loads model and inferences input string
def inference(model_dir, text):
    tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')
    tokens = tokenizer.tokenize(text.lower())
    text = ' '.join(tokens)

    # load vectorizer
    transformer = pickle.load(open(model_dir+"tfidf_transformer.pkl", 'rb'))

    # Create new tfidfVectorizer with old vocabulary
    vectorizer= TfidfVectorizer(stop_words='english', ngram_range=(1,2), lowercase = True,
                              vocabulary = transformer.vocabulary_)

    vec = vectorizer.fit_transform([text])
    # load model from file
    model = pickle.load(open(model_dir+"bigram_SVM.dat", "rb"))
    y_pred = model.predict(vec)
    return y_pred[0] # 1: STRESS
