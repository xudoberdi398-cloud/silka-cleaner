from telethon import TelegramClient, events
import re
import asyncio
import os

# Sizning ma'lumotlaringiz
api_id = 33589874
api_hash = '64603515e3d7f661c9773e8ba47678aa'
phone_number = '+998950952517'

# Server qayta yonganda qaytadan kod so'ramasligi uchun string sessiya
# (Buni birozdan keyin Termux'dan olib bu yerga qo'yamiz)
session_string = "BU_YERGA_TERMUXDAN_OLINGAN_STRING_QOYILADI"

if session_string != "BU_YERGA_TERMUXDAN_OLINGAN_STRING_QOYILADI":
    from telethon.sessions import StringSession
    client = TelegramClient(StringSession(session_string), api_id, api_hash)
else:
    client = TelegramClient('shaxsiy_silka_tozalagich', api_id, api_hash)

@client.on(events.NewMessage())
async def handle_all_private_messages(event):
    if event.is_private:
        message_text = event.message.message or ""
        has_link = bool(re.search(r'(https?://[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+|@[a-zA-Z0-9_]+)', message_text.lower()))
        if has_link:
            try:
                await event.delete(revoke=True) 
                print(f"[TOZALANDI] Silka o'chirildi.")
            except Exception:
                pass

async def main():
    await client.start(phone=phone_number)
    print("\n🎉 Serverda tizimga kirdi!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Render server o'chib qolmasligi uchun vaqtincha port ochib qo'yamiz
    from threading import Thread
    import http.server
    import socketserver
    
    def run_dummy_server():
        port = int(os.environ.get("PORT", 8080))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
            
    Thread(target=run_dummy_server, daemon=True).start()
    
    asyncio.run(main())
                                    
