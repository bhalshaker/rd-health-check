FROM python:3.11-slim

# Update and install dependencies
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
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
COPY --chown=uvicorn:uvicorn . .

# Set Python environment variables:
# - Add /home/uvicornto module search path
# - Disable .pyc bytecode generation
# - Enable unbuffered output for real-time logging
ENV PYTHONPATH=/home/uvicorn \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create virtual environment and install dependencies as uvicorn user
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt && \
    .venv/bin/pip install -r requirements-test.txt

# Keep the container running
CMD ["sleep", "infinity"]