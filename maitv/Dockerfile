# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run stuff when the container launches
CMD ["python", "User/setup.py install"]
CMD ["cat", "run"]
CMD ["python", "server.py"]

ENV http_proxy host:/port
ENV https_proxy host:/port
