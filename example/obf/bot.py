import asyncio
import aiohttp
import time
import os
import sys
from colorama import Fore

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

BANNER = """
 ██╗  ██╗     █████╗     ██████╗     ██╗
 ██║ ██╔╝    ██╔══██╗    ██╔══██╗    ██║
 █████╔╝     ███████║    ██████╔╝    ██║
 ██╔═██╗     ██╔══██║    ██╔══██╗    ██║
 ██║  ██╗    ██║  ██║    ██████╔╝    ██║
 ╚═╝  ╚═╝    ╚═╝  ╚═╝    ╚═════╝     ╚═╝
"""

print(Fore.MAGENTA + BANNER)

ALLOWED_KEYS = ["lacthiengia",]

user_key = input("Vui lòng nhập key để sử dụng tool!: ")

with open("log.txt", "a", encoding="utf-8") as f:
    f.write("Gửi thành công vào kênh\n")

if user_key not in ALLOWED_KEYS:
    print("Key không hợp lệ!")
    sys.exit()
else:
    print("Key hợp lệ! Đã vào chế độ gửi!")

async def action_pool(tokens, id_channel, content, delays):
    print(f"Đang gửi đến kênh {id_channel}")

    async def send_message(token, id_channel, content, n_delay):
        token = str(token).strip()
        headers = {
            "Authorization": token,
        }
        data = {
            "content": content,
            "tts": False
        }

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), headers=headers) as ses:
            while True:
                try:
                    async with ses.post(url=f"https://discord.com/api/v9/channels/{str(id_channel)}/messages", data=data) as resp:
                        if 200 <= resp.status < 400:
                            print(f"[✅] Gửi Đến {id_channel} Thành Công | Token {token[:10]}... ({resp.status})")
                except Exception as e:
                    print(f"Lỗi: {e}")
                finally:
                    await asyncio.sleep(n_delay * 0.3)

    tasks = [asyncio.create_task(send_message(token.strip(), id_channel, content, delays[i])) for i, token in enumerate(tokens)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    cls()
    print(Fore.MAGENTA + BANNER)
    print("LAC THIEN GIA BAT BAI NO1 DISCORD!!!")

    # Nhập số lượng kênh và các ID
    so_kenh = int(input("Nhập số lượng kênh bạn muốn! "))
    ID_CHANNELS = []
    for i in range(so_kenh):
        id_channel = input(f"Nhập ID kênh số {i+1}: ")
        ID_CHANNELS.append(id_channel.strip())

    # Nhập file tokens và nội dung
    TXT_TOKEN = input("Nhập tên file chứa token (VD: tokens.txt): ")
    TXT_CONTENT = input("Nhập tên file chứa nội dung (VD: ngon1.txt): ")

    try:
        with open(TXT_TOKEN, "r", encoding="utf-8") as f:
            TOKENS = f.readlines()
    except Exception as e:
        print(f"Lỗi đọc {TXT_TOKEN}: {e}")
        time.sleep(5)
        sys.exit()

    try:
        with open(TXT_CONTENT, "r", encoding="utf-8") as f:
            CONTENT = f.read().strip()
            print("Nội dung:", CONTENT)
    except Exception as e:
        print(f"Lỗi đọc {TXT_CONTENT}: {e}")
        time.sleep(5)
        sys.exit()

    # Delay cho từng token
    DELAYS = []
    for i, token in enumerate(TOKENS):
        delay = int(input(f"Nhập delay cho token {i + 1} (giây): "))
        DELAYS.append(delay)

    while True:
        try:
            for id_channel in ID_CHANNELS:
                asyncio.run(action_pool(TOKENS, id_channel, CONTENT, DELAYS))
        except Exception as e:
            print("Gặp lỗi khi gửi, chờ 60s rồi thử lại...")
            print(e)
            time.sleep(60)
