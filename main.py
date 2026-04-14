import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import time
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

load_dotenv()
#token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler('discord.log','w','utf-8')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot('!',intents=intents)

# List of censored words
CENSORED_WORDS = [
    "praneet",
    "pregu"
]

@bot.event
async def on_ready():
    print(f"we are ready to go in, {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    print(f"Message received: {message.author} - {message.content}")  # DEBUG
    if message.author == bot.user:
        return 
    
    # Check if any censored word is in the message
    message_lower = message.content.lower()
    for word in CENSORED_WORDS:
        if word in message_lower:
            await message.delete()
            await message.channel.send(f"{message.author.mention} - dont use the word!")
            break  # Stop checking after first match
    
    await bot.process_commands(message)

#bot.run(token,log_handler=handler, log_level=logging.DEBUG)
keep_alive()
time.sleep(60)
bot.run(token, log_handler=handler, log_level=logging.DEBUG)