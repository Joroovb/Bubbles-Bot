import os

import requests
import json
import discord
import time
from dotenv import load_dotenv
from discord.ext import commands

## Bot Setup
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

## Print to console on bot connect
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

## Welcome new members and read them the rules
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    time.sleep(1)
    await channel.send(f"Welkom {member.mention}! Zeg !accept")

## Allow users into the server after accepting rules
@client.command()
async def accept(ctx):
    member = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="Programmer")
    await addrole(ctx, member, role)

## Post top Programming humor meme
@client.command()
async def random_ph_post(ctx):
    # Get weekly top 10 posts of r/programminghumor
    url = 'https://www.reddit.com/r/programminghumor/top/.json?t=week&limit=10'
    req = requests.get(url, headers = {'User-agent': 'your bot 0.1'})
    res = json.loads(req.text)
    posts = res["data"]["children"]

    # Get image from top post and post in Discord Channel
    img_data = requests.get(posts[0]["data"]["url"]).content
    with open('top_image.jpg', 'wb') as handler:
        handler.write(img_data)
    channel = client.guilds[0].text_channels[0]
    await channel.send('Hello', file=discord.File('top_image.jpg'))

## Utility methods
async def addrole(ctx, member : discord.Member, role : discord.Role):
    await member.add_roles(role)

client.run(token)
