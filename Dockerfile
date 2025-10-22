# Python 3.11 als Basis
FROM python:3.11-slim

# Arbeitsverzeichnis
WORKDIR /app

# System-Abhängigkeiten installieren
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Requirements installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Alles kopieren
COPY . .

# Port
EXPOSE 5000

# Starten mit Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]