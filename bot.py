import os
import discord
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')
            
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTA3ODQyNTQ5NzAzOTU0ODU1Nw.GxTuHo.fwtZEyPG8a56kj0DmMg9-0LxZ2kNa0urIc162o')
