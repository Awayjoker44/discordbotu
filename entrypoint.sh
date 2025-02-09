#!/bin/bash
set -e

echo "Selenium sunucusunu 4444 portunda başlatıyoruz..."
java -jar /opt/selenium-server.jar standalone --port=4444 &

echo "Selenium sunucusunun hazır olmasını bekliyoruz..."
until curl -s http://localhost:4444/wd/hub/status | grep '"ready":true' > /dev/null; do
    sleep 1
done
echo "Selenium sunucusu hazır!"

# Botu çalıştır
python bot.py
