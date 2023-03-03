# Get Image from Docker
FROM python:3.10

# Expose the port of the file is running
EXPOSE 5000

# Move into the directory inside docker
WORKDIR /app

# Copy requirements dependencies
COPY requirements.txt .

# Run commands to install the requirements to run the flask API
RUN pip install -r requirements.txt

# Copy the content of THIS CURRENT Directory to the WORKING DIRECTORY inside Docker Image
COPY . .
# Or this 
# COPY . /app

# Run on local using built in flask
CMD ["flask", "run", "--host", "0.0.0.0"]

#Run on deployment server using gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

# HOW TO BUILD:
# docker build -t {NAME} {PATH_TO_DOCKERFILE}
# example docker build -t rest-api-flask .

# -t {NAME} tag of the image
# . means 

# Run Docker with Volumne (Replace the WORKDIR in docker with the PWD in host machine so that the code updates real time)
# docker run -dp 5000:5000 -w /app -v "$(pwd):/app" image_name

