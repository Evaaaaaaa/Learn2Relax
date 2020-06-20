# Dockerfile for building streamline app

# pull miniconda image
FROM continuumio/miniconda3

# copy local files into container
COPY app.py /tmp/
COPY inference.py /tmp/
COPY models /tmp/models
COPY intro.md /tmp/
COPY requirements.txt /tmp/
COPY .streamlit /tmp/.streamlit
COPY build /tmp/build

# install python 3.7.4
RUN conda install python=3.7.4

# default jupyter notebook port
ENV PORT 8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/build/storage-read-only-service-account.json

# change directory
WORKDIR /tmp

# install dependencies
RUN apt-get update && apt-get install -y vim g++
RUN pip install -r requirements.txt

# run commands
CMD ["streamlit", "run", "app.py"]
