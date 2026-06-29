import asyncio
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- CONFIGURATION (Token aur Strings yahan dal diye hain) ---
BOT_TOKEN = '8858492932:AAEU3vCZzX5KmBJmTX4RZzrr7qhfr81aVRA'
# Yahan apni String Session daal do:
SESSION1 = 'PAHLE_ACCOUNT_KA_STRING_CODE_YAHAN_PASTE_KARO'
SESSION2 = 'DUSRE_ACCOUNT_KA_STRING_CODE_YAHAN_PASTE_KARO'

API_DATA = [
    {'id': 21552435, 'hash': '5b108bd2fdd31c0c34bc65f24a5216a0', 'session_str': SESSION1, 'reactions': ['🔥', '👍', '❤️']},
    {'id': 29308061, 'hash': '462de3dfc98fd938ef9c6ee31a72d099', 'session_str': SESSION2, 'reactions': ['💯', '🎉', '🤩']}
]

BAD_KEYWORDS = ['porn', 'xxx', 'illegal', 'hack', 'https://', 'http://', 'forward']

# --- Flask Server ---
app = Flask(__name__)
@app.route('/')
def home(): return "Kushal Bot is Running!"
def run_server(): app.run(host='0.0.0.0', port=8080)

# --- Bot Logic ---
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
    bot = TelegramClient('bot', 21552435, '5b108bd2fdd31c0c34bc65f24a5216a0').start(bot_token=BOT_TOKEN)
    
    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        await event.respond("👋 **Welcome Kushal!**\n\nKushal Security & Reaction Shield is Active.\nSelect your mode:", 
            buttons=[[Button.inline("➕ Add for Group", b'group'), Button.inline("➕ Add for Channel", b'channel')]])

    await asyncio.gather(run_client(API_DATA[0]), run_client(API_DATA[1]), bot.run_until_disconnected())

if __name__ == '__main__':
    asyncio.run(main())
