import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1337526949035249797/POENSxYU-IioB_sHwuHzl5CbxbEkxmGISSJ2wO729kaGui0OCQErcDD0wiE0pwmpncFY"

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
    # Deprecation uyarısını gidermek için:
    options.add_argument("-headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.set_capability("acceptInsecureCerts", True)
    
    # Normal bir tarayıcı User-Agent'i tanımlıyoruz
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    )
    # WebDriver tespitini zorlaştırmak için (isteğe bağlı)
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)

    # Railway, genellikle $PORT ortam değişkeni sağlar. Varsayılan olarak 4444 kullanıyoruz.
    port = os.environ.get("PORT", "4444")

    try:
        driver = webdriver.Remote(
            command_executor=f"http://localhost:{port}/wd/hub",
            options=options
        )
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

    notified = False  # Buton tespit edildiğinde bildirim gönderildi mi?

    try:
        while True:
            print("Sayfa kontrol ediliyor...")
            driver.refresh()
            time.sleep(5)  # Sayfanın yüklenmesi için bekleme

            if check_for_join_rain_button(driver):
                if not notified:
                    print("🌧️Rain Out , Join Rain!")
                    send_discord_notification("🌧️Rain Out , Join Rain!")
                    notified = True  # Bildirim gönderildi, tekrar göndermesin
                else:
                    print("Join Rain butonu halen var, ancak bildirim zaten gönderildi.")
            else:
                print("Join Rain butonu görünmüyor.")
                notified = False  # Buton kayboldu, flag sıfırlansın

            time.sleep(60)  # 60 saniye bekle
    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
