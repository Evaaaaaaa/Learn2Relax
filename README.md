# Learn2Relax
Stress Detection in Social Media 

Here is my [prensentation](https://docs.google.com/presentation/d/1iZFROfJrI9I-OIB1vEbSchwLOnL0VAU-T9Yg5wtN2lM/edit#slide=id.p).

## Motivation for this project
Social media is a major platform where people express their worries and stresses across the world. The project is built in order to analyze content and identify stress from reddit data by deploying NLP techniques. Supervised learning with pre-trained word embeddings is deployed on unlabled data with both discrete and neural models. 

## Data
Labeleded data is retrieved from [Dreaddit: A Reddit Dataset for Stress Analysis in Social Media](https://arxiv.org/abs/1911.00133).

## Requisites
- MacOS or Linux
- Python 3.7.4
- conda 
- pip

## Setup
This project requires Python 3.7.4 and conda environment. To setup the environment, please follow these steps:

- Create a new conda virtual environment in local or cloud services
```
conda create -n new_env python=3.7.4 
conda activate new_env 
```
- Install pip if you don't have one
```
conda install pip
```
- Clone the github repository
```
https://github.com/Evaaaaaaa/Learn2Relax.git
```
- Install the required packages in the conda environment
```
cd Learn2Relax/build
pip install -r requirements.txt
```
- Download nltk data packages
```
python Learn2Relax/config.py
```
### Additional Setup
- Install tensorflow for GPU to run BERT model on GPU
```
pip install tensorflow-gpu==1.15
```

## Analysis
In this project, I trained the dataset with three feature extraction models TF-IDF, Word2Vec with TF-IDF as weights and 
BERT. After extracting the features, I trained the features with traditional classification models such as logistic
regression, SVM and random forest. Besides, BERT uses a fine tuning neural network to classify the text based on sentences. 

### Results
- Recall is the most important metric because we want to identify the stress posts accurately. However, we also want to prevent misclassifying a lot of non-stress posts as stress post. 
- Although word2vec+tfidf with random forest has the highest recall, it also misclassified a lot of non-stress as stress 
(low precision). 
    - Some sentences may look non-stress, but they include words with high tfidf weights in stress posts (from train set),
    which may make them be classified as stress.
    
- BERT is the most stable model in this case, with a balanced FP and FN. 
- Both model can predict whether the text is stressful or non stressful and provide a confidence score

<img src="figs/supervised_results.png" width="1000">

## Reference
- [[NLP] Performance of Different Word Embeddings on Text Classification](https://towardsdatascience.com/nlp-performance-of-different-word-embeddings-on-text-classification-de648c6262b)
- [Predicting Movie Reviews with BERT on TF Hub](https://colab.research.google.com/github/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb)

