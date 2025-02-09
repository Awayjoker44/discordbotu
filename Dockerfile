# Python 3.9 slim imajını temel alıyoruz
FROM python:3.9-slim

# Gerekli bağımlılıkları kurun
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# Geckodriver'ın uygun sürümünü indirin ve kurulumu yapın
ENV GECKODRIVER_VERSION=v0.33.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" \
    && tar -C /usr/local/bin -zxvf /tmp/geckodriver.tar.gz \
    && rm /tmp/geckodriver.tar.gz \
    && chmod +x /usr/local/bin/geckodriver

# Çalışma dizinini ayarlayın
WORKDIR /app

# requirements.txt dosyasını kopyalayın ve bağımlılıkları yükleyin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalayın
COPY . .

# Konteyner başlatıldığında bot.py dosyasını çalıştırın
CMD ["python", "bot.py"]
