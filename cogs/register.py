
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select
from datetime import datetime

# from main import GUILD
from .libs.roles import  getRegister
GUILD = discord.Object(id=1009880371220992000)
class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, view):
        super().__init__(timeout=timeout)
        self.add_item(view)

def Pronouns(nickname=None, family=True):
    class Pronouns(discord.ui.Select):
        def __init__(self, *args, **kwargs) -> None:
            super(Pronouns, self).__init__(*args, **kwargs)

            options=[
                discord.SelectOption(label="He/Him", emoji="🐹"),
                discord.SelectOption(label="She/Her",emoji="🐰"),
                discord.SelectOption(label="They/Them",emoji="🐻‍❄️"),
                discord.SelectOption(label="Return", emoji="🔙"),
                ]
            super().__init__(placeholder="Click here to select pronouns",max_values=1 ,min_values=1,options=options)

        async def callback(self, interaction : discord.interactions):
            go_back = "Return"
            if go_back in self.values:
                await interaction.response.edit_message(content="Register", view=SelectView(view=Select()))
                
            if not family and not nickname and go_back not in self.values:
                member_role = discord.utils.get(interaction.guild.roles, name="Member")
                pronoun_role = discord.utils.get(interaction.guild.roles, name=self.values[0])
                await interaction.user.add_roles(member_role)
                await interaction.user.add_roles(pronoun_role)
                
                await interaction.response.send_message("You have been assinged the role (Member) please speak with an Officer on being assigned a Family", ephemeral=True)
            if len(self.values) > 0 and go_back not in self.values:
                await interaction.response.send_modal(getRegister(nickname=nickname, pronoun=self.values[0], family=family))

    _Pronoun = Pronouns()
    return _Pronoun

    
        
class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Nickname", emoji="📓",description="Select this if you would like to change user name"),
            discord.SelectOption(label="Pronouns",emoji="✨",description="Select this if you like to set preferred pronouns?"),
            discord.SelectOption(label="Not in a Family", value="Family",emoji="🇵🇭",description="Select this if you are not assigned to a family."),
            discord.SelectOption(label="None of the Above", description="Clicking this will ignore the above selections, and continue the registration system!", value="Continue")
            ]
        super().__init__(placeholder="Click here to begin Registration",max_values=3,min_values=1,options=options)

    async def callback(self, interaction : discord.Interaction):
        print(self.values)
        if "Continue" in self.values:
            await interaction.response.send_modal(getRegister())

        nickname = True if "Nickname" in self.values else False 
        family = False if "Family" in self.values else True 
        pronoun = True if "Pronouns" in self.values else False 

        if not family and not pronoun and not nickname:
            print("Accessed the")
            family_role = discord.utils.get(interaction.guild.roles, name="Member")
            await interaction.user.add_roles(family_role)
            await interaction.response.send_message("You have been assinged the role (Member) please speak with an Officer on being assigned a Family", ephemeral=True)

        if pronoun:
            if pronoun and not family:
                await interaction.response.edit_message(content="Pronouns" ,view=SelectView(view=Pronouns(nickname=nickname, family=family)))
            if pronoun and nickname:
                await interaction.response.edit_message(content="Pronouns" ,view=SelectView(view=Pronouns(nickname=nickname, family=family)))
            await interaction.response.edit_message(content="Pronouns" ,view=SelectView(view=Pronouns()))
     
        if nickname:
            if nickname and not family and not pronoun:
                await interaction.response.send_modal(getRegister(nickname=nickname, family=family))
            await interaction.response.send_modal(getRegister(nickname=nickname))
            if pronoun and nickname:
                await interaction.response.edit_message(content="Pronouns" ,view=SelectView(view=Pronouns(nickname=nickname, family=family)))

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
        print(error)

class Register(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Register Command Loaded..")
     
    @commands.command()
    async def check_cog(self, ctx):
        print("Works")
        cog_response = discord.Embed(description=(f'{ctx.author.name} cog check passed!'))
        await ctx.channel.send(embed= cog_response)

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send("Pong")
    
    # @commands.command()
    # async def send_register(self, ctx : commands.Context):
    #     channel = ctx.channel
    #     member = ctx.author
    #     await ctx.message.delete()

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced the tree to {len(fmt)}.")

    @app_commands.command(name="register", description="Use this command to register")
    async def register(self, interaction : discord.interactions):
        print("menu reached")
        await interaction.response.send_message("Registration Begins Here!",view=SelectView(view=Select()), ephemeral=True)
       

    @commands.command()
    async def send_register(self, ctx):
        print("Register Command Sent")
        embed=discord.Embed(
            title="Register Here! Please Type /register to begin", description="Hello, Welcome to UGA FSA! This is Anak speaking. Currently my developers are working hard on upgrading me with new features; however, before you can enjoy this server, and see these changes, please begin by using the /register command!", 
            color=0xFFFB00)
            
        embed.set_footer(text="If you get stuck, please send a message in the help chat or to @Lightsity")

        channel =  self.bot.get_channel(1034229115299057715)
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Register(bot), guilds=[GUILD])