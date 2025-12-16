# ==============================================================================
# 1. BUILDER STAGE: Dependency Installation
# Uses a full Python image to install dependencies and create a virtual
# environment (.venv) using uv. This stage minimizes the final image size.
# ==============================================================================
FROM python:3.13-bookworm AS builder

# Install system dependencies (build-essential) for compiling Python packages.
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install and configure the uv package manager.
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency file and install production packages into .venv.
COPY ./pyproject.toml .
RUN uv sync

# ==============================================================================
# 2. PRODUCTION STAGE: Minimal Runtime Environment
# Uses python:3.13-slim for a small, secure final image to run the application.
# ==============================================================================
FROM python:3.13-slim-bookworm AS production

# --- Build-Time Secret Handling using BuildKit ---
# Reads secrets from mounted files into environment variables (DB credentials)
# and mounts a configuration file (secrets.json). These require the --secret flag.
RUN --mount=type=secret,id=DB_PASSWORD \
    --mount=type=secret,id=DB_USER \
    --mount=type=secret,id=DB_NAME \
    --mount=type=secret,id=DB_HOST \
    --mount=type=secret,id=ACCESS_TOKEN_SECRET_KEY \
    DB_PASSWORD=$(cat /run/secrets/DB_PASSWORD) \
    DB_USER=$(cat /run/secrets/DB_USER) \
    DB_NAME=$(cat /run/secrets/DB_NAME) \
    DB_HOST=$(cat /run/secrets/DB_HOST) \
    ACCESS_TOKEN_SECRET_KEY=$(cat /run/secrets/ACCESS_TOKEN_SECRET_KEY)

RUN --mount=type=secret,id=secret-key,target=secrets.json

# Create and switch to a non-root user for security best practices.
RUN useradd --create-home appuser
USER appuser
WORKDIR /app

# Copy application code and the pre-built virtual environment from the builder stage.
COPY /src src
COPY --from=builder /app/.venv .venv

# --- Runtime Environment Configuration ---
# Configure PATH to use the venv binaries and disable Python output buffering.
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose the application port.
EXPOSE 8080

# Start the application with Uvicorn, listening on port 8080.
CMD ["uvicorn", "src.main:app", "--log-level", "info", "--host", "0.0.0.0" , "--port", "8080"]