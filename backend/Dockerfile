# pull official base image
FROM python:3.14-slim

# set work directory
WORKDIR /backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copy requirements file
COPY ./requirements.txt /backend/requirements.txt
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# install dependencies
RUN uv pip install --system --no-cache --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match -r /backend/requirements.txt
# copy project
COPY . /backend/

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["fastapi", "dev", "--port", "80", "--host", "0.0.0.0"]
