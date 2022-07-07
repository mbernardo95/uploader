FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
WORKDIR /app/api

# Install requirements for building the API
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
EXPOSE 8000
