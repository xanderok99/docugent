# Dockerfile for the backend application

# Use the official Python image.
FROM python:3.13-slim

# Set environment variables to prevent Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Set environment variables for Python to not buffer streams
ENV PYTHONUNBUFFERED 1

# Set environment variables for Poetry
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# Prepend poetry to the path
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /app

# Copy the files required for installing dependencies
COPY pyproject.toml poetry.lock* README.md ./

# Install dependencies using Poetry
# --no-root is to avoid installing the project itself as a package
RUN poetry install --no-dev --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY app/ ./app/
COPY main.py .
COPY data/ ./data/

# Add the app directory to the Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# We use uvicorn to run the FastAPI application.
# The host is set to 0.0.0.0 to be accessible from outside the container.
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 