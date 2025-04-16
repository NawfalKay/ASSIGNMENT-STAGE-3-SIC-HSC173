import streamlit as st
import random
import datetime
import os

# Buat folder simpan foto jika belum ada
SAVE_DIR = "kalah_captures"
os.makedirs(SAVE_DIR, exist_ok=True)

st.title("🎌 Game Suit Jepang + Kamera Rahasia 😏")

options = ["✊ Batu", "✌️ Gunting", "🖐️ Kertas"]
rules = {
    "✊ Batu": "✌️ Gunting",
    "✌️ Gunting": "🖐️ Kertas",
    "🖐️ Kertas": "✊ Batu"
}

player_choice = st.selectbox("Pilih tanganmu:", options)

# Kamera (tidak terlihat)
camera_input = st.camera_input(" ", label_visibility="collapsed")

if st.button("Suit!"):
    computer_choice = random.choice(options)
    st.write(f"🤖 Komputer memilih: **{computer_choice}**")
    st.write(f"🧑 Kamu memilih: **{player_choice}**")

    if player_choice == computer_choice:
        st.info("⚖️ Seri!")
    elif rules[player_choice] == computer_choice:
        st.success("🎉 Kamu Menang!")
        st.balloons()
    else:
        st.error("💥 Kamu Kalah! Kamera aktif secara diam-diam... 😳")
        # Simpan gambar kamera jika tersedia
        if camera_input:
            filename = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(os.path.join(SAVE_DIR, filename), "wb") as f:
                f.write(camera_input.getbuffer())
            st.success("📸 Foto berhasil disimpan diam-diam!")

