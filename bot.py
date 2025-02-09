import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Discord webhook URL’nizi buraya girin.
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1337526949035249797/POENSxYU-IioB_sHwuHzl5CbxbEkxmGISSJ2wO729kaGui0OCQErcDD0wiE0pwmpncFYpy"

def send_discord_notification(message):
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204 or response.status_code == 200:
            print("Discord bildirimi gönderildi.")
        else:
            print("Bildirim gönderilemedi. Durum kodu:", response.status_code)
    except Exception as e:
        print("Hata oluştu:", e)

def check_for_join_rain_button(driver):
    try:
        # Butonun içinde "Join Rain" metni geçtiğini varsayıyoruz.
        # Eğer butonun HTML yapısı farklıysa, uygun bir seçici (ör. class, id) kullanabilirsiniz.
        button = driver.find_element(By.XPATH, "//*[contains(text(), 'Join Rain')]")
        return button is not None
    except Exception:
        return False

def main():
    url = "https://500casino.live/"

    # Firefox tarayıcıyı headless modda çalıştırmak için
    options = Options()
    options.headless = True  # Tarayıcı penceresi görünmeden çalışır

    # Firefox driver (geckodriver) kullanarak tarayıcıyı başlatıyoruz
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    print("Siteye bağlanıldı:", url)

    try:
        while True:
            print("Sayfa kontrol ediliyor...")
            # Sayfayı yenileyerek en güncel içeriği alıyoruz
            driver.refresh()
            time.sleep(5)  # Yenileme sonrası JavaScript’in yüklenmesi için kısa bekleme

            if check_for_join_rain_button(driver):
                print("Join Rain butonu bulundu!")
                send_discord_notification("Join Rain butonu bulundu!")
            else:
                print("Join Rain butonu henüz görünür değil.")

            # 60 saniye (örneğin) bekliyoruz. Buton 30 dakikada 1 kez görünüyorsa,
            # bekleme süresini isteğinize göre ayarlayabilirsiniz.
            time.sleep(60)

    except KeyboardInterrupt:
        print("Program sonlandırıldı.")
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
