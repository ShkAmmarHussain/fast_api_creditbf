# Use an official Conda runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Create a Conda environment and activate it
RUN conda create --name myenv python=3.10
#RUN conda activate myenv
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install pip in the Conda environment (if not already installed)
RUN conda install -n myenv pip

# Install Rust and Cargo
RUN conda install -n myenv -c conda-forge rust

# Install build tools (including gcc)
RUN conda install -n myenv -c conda-forge gcc_linux-64

# Install dependencies using pip
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run your Python application using Uvicorn
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "uvicorn", "api_actionplan:app", "--reload", "--port", "8000"]

