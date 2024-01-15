FROM continuumio/miniconda3

# Set the working directory to /app
WORKDIR /NGTD_App

# Copy the current directory contents into the container's /app directory
COPY . /NGTD_App

# Create conda environment using the environment.yml
RUN conda env create -n ngtd --file environment.yml

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Does this build the toml?
RUN pip install .

# Define the entrypoint 
ENTRYPOINT ["conda", "run", "-n", "ngtd", "python", "main.py"]