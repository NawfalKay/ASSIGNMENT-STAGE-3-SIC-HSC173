import network
import urequests
import time
from machine import Pin, ADC, I2C
import dht
from ssd1306 import SSD1306_I2C

# WiFi Config
SSID = "Furina"
PASSWORD ="rasquerust"

# Ubidots Config
UBIDOTS_TOKEN = "BBUS-ZYMsrjRHYXbLRigG1JqWtRBmjhpLls"
DEVICE_NAME = "phaethon"
UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_NAME)

# Fungsi koneksi WiFi lebih stabil
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(1)

    if not wlan.isconnected():
        print("Menghubungkan ke WiFi...")
        wlan.connect(SSID, PASSWORD)

        timeout = 10  # tunggu maksimal 10 detik
        while not wlan.isconnected() and timeout > 0:
            print("Tunggu koneksi... ({}s)".format(11 - timeout))
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("✅ Terhubung ke WiFi:", wlan.ifconfig())
    else:
        print("❌ Gagal terhubung ke WiFi.")

# Inisialisasi sensor
dht_sensor = dht.DHT11(Pin(15))
mic_sensor = ADC(Pin(34))
mic_sensor.atten(ADC.ATTN_11DB)  # 0 - 3.3V

# OLED setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

# Fungsi kirim ke Ubidots
def send_to_ubidots(temp, hum, sound):
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "temperature": temp,
        "humidity": hum,
        "sound": sound
    }
    try:
        response = urequests.post(UBIDOTS_URL, json=data, headers=headers)
        print("✅ Data terkirim:", response.text)
        response.close()
    except Exception as e:
        print("❌ Gagal mengirim ke Ubidots:", e)

# Jalankan
connect_wifi()

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        sound = mic_sensor.read()

        print("Suhu:", temp, "°C | Kelembaban:", hum, "% | Suara:", sound)

        # Tampilkan di OLED
        oled.fill(0)
        oled.text("Suhu: {} C".format(temp), 0, 0)
        oled.text("Lembab: {} %".format(hum), 0, 10)
        oled.text("Suara: {}".format(sound), 0, 20)
        oled.show()

        # Kirim ke Ubidots
        send_to_ubidots(temp, hum, sound)

    except Exception as e:
        print("⚠ Error:", e)

    time.sleep(5)
