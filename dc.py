import os
import time
import random
import requests
from colorama import Fore, init

# Inisialisasi colorama
init(autoreset=True)

# 🎯 Banner & Penjelasan Fungsi
def show_banner():
    banner = f"""{Fore.GREEN}
    ╔══════════════════════════════════════════╗
    ║      🔥 DISCORD AUTO MESSAGING BOT 🔥    ║
    ║         🚀 Script by: Reboy69 🚀         ║
    ╠══════════════════════════════════════════╣
    ║ Fungsi:                                  ║
    ║ ✅ Mengirim pesan otomatis ke channel    ║
    ║ ✅ Menghapus pesan setelah beberapa detik║
    ║ ✅ Looping otomatis dengan jeda waktu    ║
    ║ ✅ Bisa dihentikan dengan CTRL + C       ║
    ╚══════════════════════════════════════════╝
    {Fore.RESET}"""
    print(banner)
    time.sleep(1)

# 📌 Input dari pengguna
def get_user_input():
    channel_id = input(Fore.CYAN + "📢 Masukkan ID channel: ").strip()
    waktu_hapus = int(input(Fore.CYAN + "⏳ Set Waktu Hapus Pesan (detik): "))
    waktu_kirim = int(input(Fore.CYAN + "📩 Set Waktu Kirim Pesan (detik): "))
    return channel_id, waktu_hapus, waktu_kirim

# ⏳ Countdown sebelum mulai
def countdown():
    for i in range(3, 0, -1):
        print(Fore.YELLOW + f"🚀 Memulai dalam {i} detik...")
        time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')

# 📂 Membaca file
def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ✉️ Mengirim pesan
def send_message(channel_id, token, messages):
    payload = {'content': random.choice(messages)}
    headers = {'Authorization': token}
    response = requests.post(
        f"https://discord.com/api/v9/channels/{channel_id}/messages",
        data=payload,
        headers=headers
    )
    print(Fore.GREEN + "✅ Pesan terkirim: " + Fore.YELLOW + payload['content'])
    return response

# 🔍 Mengambil pesan terbaru
def get_latest_message(channel_id, token):
    headers = {'Authorization': token}
    response = requests.get(
        f'https://discord.com/api/v9/channels/{channel_id}/messages',
        headers=headers
    )
    if response.status_code == 200:
        messages = response.json()
        return messages[0]['id'] if messages else None
    return None

# 🗑️ Menghapus pesan
def delete_message(channel_id, token, message_id):
    headers = {'Authorization': token}
    response = requests.delete(
        f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}',
        headers=headers
    )
    if response.status_code == 204:
        print(Fore.RED + f'🗑️ Pesan dengan ID {message_id} berhasil dihapus')
    else:
        print(Fore.RED + f'❌ Gagal menghapus pesan {message_id}: {response.status_code}')

# 🔄 Main loop
def main():
    show_banner()
    channel_id, waktu_hapus, waktu_kirim = get_user_input()
    countdown()

    messages = read_file("pesan.txt")
    token = read_file("token.txt")[0]

    try:
        while True:
            send_message(channel_id, token, messages)
            time.sleep(waktu_hapus)

            message_id = get_latest_message(channel_id, token)
            if message_id:
                delete_message(channel_id, token, message_id)

            time.sleep(waktu_kirim)
    except KeyboardInterrupt:
        print(Fore.RED + "\n❌ Dihentikan oleh pengguna.")

if __name__ == "__main__":
    main()
