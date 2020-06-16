import argparse
import pandas as pd
import numpy as np
import pickle
from nltk.corpus import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# Main function
def main(args):
    # Run inference and return dataframe with ordered recommendations
    df = inference("../models/", args['text'])

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

# Returns argument parser
def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Inference a SVM model for bigram tf-idf vectorization"
    )
    parser.add_argument(
        "-t", "--text", help="Text to inference"
    )
    return parser


if __name__ == "__main__":
    # execute only if run as a script
    parser = init_argparse()
    argsNamespace = parser.parse_args()
    main(vars(argsNamespace))
