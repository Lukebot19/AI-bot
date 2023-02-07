import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
    
    async def on_ready(self):
        print('Bot is ready.')
        await self.change_presence(activity=nextcord.Game(name='with nextcord'))


client = MyBot(command_prefix='!', intents=nextcord.Intents.default())

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))