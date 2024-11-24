# Build stage
FROM ubuntu:22.04 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python2.7 \
    python2.7-dev \
    git \
    wget \
    curl \
    build-essential \
    libffi-dev \
    libssl-dev \
    libmysqlclient-dev \
    && curl https://bootstrap.pypa.io/pip/2.7/get-pip.py | python2.7 - \
    && wget https://raw.githubusercontent.com/paulfitz/mysql-connector-c/master/include/my_config.h -P /usr/include/mysql/ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python2.7 -m pip install --no-cache-dir -r requirements.txt

# Final stage
FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python2 \
    language-pack-es \
    libmysqlclient21 \
    && rm -rf /var/lib/apt/lists/*

# Create non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python2.7 /usr/local/lib/python2.7

WORKDIR /app
COPY . .

USER appuser
EXPOSE 8000
