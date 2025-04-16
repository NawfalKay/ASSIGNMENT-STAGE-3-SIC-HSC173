import streamlit as st
import os
import requests
import cv2
from PIL import Image
from datetime import datetime

# Konfigurasi
ESP32_CAM_URL = "http://192.168.49.229:81/stream"  # Ganti sesuai IP ESP32-CAM kamu
UBIDOTS_TOKEN = "BBUS-ZYMsrjRHYXbLRigG1JqWtRBmjhpLls"
DEVICE_LABEL = "phaethon"
SAVE_DIR = "absensi_foto"

# Buat folder simpan foto jika belum ada
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

st.set_page_config(page_title="Absensi Siswa", layout="centered")
st.title("📸 Absensi Otomatis Siswa")

# Formulir input
nama_siswa = st.text_input("Nama Siswa:")
kelas = st.selectbox("Pilih Kelas:", ["Kelas 10", "Kelas 11", "Kelas 12"])

# Fungsi kirim absen ke Ubidots
def kirim_absen():
    url = f"http://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
    payload = {"absensi": 1}
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.status_code == 200

# Fungsi kamera & deteksi wajah
def mulai_absensi(nama_siswa, kelas):
    cap = cv2.VideoCapture(ESP32_CAM_URL)
    if not cap.isOpened():
        st.error("🚫 Tidak dapat membuka kamera ESP32-CAM.")
        return

    stframe = st.empty()
    sudah_absen = False
    foto_terambil = None

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while cap.isOpened() and not sudah_absen:
        ret, frame = cap.read()
        if not ret:
            st.error("🚫 Gagal mengambil frame dari kamera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if not sudah_absen:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(SAVE_DIR, f"{nama_siswa}{kelas}{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                foto_terambil = Image.open(filename)
                if kirim_absen():
                    st.success("✅ Absensi berhasil dikirim")
                else:
                    st.error("❌ Gagal mengirim absensi ke Ubidots")
                sudah_absen = True

        stframe.image(frame, channels="BGR", use_container_width=True)

    cap.release()
    if foto_terambil:
        st.image(foto_terambil, caption=f"Foto Absen: {nama_siswa} - {kelas}", use_container_width=True)

# Tombol untuk mulai absen
if st.button("Ambil Absen"):
    if nama_siswa and kelas:
        mulai_absensi(nama_siswa, kelas)
    else:
        st.warning("⚠ Harap isi Nama Siswa dan pilih Kelas terlebih dahulu!")