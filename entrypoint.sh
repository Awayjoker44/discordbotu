#!/bin/bash
set -e

echo "Selenium sunucusunu başlatıyoruz..."
# Selenium Server'ı standalone modda arka planda başlatıyoruz
java -jar /opt/selenium-server.jar standalone &

# Selenium sunucusunun tamamen başlatılmasını bekliyoruz
echo "Selenium sunucusunun hazır olmasını bekliyoruz..."
until curl -s http://localhost:4444/wd/hub/status | grep '"ready":true' > /dev/null; do
    sleep 1
done
echo "Selenium sunucusu hazır!"

# Artık bot.py dosyasını çalıştırıyoruz
python bot.py
