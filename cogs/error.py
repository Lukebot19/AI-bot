try:

	from nextcord.ext import commands, application_checks
	import nextcord

except Exception as e:
	print(e)
	print("\n\n\nIMPOPRT ERROR\nRESTARTING NOW\n\n\n")


class ErrorHandler(commands.Cog):
	"""A cog for global error handling."""


	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""Error handling for the context commands"""


		message = ''
		if isinstance(error, commands.CommandOnCooldown):
			message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
		elif isinstance(error, commands.MissingPermissions):
			message = "You are missing the required permissions to run this command!"
		elif isinstance(error, commands.MissingRequiredArgument):
			message = f"Missing a required argument: {error.param.name}"

		elif isinstance(error, commands.ConversionError):
			message = str(error)
		elif isinstance(error, commands.CommandNotFound):
			pass
		elif isinstance(error, commands.CommandInvokeError):
			print(str(error.args[0]))
		elif isinstance(error, commands.CheckFailure):

			message = (
					f'{ctx.command.name} is disabled in this server. Contact an admin if you think it should be enabled.')

		if message == '':
			print("Invalid command")
			return
		try:

			embed = nextcord.Embed(title="Error Occurred",
				                       description=message, colour=nextcord.Colour.red())
			await ctx.reply(embed=embed)
		except:
			embed = nextcord.Embed(
					title="Error Occurred", description='This is likely an issue on Discords end, please check Discord official status [here](https://discordstatus.com) for any errors. \n \n If everything is running fine, please join Atoms support server [here](https://discord.com/invite/dbxjZVECKt) and report the error. \nThank you!', colour=nextcord.Colour.red())

			await ctx.reply(embed=embed)
		return

	@commands.Cog.listener()
	async def on_application_command_error(self, interaction, error):

		emotes = False

		if emotes:
			emote = "<a:no:965924366862909440>"
		else:
			emote = "❌"


		if isinstance(error, application_checks.ApplicationMissingPermissions):
			await interaction.send(f"{emote} Command: `{interaction.application_command.name}` requires the `{error.missing_permissions[0]}` permission.", ephemeral=True)
		elif isinstance(error, nextcord.ApplicationCheckFailure):
			await interaction.send(f"{emote} Command: `{interaction.application_command.name}` is disabled in this server.", ephemeral=True)

		elif isinstance(error, nextcord.ApplicationInvokeError):
			if error.args[0] == "Command raised an exception: InvalidVoiceChannel: No channel to join. Please either specify a valid channel or join one.":
				await interaction.edit_original_message(content=f"<a:no:965924366862909440> {error.original.args[0]}")
			else:

				await interaction.send(f"{emote} An unknwon error has occoured. {error}", ephemeral=True)
		else:
			try:
				await interaction.edit_original_message(content=f"{emote} An unknwon error has occoured. {error}")
			except:
				try:
					await interaction.send(f"{emote} An unknwon error has occoured. {error}", ephemeral=True)

				except:
					print(error)
		return

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))

