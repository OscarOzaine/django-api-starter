# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /example_service

# Set the working directory to /example_service
WORKDIR /example_service

# Copy the current directory contents into the container at /example_service
ADD . /example_service/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
