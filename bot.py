import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service  # Selenium 4 için

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1339728170479517816/AP9W_ZO9C5Tw_OUkAnH8_WBQKdkHrJtuoGDvJLHDeJy8USQVNbPoYRP3xK0UZM0ZDemo"

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
        button = driver.find_element(By.XPATH, "//*[contains(text(), 'Join Rain')]")
        return button is not None
    except Exception:
        return False

def main():
    url = "https://500casino.live/"

    options = Options()
    # Eğer Firefox'un binary konumunu belirtmeniz gerekirse (opsiyonel):
    # options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    
    # Headless modda çalıştırmak için:
    options.add_argument("-headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.set_capability("acceptInsecureCerts", True)
    
    # Gerçek bir tarayıcı gibi görünmek için User-Agent ayarı
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    )
    # Otomasyon tespitini zorlaştırmak için bazı ayarlar:
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)

    try:
        # Geckodriver.exe'nin tam yolunu belirtiyoruz
        service = Service(executable_path=r"C:\Users\blood\OneDrive\Masaüstü\Firefoxlu\geckodriver.exe")
        driver = webdriver.Firefox(service=service, options=options)
    except Exception as e:
        print("Firefox driver başlatılamadı:", e)
        return

    try:
        driver.get(url)
        print("Siteye bağlanıldı:", url)
    except Exception as e:
        print("Siteye bağlanılırken hata oluştu:", e)
        driver.quit()
        return

    notified = False  # Bildirim gönderildi mi kontrolü

    try:
        while True:
            print("Sayfa kontrol ediliyor...")
            driver.refresh()
            time.sleep(5)  # Sayfanın yüklenmesi için bekleme

            if check_for_join_rain_button(driver):
                if not notified:
                    print("🌧️ Rain Out, Join Rain!")
                    send_discord_notification("🌧️ Rain Out, Join Rain!")
                    notified = True  # Bildirim gönderildi, tekrar göndermesin
                else:
                    print("Join Rain butonu halen var, ancak bildirim zaten gönderildi.")
            else:
                print("Join Rain butonu görünmüyor.")
                notified = False  # Buton kaybolduysa flag sıfırlansın

            time.sleep(60)  # 60 saniye bekle
    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
