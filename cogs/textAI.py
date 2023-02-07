import nextcord
from nextcord.ext import commands
import openai
import os

class textAI(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="text", description="Get a response from OpenAI's text AI")
    async def textAI(self, interaction, query:str = nextcord.SlashOption(description="Enter your query here", required=True)):
        
        await interaction.response.defer(with_message=True)
        reponse = openai.Completion.create(
            api_key=os.getenv('OPENAI_API_KEY'),
            model = "text-davinci-003",
            prompt = query,
            temperature = 0.9,
            max_tokens = 4096,
            top_p = 0.3,
            frequency_penalty = 0.5,
            presence_penalty = 0.0
        )
        embed = nextcord.Embed(
            title=query,
            description=f"```{reponse['choices'][0]['text']}```",
        )
        await interaction.send(embed=embed)

def setup(client):
    client.add_cog(textAI(client))