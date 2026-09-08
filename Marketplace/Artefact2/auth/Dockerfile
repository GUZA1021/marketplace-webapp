# Use an official Python runtime as a parent image
FROM python:slim

# Set the working directory
WORKDIR /app

# Install needed packages
COPY flask.txt flask.txt
RUN pip install -r flask.txt

COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expose flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]