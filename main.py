import nextcord
from nextcord.ext import commands
import os

intents  = nextcord.Intents.default()

class MyBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')
    
    async def on_ready(self):
        print('Bot is ready.')

client = MyBot(command_prefix='!', intents=intents)

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))