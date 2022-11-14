import discord
from discord import app_commands, ui
from discord.ext import commands
from datetime import datetime
from google_commands.update_anon import anon_append
from google_commands.get_member import get_member

GUILD = discord.Object(id=1009880371220992000)

class AnonymousHotline(ui.Modal, title="Anonymous Hotline"):
    ANON_MESSAGE = discord.ui.TextInput(
        label='Anonymous Hotline',
        placeholder='Please report any concerns you have in regards to the club...',
        required=True,
        style=discord.TextStyle.paragraph,
        max_length=300)


    async def on_submit(self, interaction: discord.Interaction):
        now = datetime.now()

        anon_append(now.strftime("%m/%d/%Y %H:%M:%S"), self.ANON_MESSAGE.value)

        await interaction.response.send_message(f'Thanks for your Submission, {interaction.user.name}', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        print(error)


class HotlineButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Activate Hotline",style=discord.ButtonStyle.success)
    async def active_button(self, button:discord.ui.Button,interaction:discord.Interaction):
        pass
    # async def callback(self, interaction : discord.Interaction): 
    #     await interaction.response.send_modal(AnonymousHotline())
        
class Hotline(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hotline Command Loaded..")

    @app_commands.command(name="hotline", description="Use this command to report any concerns you have in regards to the club")
    async def hotline(self, interaction : discord.interactions):
        await interaction.response.send_modal(AnonymousHotline())

    @commands.command()
    async def send_hotline(self, ctx):
        print("Hotline Command Sent")
        channel =  self.bot.get_channel(1035676539376914463)
        await channel.send("This is an Automated Test for the Hotline Feature.", view=HotlineButton())

async def setup(bot):
    await bot.add_cog(Hotline(bot), guilds=[GUILD])