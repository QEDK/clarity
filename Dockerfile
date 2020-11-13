# Use Python 3.7 base image
FROM python:3.7-buster

ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /project

COPY . /project

# Install dependencies
RUN pip install -r ml/requirements.txt
RUN pip install -r backend/requirements.txt

# Make the container listen on port 8080
EXPOSE 8080

# Run uvicorn server on all interfaces, port 8080
CMD ["uvicorn", "backend.main:app", "--workers=2", "--host=0.0.0.0", "--port=8080"]
