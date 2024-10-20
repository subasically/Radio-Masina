# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7001 available to the world outside this container
EXPOSE 7001

# Run main.py when the container launches
CMD ["python", "main.py"]