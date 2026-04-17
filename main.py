import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
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
secret_role = "King of GAYS"

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

@bot.command()
async def hello(ctx):
    await ctx.send(f"hello {ctx.author.mention}")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name = secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}.")
    else:
        await ctx.send("Role does not exist.") 

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name = secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed.")
    else:
        await ctx.send("Role does not exist.")
bot.run(token, log_handler=handler, log_level=logging.DEBUG)