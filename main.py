import os
import logging
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API credentials from environment variables
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "0123456789abcdef012345678")
BOT_TOKEN = os.getenv("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
URL = "https://lexica.qewertyy.dev"

# Model mapping
MODELS = {
    'ask': 'bard',
    'bard': 20,
    'gemini': 20,
    'geminiVission': 20,
    'gemma': 20,
    'mistral': 21,
    'llama': 14,
}

# Initialize bot client
app = Client("ChatGPT-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def fetch_response(model_id: int, query: str) -> str:
    try:
        async with ClientSession() as session:
            async with session.post(URL + "/models", params={'model_id': model_id, 'prompt': query}) as resp:
                json = await resp.json()
                if json['code'] == 0:
                    return 'Something went wrong, Please try again later. Sorry for the Inconvenience.'
                return json['content']
    except Exception as e:
        logger.error(f"Error fetching response: {e}")
        return 'An error occurred while processing your request. Please try again later.'

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("Hello! I am a ChatGPT Bot. I can chat with you. Send /help to know more about me.")

@app.on_message(filters.command("help"))
async def help(client: Client, message: Message):
    await message.reply_text(
        "I am a ChatGPT Bot. I can chat with you. Send /ask, /bard, /gemini, /gemma, /mistral, or /llama to chat with me."
    )

@app.on_message(filters.command(['ask', 'bard', 'gemini', 'gemma', 'mistral', 'llama']))
async def chat(client: Client, message: Message):
    modal = message.command[0]
    if modal == 'ask':
        modal = 'bard'
    model_id = MODELS[modal]

    query = message.text.split(' ', 1)[1] if len(message.command) > 1 else (message.reply_to_message.text if message.reply_to_message else 'Hello!')
    txt = await message.reply_text("Processing...")

    answer = await fetch_response(model_id, query)
    await txt.delete()
    await message.reply(answer, quote=True)

@app.on_message(filters.private)
async def private_message(client: Client, message: Message):
    query = message.text
    model_id = MODELS['bard']  # Default model
    txt = await message.reply_text("Processing...")

    answer = await fetch_response(model_id, query)
    await txt.delete()
    await message.reply(answer, quote=True)

# Run the bot
app.run()