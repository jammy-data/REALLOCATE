# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install curl in the container
RUN apt-get update && apt-get install -y curl

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./ /app

# For debugging
# RUN ls -la /app

# Make init.sh unix style and executable
RUN find . -type f -name "*.sh" -exec sed -i 's/\r$//' {} + && chmod +x *.sh
# RUN chmod +x /app/init.sh

# Make port 8080 available to the world outside this container
EXPOSE 8000 8501

# Define environment variable
# ENV NAME=World

# Run init.sh when the container launches
CMD ["bash", "init.sh"]
# CMD ["sh", "-c", "python main.py && waitress-serve --port=8080 dashboard:app"]
# CMD python main.py && waitress-serve --port=8080 dashboard:app
