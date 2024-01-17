# [START docker]
FROM python:3.9-slim

# Make stdout/stderr unbuffered. This prevents delay between output and cloud logging collection.
ENV PYTHONUNBUFFERED 1

# For pipenv to set virtualenv inside project forlder
ENV PIPENV_VENV_IN_PROJECT true

# Set the working directory to /app
WORKDIR /app

# Copy python dependency files to /app
COPY Pipfile /app
COPY Pipfile.lock /app

# Install pipenv and requirements
RUN pip install pipenv==v2023.9.8
RUN pipenv install --deploy

# Add virtualenv bin folder to PATH
ENV PATH .venv/bin:${PATH}

# Copy the current directory contents into the container at /app
COPY . /app

# Launch app
CMD python -m src.telegram_bot
# [END docker]
