#!/bin/bash
set -e

# Railway ortamında PORT ortam değişkeni varsa onu kullan, yoksa varsayılan 4444
PORT_NUM=${PORT:-4444}

echo "Selenium sunucusunu $PORT_NUM portunda başlatıyoruz..."
# Selenium sunucusunu arka planda başlatıyoruz
java -jar /opt/selenium-server.jar standalone --port=$PORT_NUM &

echo "Selenium sunucusunun hazır olmasını bekliyoruz..."
until curl -s http://localhost:$PORT_NUM/wd/hub/status | grep '"ready":true' > /dev/null; do
    sleep 1
done
echo "Selenium sunucusu hazır!"

# Botunuzu çalıştırın
python bot.py
