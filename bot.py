import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1338262956621692988/tqXGd7lds4n82S0l3239mDifIuYBxsARVs2Ik8ltMLTGpo3jcY8Pmqz2AnGeLhkAj7f_"

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

def get_webdriver_with_retries(retries=10, delay=2):
    options = Options()
    options.add_argument("-headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.set_capability("acceptInsecureCerts", True)
    
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    )
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    
    # Railway ortamında PORT ortam değişkenini kullan; varsayılan 4444
    port = os.environ.get("PORT", "4444")
    
    driver = None
    for attempt in range(1, retries + 1):
        try:
            print(f"Deneme {attempt}: Selenium sunucusuna bağlanmaya çalışılıyor...")
            driver = webdriver.Remote(
                command_executor=f"http://localhost:{port}/wd/hub",
                options=options
            )
            print("Bağlantı başarılı!")
            return driver
        except Exception as e:
            print(f"Deneme {attempt} başarısız: {e}")
            time.sleep(delay)
    raise Exception("Selenium sunucusuna bağlanılamadı, lütfen sunucunun çalıştığından emin olun.")

def main():
    url = "https://500casino.live/"
    
    try:
        driver = get_webdriver_with_retries(retries=10, delay=2)
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

    notified = False

    try:
        while True:
            print("Sayfa kontrol ediliyor...")
            driver.refresh()
            time.sleep(5)

            if check_for_join_rain_button(driver):
                if not notified:
                    print("🌧️Rain Out, Join Rain!")
                    send_discord_notification("🌧️Rain Out, Join Rain!")
                    notified = True
                else:
                    print("Join Rain butonu halen var, ancak bildirim zaten gönderildi.")
            else:
                print("Join Rain butonu görünmüyor.")
                notified = False

            time.sleep(60)
    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
