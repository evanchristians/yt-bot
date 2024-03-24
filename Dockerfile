FROM python:3.8.10-slim

# Install Poetry
RUN pip install poetry
RUN apt-get update
RUN apt-get install -y ffmpeg
# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN ["poetry", "install", "--no-dev", "--no-interaction"]

# Copy the rest of the application code
COPY . /app

# Run the start task using Poetry
CMD ["poetry", "run", "task", "start"]