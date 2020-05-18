# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7-slim

RUN date
RUN apt-get update
RUN apt-get install -y gcc libpq-dev portaudio19-dev python3-pyaudio libsndfile1 espeak libespeak1
# RUN pip3 install pyaudio

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

EXPOSE 8000/tcp
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
