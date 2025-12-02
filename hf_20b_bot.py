# 이거 그대로 복붙 (HF_TOKEN, DISCORD_TOKEN은 비워둬!)
import discord
from discord.ext import commands
import requests
import asyncio
import os

HF_TOKEN = os.environ.get("HF_TOKEN")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

MODEL = "openai/gpt-oss-20b"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

API_URL = "https://router.huggingface.co/v1/chat/completions"
headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

async def ask_hf(message):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "너는 친절하고 재치 있는 한국어 AI야. Reasoning: medium."},
            {"role": "user", "content": message}
        ],
        "max_tokens": 768,
        "temperature": 0.8
    }
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=90)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"에러: {r.status_code} (모델 로딩 중일 수 있어... 30초 후 다시 시도!)"
    except:
        return "요청 실패... 다시 시도해줘!"

@bot.event
async def on_ready():
    print(f"{bot.user} 20B 봇 온라인! 🔥")

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        clean = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not clean: clean = "안녕!"
        async with message.channel.typing():
            reply = await ask_hf(clean)
            await message.reply(reply, mention_author=True)
    await bot.process_commands(message)

@bot.command()
async def oss(ctx, *, q):
    async with ctx.typing():
        reply = await ask_hf(q)
        await ctx.reply(reply)

bot.run(DISCORD_TOKEN)
