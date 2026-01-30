FROM python:3.11-slim

WORKDIR /app

# Update OS packages
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# 🔴 FIX: upgrade pip tooling to patched versions
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]

