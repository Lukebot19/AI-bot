try:
	from nextcord.ext import commands
	import nextcord
	from main import getLang, updateInteraction
except Exception as e:
	print(e)
	print("\n\n\nIMPOPRT ERROR\nRESTARTING NOW\n\n\n")


class ErrorHandler(commands.Cog):
	"""A cog for global error handling."""

	def __init__(self, bot: commands.Bot, mDB):
		self.bot = bot
		self.mDB = mDB

	@commands.Cog.listener()
	async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""Error handling for the context commands"""

		lang = getLang(ctx.guild)
		updateInteraction()

		message = ''
		if isinstance(error, commands.CommandOnCooldown):
			if lang == "eng":
				message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
			elif lang == "viet":
				message = f"Lệnh này đang trong thời gian hồi chiêu. Vui lòng thử lại sau {round(error.retry_after, 1)} giây."
		elif isinstance(error, commands.MissingPermissions):
			if lang == "eng":
				message = "You are missing the required permissions to run this command!"
			elif lang == "viet":
				message = "Bạn đang thiếu các quyền cần thiết để chạy lệnh này!"
		elif isinstance(error, commands.MissingRequiredArgument):
			if lang == "eng":
				message = f"Missing a required argument: {error.param.name}"
			elif lang == "viet":
				message = f"Missing a required argument: {error.param.name}"
		elif isinstance(error, commands.ConversionError):
			message = str(error)
		elif isinstance(error, commands.CommandNotFound):
			pass
		elif isinstance(error, commands.CommandInvokeError):
			print(str(error.args[0]))
		elif isinstance(error, commands.CheckFailure):
			if lang == "eng":
				message = (
					f'{ctx.command.name} is disabled in this server. Contact an admin if you think it should be enabled.')
			elif lang == "viet":
				message = (
					f'{ctx.command.name} bị tắt trong máy chủ này. Liên hệ với quản trị viên nếu bạn nghĩ rằng nó nên được kích hoạt.')
		else:
			if lang == "eng":
				message = f"Oh no! Something went wrong while running the command! Error: {error}"
			elif lang == "viet":
				message = f"Ôi không! Đã xảy ra lỗi khi chạy lệnh! Lỗi: {error}"
		if message == '':
			print("Invalid command")
			return
		try:
			if lang == "eng":
				embed = nextcord.Embed(title="Error Occurred",
				                       description=message, colour=nextcord.Colour.red())
			elif lang == "viet":
				embed = nextcord.Embed(
					title="Xảy ra lỗi", description=message, colour=nextcord.Colour.red())
			await ctx.reply(embed=embed)
		except:
			if lang == "eng":
				embed = nextcord.Embed(
					title="Error Occurred", description='This is likely an issue on Discords end, please check Discord official status [here](https://discordstatus.com) for any errors. \n \n If everything is running fine, please join Atoms support server [here](https://discord.com/invite/dbxjZVECKt) and report the error. \nThank you!', colour=nextcord.Colour.red())
			elif lang == "viet":
				embed = nextcord.Embed(
					title="Xảy ra lỗi", description='Đây có thể là sự cố khi kết thúc Discords, vui lòng kiểm tra trạng thái chính thức của Discord [nơi đây](https://discordstatus.com) cho bất kỳ lỗi nào. \n \n Nếu mọi thứ đang chạy tốt, vui lòng tham gia máy chủ hỗ trợ của Atoms [nơi đây](https://discord.com/invite/dbxjZVECKt) và báo cáo lỗi. \nCảm ơn bạn!', colour=nextcord.Colour.red())
			await ctx.reply(embed=embed)
		return

	@commands.Cog.listener()
	async def on_application_command_error(self, interaction, error):

		emotes = False

		lang = getLang(interaction.guild)
		updateInteraction()
		if emotes:
			emote = "<a:no:965924366862909440>"
		else:
			emote = "❌"

		if isinstance(error, nextcord.ext.application_checks.ApplicationMissingPermissions):
			if lang == "eng":
				await interaction.send(f"{emote} Command: `{interaction.application_command.name}` requires the `{error.missing_permissions[0]}` permission.", ephemeral=True)
			elif lang == "viet":
				await interaction.send(f"{emote} Yêu cầu: `{interaction.application_command.name}` yêu cầu `{error.missing_permissions[0]}` sự cho phép.", ephemeral=True)
		elif isinstance(error, nextcord.ApplicationCheckFailure):
			if lang == "eng":
				await interaction.send(f"{emote} Command: `{interaction.application_command.name}` is disabled in this server.", ephemeral=True)
			elif lang == "viet":
				await interaction.send(f"{emote} Yêu cầu: `{interaction.application_command.name}` bị tắt trong máy chủ này.", ephemeral=True)
		elif isinstance(error, nextcord.ApplicationInvokeError):
			if error.args[0] == "Command raised an exception: InvalidVoiceChannel: No channel to join. Please either specify a valid channel or join one.":
				await interaction.edit_original_message(content=f"<a:no:965924366862909440> {error.original.args[0]}")
			else:
				if lang == "eng":
					await interaction.send(f"{emote} An unknwon error has occoured. {error}", ephemeral=True)
				elif lang == "viet":
					await interaction.send(f"{emote} Đã xảy ra một lỗi không đáng có. {error}", ephemeral=True)
		else:
			try:
				if lang == "eng":
					await interaction.edit_original_message(content=f"{emote} An unknwon error has occoured. {error}")
				elif lang == "viet":
					await interaction.edit_original_message(content=f"{emote} Đã xảy ra một lỗi không đáng có. {error}")
			except:
				try:
					if lang == "eng":
						await interaction.send(f"{emote} An unknwon error has occoured. {error}", ephemeral=True)
					elif lang == "viet":
						await interaction.send(f"{emote} Đã xảy ra một lỗi không đáng có. {error}", ephemeral=True)
				except:
					print(error)
		return


def setup(bot: commands.Bot, mDB):
    bot.add_cog(ErrorHandler(bot, mDB))
