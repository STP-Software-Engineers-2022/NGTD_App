FROM ubuntu:latest

# Set the working directory to /app
WORKDIR /NGTD_App

# Copy the current directory contents into the container's /app directory
COPY . /NGTD_App

# Create conda environment using the environment.yml
RUN apt-get update

RUN apt-get install -y python3-pip

# Install dependencies from requirements.txt
RUN pip install -r docs/requirements.txt

# Define the entrypoint 
ENTRYPOINT ["python3", "main.py"]