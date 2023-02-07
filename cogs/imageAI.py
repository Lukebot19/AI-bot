import nextcord
from nextcord.ext import commands
import openai
import os


class imageAI(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="image", description="Get a response from OpenAI's image AI")
    async def textAI(self, interaction, query: str = nextcord.SlashOption(description="What should the image be of?", required=True)):

        await interaction.response.defer(with_message=True)
        response = openai.Image.create(
            api_key=os.getenv('OPENAI_API_KEY'),
            prompt=f"Create an image of a {query}",
            n=1,
            size="1024x1024"
        )


        # Send the generated image to the channel
        embed = nextcord.Embed(
            title=query,
            description="some text"
        )
        embed.set_image(url=response['data'][0]['url'])
        await interaction.send(embed=embed)


def setup(client):
    client.add_cog(imageAI(client))
