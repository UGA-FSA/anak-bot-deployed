import discord
from discord import Button, app_commands, ui
from discord.ext import commands
from datetime import datetime


GUILD = discord.Object(id=1009880371220992000)
class HotlineButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Activate Hotline",style=discord.ButtonStyle.success)
    async def active_button(self, button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.edit_message(content=f"This is an Automated Button Test!")


class ChannelMessageCommands(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Channel Message Commands Loaded..")

    # @commands.command()
    # async def send_register(self, ctx):
    #     print("Register Command Sent")
    #     # await ctx.channel.send("Test Command")
    #     # channel = self.bot.get_channel(1034229115299057715)
        
    #     await self.bot.get_channel(1034229115299057715).send("Automated Message: : This is an Automated Test")
        # channel = self.bot.get_channel(1035059275178975232)

        # channel = discord.utils.get(ctx.bot.guild, name="music")
        # print("channel" + channel)
        # print("hreeknfl")
        # await channel.send("This is an automated test from bot.")

    @commands.command()
    async def send_rules(self, ctx):
        
        channel =  self.bot.get_channel(1011488377322876969)
        embed=discord.Embed(
            title="Server Rules", 
            description="\n1. Please use common sense.\n2. No discrimination. This includes, but will not be limited to any signs of xenophobia, racism, sexism, religious bigotry, and homophobia.\n3. No NSFW images. \n4. Please don't harass people! (Including, but not limited to: stalking, physical harassment, emotional harassment)\n5. Do not spam \n8. Do not spread false information, and keep an eye out for anything that may be suspicious! Always do your own research.\nNo academic dishonesty\n8. If you do not feel comfortable with a member, please let someone on E-Board know.\nAll Discord community guidelines also apply.,", 
            color=0xFFFB00)
        await channel.send(embed=embed)


        

async def setup(bot):
    await bot.add_cog(ChannelMessageCommands(bot), guilds=[GUILD])