import discord
from discord import app_commands, ui
import json
import sqlite3
from datetime import datetime
from google_commands.update_anon import anon_append
from google_commands.get_member import get_member

config = json.loads(open("tempConfig.json").read())
GUILD = discord.Object(id=1009880371220992000)

class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

intents = discord.Intents.default()
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

@client.event
async def ban(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'Banned {member}')

class registerModal(ui.Modal, title="Anonymous Hotline"):
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



@client.tree.command(guild=GUILD, name='hotline', description='Anonymously Hotline')
async def hotline(interaction: discord.Interaction):
    await interaction.response.send_modal(registerModal())




