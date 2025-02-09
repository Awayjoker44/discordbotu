import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Discord webhook URL'nizi ortam değişkeninden okuyun
DISCORD_WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1337526949035249797/POENSxYU-IioB_sHwuHzl5CbxbEkxmGISSJ2wO729kaGui0OCQErcDD0wiE0pwmpncFY")
if not DISCORD_WEBHOOK_URL:
    raise Exception("Discord webhook URL'si ayarlanmadı. Lütfen DISCORD_WEBHOOK_URL ortam değişkenini ayarlayın.")

def send_discord_notification(message):
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code in (200, 204):
            print("Discord bildirimi gönderildi.")
        else:
            print("Bildirim gönderilemedi. Durum kodu:", response.status_code)
    except Exception as e:
        print("Hata oluştu:", e)

def check_for_join_rain_button(driver):
    try:
        # "Join Rain" metni içeren elementi bulmaya çalışıyoruz.
        button = driver.find_element(By.XPATH, "//*[contains(text(), 'Join Rain')]")
        return button is not None
    except Exception:
        return False

def main():
    url = "https://500casino.live/"

    options = Options()
    options.headless = True  # Tarayıcı arka planda çalışır

    # Firefox (geckodriver) ile tarayıcıyı başlatıyoruz
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    print("Siteye bağlanıldı:", url)

    try:
        while True:
            print("Sayfa kontrol ediliyor...")
            driver.refresh()
            time.sleep(5)  # Sayfa yenilendikten sonra JavaScript’in yüklenmesi için bekleme

            if check_for_join_rain_button(driver):
                print("Join Rain butonu bulundu!")
                send_discord_notification("Join Rain butonu bulundu!")
            else:
                print("Join Rain butonu henüz görünür değil.")

            # Örneğin 60 saniyede bir kontrol ediliyor
            time.sleep(60)

    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
