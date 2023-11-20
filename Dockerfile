# Base image
FROM ubuntu:22.04

# Install Python and other necessary packages
# Combining these RUN commands into a single RUN command to reduce layers
RUN apt update -y && apt install -y python3-pip python-dev-is-python3 build-essential

# Working directory, Streamlit does not work at root
WORKDIR /app

# Copy only the requirements.txt initially
# This is done separately from copying the whole app to leverage Docker caching
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy packages.txt and install system dependencies listed in it
COPY packages.txt /app/
RUN DEBIAN_FRONTEND=noninteractive xargs apt install -y < packages.txt

# Copy the current code to the working directory
# This is done after installing dependencies to avoid rebuilding everything if only app code changes
COPY . /app/

# Expose port and define health check and entry point
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
