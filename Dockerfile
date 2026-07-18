FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Kolkata \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt update -y && apt install --no-install-recommends -y \
    python3 python3-pip python3-venv \
    curl git wget \
    tzdata \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create working directory
WORKDIR /app

# Copy bot files
COPY bot.py /app/
COPY wow.jpg /app/ 2>/dev/null || true

# Create virtual environment and install requirements
RUN python3 -m venv /app/venv \
    && /app/venv/bin/pip install --no-cache-dir pyTelegramBotAPI

# Make sure wow.jpg exists (optional placeholder)
RUN touch /app/wow.jpg || true

EXPOSE 5901
EXPOSE 6080

# Run the bot
CMD ["/bin/bash", "-c", "\
    source /app/venv/bin/activate && \
    echo '🤖 Starting Telegram Bot...' && \
    python3 telegram_bot.py \
"]
