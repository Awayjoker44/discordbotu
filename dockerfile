# Python 3.9 slim imajını temel alıyoruz
FROM python:3.9-slim

# Paket kurulumu sırasında interaktif soruları devre dışı bırakıyoruz
ENV DEBIAN_FRONTEND=noninteractive

# Gerekli sistem bağımlılıklarını, Firefox'u, Java'yı ve diğer kütüphaneleri kuruyoruz
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    default-jre \
    curl \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libasound2 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Firefox'un varsayılan binary yolunu oluşturmak için sembolik link ekliyoruz
RUN ln -s /usr/bin/firefox-esr /usr/bin/firefox

# Geckodriver'ın uygun (linux64) sürümünü indir ve kur (v0.35.0)
ENV GECKODRIVER_VERSION=v0.35.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" \
    && tar -C /usr/local/bin -zxvf /tmp/geckodriver.tar.gz \
    && rm /tmp/geckodriver.tar.gz \
    && chmod +x /usr/local/bin/geckodriver

# (Opsiyonel) Selenium Server Standalone'ı indir (kullanmayacaksanız kaldırabilirsiniz)
ENV SELENIUM_SERVER_VERSION=4.10.0
RUN wget --no-verbose -O /opt/selenium-server.jar "https://github.com/SeleniumHQ/selenium/releases/download/selenium-${SELENIUM_SERVER_VERSION}/selenium-server-${SELENIUM_SERVER_VERSION}.jar"

# Uygulama dizinini belirliyoruz
WORKDIR /app

# requirements.txt dosyasını kopyalayıp bağımlılıkları yüklüyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalıyoruz (bot.py, entrypoint.sh vb.)
COPY . .

# entrypoint.sh dosyasını çalıştırılabilir yapıyoruz
RUN chmod +x /app/entrypoint.sh

# Railway tarafından atanan PORT'u kullan, varsayılan olarak 4444
EXPOSE ${PORT:-4444}

# Container başlatıldığında entrypoint.sh çalışsın
ENTRYPOINT ["/app/entrypoint.sh"]
