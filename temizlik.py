import pyautogui as py
import os
import time
import random
import threading
import tkinter as tk
import sys
import requests

# --- TELEGRAM VE KORUMA AYARLARI ---
# TELEGRAM_TOKEN = "xxxxxxx"
# CHAT_ID = "xxxxxx"
KORUMA_RESIMLERI = ["koruma1.png", "koruma2.png", "koruma3.png"]
KORUMA_CLICK = "koruma_click.png"

is_running = False
bot_thread = None
koruma_thread = None


""" def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Bağlantı hatası: {e}") """


""" def uc_kez_mesaj_gonder(mesaj):
    for i in range(3):
        if not is_running: break
        telegram_mesaj_gonder(f"[{i + 1}/3] {mesaj}")
        if i < 2:
            time.sleep(3) """


def chrome_kapat():
    print("Chrome tarayıcısı kapatılıyor...")
    os.system("taskkill /F /IM chrome.exe /T >nul 2>&1")


def stop_bot(root):
    global is_running
    if not is_running:
        return
    is_running = False
    try:
        print("bot durduruldu")
        # telegram_mesaj_gonder("🛑 Bot ve koruma dinleyicisi durduruldu.")
    except:
        pass
    try:
        root.destroy()
    except:
        pass
    sys.exit(0)


def koruma_gozlem_dongusu(root):
    global is_running
    print("Bot koruma tarayıcısı aktif...")

    # Dosya yolları için base_dir tespiti
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    click_resim_yolu = os.path.join(base_dir, 'assets', KORUMA_CLICK)

    while is_running:
        tespit_edilen = None
        for resim in KORUMA_RESIMLERI:
            if not is_running: break
            resim_yolu = os.path.join(base_dir, 'assets', resim)
            try:
                konum = py.locateOnScreen(resim_yolu, confidence=0.8)
                if konum is not None:
                    tespit_edilen = resim
                    break
            except py.ImageNotFoundException:
                continue
            except Exception:
                pass

        if tespit_edilen:
            print(f"\n🚨 BOT KORUMASI EKRANDA GÖRÜLDÜ: {tespit_edilen}")

            try:
                # 1. Adım: koruma1 veya koruma3 ise önce kendisine tıkla
                if tespit_edilen in ["koruma1.png", "koruma3.png"]:
                    resim_yolu = os.path.join(base_dir, 'assets', tespit_edilen)
                    ilk_konum = py.locateOnScreen(resim_yolu, confidence=0.8)
                    if ilk_konum is not None:
                        py.click(ilk_konum.left + ilk_konum.width // 2, ilk_konum.top + ilk_konum.height // 2)
                        time.sleep(4.5)

                # 2. Adım: koruma_click.png'ye tıkla (koruma2 için direkt buraya gelinir)
                click_konum = py.locateOnScreen(click_resim_yolu, confidence=0.8)
                if click_konum is not None:
                    py.click(click_konum.left + click_konum.width // 2, click_konum.top + click_konum.height // 2)
                    time.sleep(4.5)  # İşlemin ekrana yansıması için kısa bekleme
                else:
                    print("⚠️ koruma_click.png ekranda bulunamadı!")

            except Exception as e:
                print(f"Koruma tıklama sırasında hata: {e}")

            # 3. Adım: İşlem sonrası hala herhangi bir koruma görseli var mı kontrol et
            time.sleep(4.5)
            hala_koruma_var = False
            for resim in KORUMA_RESIMLERI:
                resim_yolu = os.path.join(base_dir, 'assets', resim)
                try:
                    if py.locateOnScreen(resim_yolu, confidence=0.8) is not None:
                        hala_koruma_var = True
                        break
                except:
                    pass

            # Sonuç değerlendirmesi
            if hala_koruma_var:
                print("🚨 Koruma geçilemedi, hala ekranda duruyor! Bot kapatılıyor...")
                uyari_mesaji = f"🚨 DİKKAT! Bot Koruması ({tespit_edilen}) atlatılamadı. Chrome kapatılıyor ve bot sonlandırılıyor!"
                # uc_kez_mesaj_gonder(uyari_mesaji)
                chrome_kapat()
                root.after(0, lambda: stop_bot(root))
                return
            else:
                print("✅ Koruma başarıyla tıklandı ve ekrandan kalktıl, bot çalışmaya devam ediyor.")

        for _ in range(3):
            if not is_running: break
            time.sleep(4.5)


# --- DİĞER BOT FONKSİYONLARI YORUM SATIRINA ALINDI ---
"""
def combine_close_boxes(boxes, tolerance=10):
    ...
def find_rightmost_bonus(bonus_positions):
    ...
def run_bot(bonusActive, status_label):
    ...
"""


def start_bot(bonus_var, status_label, start_btn, stop_btn, root):
    global is_running, koruma_thread
    if is_running:
        return

    is_running = True
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

    status_label.config(text="Durum: Sadece Bot Koruma Aktif", fg="blue")

    # Sadece bot koruma gözlemcisini başlat
    koruma_thread = threading.Thread(target=koruma_gozlem_dongusu, args=(root,))
    koruma_thread.daemon = True
    koruma_thread.start()


def main():
    root = tk.Tk()
    root.title("Klanlar Bot Koruma Modu")
    root.geometry("320x220")
    root.resizable(False, False)

    bonus_var = tk.BooleanVar()
    chk_bonus = tk.Checkbutton(root, text="Bonus Aktif Olsun (Pasif)", variable=bonus_var, font=("Arial", 11), state=tk.DISABLED)
    chk_bonus.pack(pady=15)

    status_label = tk.Label(root, text="Durum: Bekliyor...", font=("Arial", 10), fg="gray")
    status_label.pack(pady=5)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=15)

    stop_btn = tk.Button(btn_frame, text="Durdur", bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"), width=10,
                         command=lambda: stop_bot(root))
    stop_btn.pack(side=tk.RIGHT, padx=5)

    start_btn = tk.Button(btn_frame, text="Başlat", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=10,
                          command=lambda: start_bot(bonus_var, status_label, start_btn, stop_btn, root))
    start_btn.pack(side=tk.LEFT, padx=5)

    root.protocol("WM_DELETE_WINDOW", lambda: stop_bot(root))
    root.mainloop()


if __name__ == "__main__":
    main()