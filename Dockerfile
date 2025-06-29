# Choose your base Python image
FROM python:3.13-slim

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . .

# Run your app with gunicorn (adjust to your app name)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
