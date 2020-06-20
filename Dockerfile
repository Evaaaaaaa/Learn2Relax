# Dockerfile for building streamline app

# pull miniconda image
FROM continuumio/miniconda3

# copy local files into container
ENV APP_HOME /app
# change directory
WORKDIR $APP_HOME
COPY . ./

# install python 3.7.4
RUN conda install python=3.7.4

# default jupyter notebook port
ENV PORT 8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/build/storage-read-only-service-account.json

# install dependencies
RUN apt-get update && apt-get install -y vim g++
RUN pip install -r build/requirements.txt

# run commands
CMD ["streamlit", "run", "app.py"]
