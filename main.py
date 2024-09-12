import pyrogram
import aiohttp

# API credentials
API_ID = 123456
API_HASH = "0123456789abcdef012345678"
BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
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
app = pyrogram.Client("ChatGPT-Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Start command
@app.on_message(pyrogram.filters.command("start"))
async def start(client, message):
    await message.reply_text("Hello! I am a ChatGPT Bot. I can chat with you. Send /help to know more about me.")


# Help command
@app.on_message(pyrogram.filters.command("help"))
async def help(client, message):
    await message.reply_text(
        "I am a ChatGPT Bot. I can chat with you. Send /ask, /bard, /gemini, /gemma, /mistral, or /llama to chat with me.")


# Chat command
@app.on_message(pyrogram.filters.command(['ask', 'bard', 'gemini', 'gemma', 'mistral', 'llama']))
async def chat(client, message):
    modal = message.command[0]
    if modal == 'ask':
        modal = 'bard'
    model_id = MODELS[modal]

    if len(message.command) > 1:
        query = message.text.split(' ', 1)[1]
    else:
        query = message.reply_to_message.text if message.reply_to_message else 'Hello!'

    txt = await message.reply_text("Processing...")

    async with aiohttp.ClientSession() as session:
        async with session.post(URL + "/models", params={'model_id': model_id, 'prompt': query}) as resp:
            json = await resp.json()
            if json['code'] == 0:
                return await txt.edit('Something went wrong, Please try again later. Sorry for the Inconvenience.')
            answer = json['content']
            await txt.delete()
            await message.reply(answer, quote=True)


# Run the bot
app.run()