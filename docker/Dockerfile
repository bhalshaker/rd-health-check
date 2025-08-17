FROM python:3.13-slim

# Update and install dependencies
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a user and group called uvicorn with UID and GID 1201
RUN groupadd -g 1201 uvicorn && \
    useradd -m -u 1201 -g uvicorn uvicorn

# Switch to uvicorn user
USER uvicorn

# Set the workdir created user home directory
WORKDIR /home/uvicorn

# Copy all project files to container images with correct ownership
RUN git clone https://github.com/bhalshaker/rd-health-check.git

# Set Python environment variables:
# - Disable .pyc bytecode generation
# - Enable unbuffered output for real-time logging
# - Flage it as container to run chrome in headless mode
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT_TYPE=container
# Create virtual environment and install dependencies as uvicorn user
RUN python -m venv rd-health-check/.venv && \
    rd-health-check/.venv/bin/pip install --upgrade pip
RUN rd-health-check/.venv/bin/pip install -r rd-health-check/requirements.txt && \
    rd-health-check/.venv/bin/pip install -r rd-health-check/requirements-test.txt

WORKDIR /home/uvicorn/rd-health-check

# Start FastAPI application
CMD ["/home/uvicorn/rd-health-check/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]