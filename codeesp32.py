import network
import urequests
import time
from machine import Pin, ADC, I2C
import dht
from ssd1306 import SSD1306_I2C

# WiFi Config
SSID = "Furina De Fontaine"
PASSWORD = "31415900"

# Ubidots Config
UBIDOTS_TOKEN = "BBUS-ZYMsrjRHYXbLRigG1JqWtRBmjhpLls"
DEVICE_NAME = "x`"
UBIDOTS_URL = "http://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_NAME)

# OLED setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 64, i2c)

# Inisialisasi sensor
dht_sensor = dht.DHT11(Pin(15))
mic_sensor = ADC(Pin(34))
mic_sensor.atten(ADC.ATTN_11DB)  # 0 - 3.3V

# Variabel status WiFi global
wifi_connected = False

# Fungsi koneksi WiFi lebih stabil
def connect_wifi():
    global wifi_connected
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wlan.disconnect()
        time.sleep(1)

    print("Menghubungkan ke WiFi...")
    wlan.connect(SSID, PASSWORD)

    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        print("Tunggu koneksi... ({}s)".format(11 - timeout))
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("✅ Terhubung ke WiFi:", wlan.ifconfig())
        wifi_connected = True
    else:
        print("❌ Gagal terhubung ke WiFi.")
        wifi_connected = False

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

# Jalankan WiFi
connect_wifi()

# Timer kirim data tiap 5 detik
last_sent = time.ticks_ms()

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        sound = mic_sensor.read()

        print("Suhu:", temp, "°C | Kelembaban:", hum, "% | Suara:", sound)

        # Tampilkan realtime ke OLED
        oled.fill(0)
        oled.text("WiFi: " + ("Terhubung" if wifi_connected else "Gagal"), 0, 0)
        oled.text("Suhu: {} C".format(temp), 0, 15)
        oled.text("Lembab: {} %".format(hum), 0, 30)
        oled.text("Suara: {}".format(sound), 0, 45)
        oled.show()

        # Kirim ke Ubidots tiap 5 detik
        if time.ticks_diff(time.ticks_ms(), last_sent) > 5000:
            send_to_ubidots(temp, hum, sound)
            last_sent = time.ticks_ms()

    except Exception as e:
        print("⚠️ Error:", e)

    time.sleep(0.1)  # Realtime refresh tapi hemat CPU

