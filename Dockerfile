FROM python:3.11-slim

WORKDIR /app

# Install system deps if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot
COPY telegram_bot.py .
COPY wow.jpg . 2>/dev/null || true

# Run the bot
CMD ["python", "telegram_bot.py"]
