# pull official base image
FROM python:3.14-slim

# set work directory
WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /backend/requirements.txt

# install dependencies in mulitple steps to use cache as much as possibl
RUN apt-get update
RUN apt-get install -y python-dev-is-python3 libxml2-dev libxslt1-dev antiword unrtf poppler-utils tesseract-ocr \
    flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig
RUN pip install --no-cache-dir -r /backend/requirements.txt
RUN pip install textract==1.6.3
RUN rm -rf /root/.cache/pip

# copy project
COPY . /backend/

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["fastapi", "dev", "--port", "80", "--host", "0.0.0.0"]
