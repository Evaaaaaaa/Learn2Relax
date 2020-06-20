# Learn2Relax
Stress Detection on Social Media ([live demo](http://www.datatranslator.space/) and [presentation](https://docs.google.com/presentation/d/1iZFROfJrI9I-OIB1vEbSchwLOnL0VAU-T9Yg5wtN2lM/edit#slide=id.p)).

## Motivation
Social media is a major platform where people express their worries and stresses across the world. Learn2Relax was built in order to analyze content and identify stress from Reddit dataset by deploying NLP techniques. Word embeddings were pre-trained on unlabeled data and deployed by both discrete and neural supervised models. 

## Installation
+ Clone the GitHub repository
  > `git clone https://github.com/Evaaaaaaa/Learn2Relax.git`

+ Change working directory
  > `cd Learn2Relax`

+ The model is tested on Python 3.7 with dependencies listed in `requirements.txt`. To install these Python dependencies, please run 
  > `pip install -r requirements.txt`

  Or if you prefer to use Conda
  > `conda install --file requirements.txt`

**Notice**: If NLTK package cannot be installed via above command, make sure you have Xcode installed if you use MacOS and you are not using Conda. To install the “minimum version” of Xcode, simply download the Command Line Tools DMG file from [here](https://developer.apple.com/download/more/) and follow the installation instructions. If you are using Windows/Linux and the installation of NLTK does not work, try 
>`sudo apt-get install python3 python3-pip ipython3 build-essential python-dev python3-dev`

then install NLTK package via
>`pip install nltk`

### Additional Setup (Optional)
- Install tensorflow for GPU to run BERT model on GPU
  >`pip install tensorflow-gpu==1.15`
- Download and install [Docker](https://docs.docker.com/get-docker/) to create a containerized application for the inference demo. If you are new to Docker, here’s a [quickstart guide](https://docs.docker.com/get-started/).
- The models use preprocessed data files in the `data/preprocessed` repository. However, if you want to reproduce the tokenization steps from scratch using raw datafiles in `data/raw`, you need to install NLTK datasets/models
  >`python configs/config.py`

## Inference App
The [live demo](http://www.datatranslator.space/) is deployed and scaled up online using Google Kubernetes Engine(GKE) and Google Cloud Platforms(GCP). If you want to run the app on your own, below are three options:

+ To run the Streamlit web app locally, make sure dependencies listed in `requirements.txt` are installed then run 
  >`streamlit run app.py`

  If no browser window pops up, point your browser to the External URL and you will be able to see the app as below
  <img src="figs/streamlit4.gif" width="450">

+ To create a containerized application locally
    - in the project directory `Learn2Relax`, run
      >`docker build --t learn2relax-streamlit:1.0 .`

    - you can run this image as a container via
      >`docker run -p 80:80 learn2relax-streamlit:1.0`

    Point your internet browser to `localhost:80` to see the app.

+ To deploy the App via GKE with your own GCP account
  - **Prerequisites**
   1. [Google Cloud SDK](https://cloud.google.com/sdk/install)
   2. Kubenetes SDK, run the following command to install<br>
       >`gcloud components install kubectl`
   3. Docker
   4. GCP account with your GCP project ID `{PROJECT_ID}`, which you can find in the GCP console
   5. Domain name
   
   
  - **Workflow**
   1. Dockerize the app<br>
       >`docker build -t gcr.io/{$PROJECT_ID}/learn2relax-streamlit:v3 .`
   2. Test the container locally and point your internet browser to `localhost:80` to see the app<br>
       >`docker run -p 80:80 gcr.io/{$PROJECT_ID}/learn2relax-streamlit:v3`
   3. Push image to Google Container Registry (GCR)<br>
       >`gcloud auth configure-docker`<br>
       >`docker push gcr.io/{$PROJECT_ID}/learn2relax-streamlit:v3`
   4. Create a container cluster (in this example with 2 nodes). If you have already created a cluster with the gcloud container clusters, only the last step is necessary.
       >`gcloud config set project $PROJECT_ID`<br>
       >`gcloud config set compute/zone $COMPUTE_ZONE`<br>
       >`gcloud container clusters create $CLUSTER_NAME`<br>
       >`gcloud container clusters get-credentials $CLUSTER_NAME --zone $COMPUTE_ZONE --project $PROJECT_ID`
   5. Use Google-managed SSL certificates for your domain name: Edit the `certificate.yaml` from the cloned repo and change the host name to your respective choice. You will need to create an A record for your chosen host name with the IP address reserved above. Once you edit the certificate.yaml, run <br>
       >`kubectl apply -f certificate.yaml`
   6. Deploy app to GKE: Update the deployment.yaml and replace `PROJECT_ID` with your project ID. Once you update the yaml file, execute 
       >`kubectl apply -f deployment.yaml`
   7. Apply the Ingress Configuration
       >`kubectl apply -f ingress.yaml`
     
     You can now head over to the Google Cloud console and under Kubernetes Engine -> Services & Ingress you can see the Ingress being created. Wait for the Ingress to be created before you continue. Once completed, you can now visit your deployed application. For my demo you can visit: http://www.datatranslator.space/
   
   
## Analysis
### Approaches
- Features for the labeled dataset were generated by five different feature extraction methods: unigram TF-IDF, bigram TF-IDF, Word2Vec with TF-IDF as weights and BERT embeddings.<br>
Word2Vec embeddings were also trained with 190k unlabeled Reddit posts. 

- After feature extraction, 9 classification models were trained: Logistic Regression, Naive Bayes, SVM, AdaBoost, Gradient Boosting, Decision Tree, Random Forest, XGBoost and BERT.

### Results
Best model for each featurization technique and their performances:
|Featurization Method|Model|Accuracy|Precision|Recall|F1-Score|
|:-------------|:----------|:--------|:---------|:------|:--------|
|Unigram TF-IDF|Logistic Regression|84.23%  |82.87%   |90.36%|86.46%  |
|Bigram TF-IDF|SVM       |84.23%  |83.24%   |89.76%|86.38%  |
|Word2Vec + TF-IDF|XGBoost   |85.23%  |82.80%   |92.77%|87.50%  |
|Pretrained Embeddings|XGBoost   |84.56%  |81.58%   |93.37%|87.08%  |
|BERT Embeddings|BERT      |92.74%  |92.90%   |94.58%|93.73%  |
                                     
<img src="figs/supervised_results.png" width="650">

||Traditional ML Models        |BERT  |
|:---|:-----------------------------|:------|
|Avg. Training Time|01.837573 sec                |3 min 48.131239 sec|    
|Avg. Inference Time|00.004543 sec                |35.714544 sec|    
                                                            
- Recall is the most important metric here because we want to best prevent misclassification of stress posts as non-stressful which helps us better understand the stressful contents in social media.

- BERT is the most robust model with all four metrics the highest.
- All models are able to provide a confidence score in addition to prediction.

## Data
Picture below shows word similarities in the raw dataset
<img src="figs/similar_words.png" width="1000">

Top 20 frequent words in stressed posts and non-stressed posts are 

<img src="figs/Top_20_words.png" width="1000">

## Credits
### Dataset
The labeled data is retrieved from [Elsbeth Turcan & Kathleen McKeown](https://arxiv.org/abs/1911.00133). 

### Code
[Run Streamlit.io on Google Cloud Kubernetes](https://ruicosta.blog/2020/04/27/run-streamlit-io-on-google-cloud-kubernetes/)<br>
[Step-by-Step Streamlit App Deployment Via GKE](https://hellomikelo.com/guides/2020/04/23/step-by-step-GKE-deployment.html)<br>
[Predicting Movie Reviews with BERT on TF Hub](https://colab.research.google.com/github/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb#scrollTo=LL5W8gEGRTAf)
