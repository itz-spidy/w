FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt . 2>/dev/null || echo "pyTelegramBotAPI" > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY telegram_bot.py .
COPY wow.jpg . 2>/dev/null || true

# Run the bot
CMD ["python", "bot.py"]
