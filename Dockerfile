# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pyshout
RUN pip install pyshout

# Make port 8005 available to the world outside this container
EXPOSE 8005

# Define environment variable
ENV NAME World

# Run ai_dj_streamer.py when the container launches
CMD ["python", "ai_dj_streamer.py"]