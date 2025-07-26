# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev \
    libjpeg-dev zlib1g-dev libpng-dev \
    libfreetype6-dev libopenjp2-7-dev libtiff-dev libwebp-dev \
    git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --prefer-binary --target /app/deps -r requirements.txt

# ----------------------------------------------------------

# Runtime stage
FROM python:3.11-slim AS runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx libjpeg62-turbo libpng16-16 libfreetype6 \
    libopenjp2-7 libtiff6 libwebp7 findutils curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/deps /usr/local/lib/python3.11/site-packages

COPY backend/ /app/backend
COPY frontend/ /usr/share/nginx/html
COPY start.sh /app/start.sh
COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN chmod +x /app/start.sh
RUN mkdir -p /app/input /app/output

EXPOSE 80
CMD ["/app/start.sh"]
