import os

import requests
import json
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

async def random_ph_post():
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

client.run(token)
