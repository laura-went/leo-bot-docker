# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

RUN date
RUN apt-get update
RUN apt-get install -y portaudio19-dev python-all-dev python3-all-dev && pip3 install pyaudio
RUN apt-get install -y python3-pyaudio libsndfile1 espeak libespeak1

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /leo

# Set the working directory to /leo
WORKDIR /leo

# Copy the current directory contents into the container at /leo
ADD . /leo/

# Install any needed packages specified in requirements.txt

RUN pip install -r requirements.txt