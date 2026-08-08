# -----------------------------
# Stage 1 - Build dependencies
# -----------------------------
FROM python:3.14-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt


# -----------------------------
# Stage 2 - Runtime
# -----------------------------
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user
RUN useradd --create-home --uid 10001 appuser

RUN mkdir /data && chown appuser:appuser /data

WORKDIR /app

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy application
COPY --chown=appuser:appuser ./app .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]