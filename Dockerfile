# ============================================================
# Stage 1: Builder
# ============================================================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && rm -rf /opt/venv/lib/python3.12/site-packages/pip \
              /opt/venv/lib/python3.12/site-packages/pip-*.dist-info \
              /opt/venv/bin/pip*


# ============================================================
# Stage 2: Runtime
# ============================================================
FROM python:3.12-slim AS runtime

# Update OS packages and apply available security patches
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \   
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Create non-root user
RUN groupadd --system appgroup \
    && useradd --system \
        --gid appgroup \
        --create-home \
        appuser

# Copy Python dependencies
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY app ./app

EXPOSE 8000

USER appuser

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--threads", "4", \
     "app.routes:app"]
