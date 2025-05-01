import discord
import aiohttp
import asyncio

# Replace with your actual bot token
TOKEN = 'insert bot token here'

# Discord intents setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Ollama local server settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


async def query_ollama(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,      # More consistent responses
            "num_ctx": 4096,         # Bigger context window
            "num_predict": 1024      # More text generated
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(OLLAMA_URL, json=payload, headers=headers) as response:
            data = await response.json()
            reply = data.get("response", "No response from model.")
            # Automatically wrap code responses
            if "```" not in reply and ("def " in reply or "import " in reply or "class " in reply):
                reply = f"```python\n{reply}\n```"
            return reply


@client.event
async def on_ready():
    print(f'🤖 Bot connected as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content

    if content.startswith('!ask '):
        question = content[5:]
        thinking = await message.channel.send("💬 Thinking...")
        reply = await query_ollama(f"Answer this cybersecurity question clearly and briefly: {question}")
        await thinking.edit(content=reply)

    elif content.startswith('!summarize '):
        text = content[11:]
        thinking = await message.channel.send("📝 Summarizing...")
        reply = await query_ollama(f"Summarize this cybersecurity-related text in simple words: {text}")
        await thinking.edit(content=reply)

    elif content.startswith('!quiz '):
        topic = content[6:]
        thinking = await message.channel.send("📚 Generating quiz...")
        prompt = (
            f"Create a 5-question multiple choice quiz on the topic '{topic}' for cybersecurity students. "
            "Each question should have 4 options (a–d) and provide the correct answer below each question."
        )
        reply = await query_ollama(prompt)
        await thinking.edit(content=reply)


if __name__ == '__main__':
    client.run(TOKEN)
