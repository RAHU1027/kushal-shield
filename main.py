import os
import asyncio
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- CONFIGURATION ---
BOT_TOKEN = '8858492932:AAEU3vCZzX5KmBJmTX4RZzrr7qhfr81aVRA'

# --- STRING SESSIONS ---
SESSION1 = '''BQE1hZwAGi2-m_y-td38cmRGtB76YEqV3lSOt9ReR1UeOLb6D6Wxj9tZjnMkOvfVgp_XFZh0bft5mp8xLC31Y1EctX8arYxkn64Nrn35QsSnGUtosB8asH8yHLsCvWkv6EHT5BUfYujlsH0EM-yljv0Bfc8eyRFP6QisB5v1C2JCjlnIWZVjgtlWm7YB--54V-SmNH0rXaGdXJ1jFOVInX5eEXbyvdctJDoQJr-G3bKMd9Yt-LIstU3xwI-UgzHKVLx_oBVWOHPV3AkaKNExRYNoIPQwGKDzhpKoNt5N-5mY8-lsaBf69gq_FSnNl-IsN8n5HhTyanjEYUT3HLKND4hk-P96UAAAAAHTR-i_AA'''
SESSION2 = '''BQHycQwABmLIvjVlpgOpFs7bFi3VPm_NSrMvuXgJ6gVsbjfEMEzJpRrkL38IuQOE8sAgnKpHJog-E59Ku-iqwsE1zIP0C0D3Qms5Q0uTpAAUYe8PCJmePuKZ-e4kcRwKNXWLf9Mw1FOBFPNflpM1IEE60xEnZowb49VhHfYH6trh-5RNRRQP4vpK61NeERcfs5uRc41jhq6aOY0u36mPIl-JkQ5Uq5Kep8hurz_E9IzW2_wxummbfKh-g5qwQuL2ls4xrazgMCdy5rtfhQZ4Lj7EGLZZVz_WbbPlKprRk3IZcEPgMeViuB7Uaf7W8oMlgGYMo9BAuxs72NxLEFdbwaA9CqIkLwAAAAHJRoKvAA'''

API_DATA = [
    {'id': 21552435, 'hash': '5b108bd2fdd31c0c34bc65f24a5216a0', 'session_str': SESSION1, 'reactions': ['🔥', '👍', '❤️']},
    {'id': 29308061, 'hash': '462de3dfc98fd938ef9c6ee31a72d099', 'session_str': SESSION2, 'reactions': ['💯', '🎉', '🤩']}
]

BAD_KEYWORDS = ['porn', 'xxx', 'illegal', 'hack', 'https://', 'http://', 'forward', 'gali', 'abuse']

# --- FLASK SERVER (24/7) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Kushal Bot is Alive!"
def run_server(): app.run(host='0.0.0.0', port=8080)

# --- BOT LOGIC ---
async def run_client(data):
    client = TelegramClient(StringSession(data['session_str']), data['id'], data['hash'])
    await client.start()
    
    @client.on(events.NewMessage)
    async def handler(event):
        text = event.raw_text.lower()
        if any(word in text for word in BAD_KEYWORDS):
            try: await event.delete()
            except: pass
            return
        try:
            for r in data['reactions']:
                await client.send_reaction(event.chat_id, event.id, r)
                await asyncio.sleep(0.3)
        except: pass
    await client.run_until_disconnected()

async def main():
    Thread(target=run_server).start()
    bot = TelegramClient('bot', 21552435, '5b108bd2fdd31c0c34bc65f24a5216a0')
    await bot.start(bot_token=BOT_TOKEN)
    
    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        await event.respond("👋 **Welcome Kushal!**\n\nKushal Security & Reaction Shield is Active.", 
            buttons=[[Button.inline("➕ Add for Group", b'group'), Button.inline("➕ Add for Channel", b'channel')]])

    await asyncio.gather(run_client(API_DATA[0]), run_client(API_DATA[1]), bot.run_until_disconnected())

if __name__ == '__main__':
    asyncio.run(main())
