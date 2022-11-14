import discord
import json
from discord import ui
from google_commands.get_member import get_member

ServerConfig = json.loads(open("server_config.json").read())


def getRegister(nickname=False, pronoun=None, family=True):
    print(pronoun)
    class RegisterModal(discord.ui.Modal, title="Registration Modal"):
        def __init__(self, *args, **kwargs) -> None:
            super(RegisterModal, self).__init__(*args, **kwargs)
    
        inquiry = discord.ui.TextInput(
            label='What is your full name',
            placeholder='Type your name here...',
            required=True,
            max_length=50) if family else None

        nick = discord.ui.TextInput(
            label='What is your nick name?',
            placeholder='Default is your real name',
            required=False,
            max_length=32) if nickname else None

        async def on_submit(self, interaction: discord.Interaction):
            if nickname:
                await interaction.user.edit(nick=self.nick.value)
            
            if pronoun and not nickname:
                member = get_member(self.inquiry.value)
                print(member)
                await interaction.response.edit_message(content="Please confirm your identity", view=SelectView(view=Confirmation(member, pronoun=pronoun)))

            if  family: 
                member = get_member(self.inquiry.value)
                await interaction.response.edit_message(content="Please confirm your identity", view=SelectView(view=Confirmation(member, pronoun=pronoun)))

            if nickname and not family:
                member_role = discord.utils.get(interaction.guild.roles, name="Member")
                await interaction.user.add_roles(member_role)
                await interaction.response.send_message("You have been assinged the role (Member) please speak with an Officer on being assigned a Family", ephemeral=True)
            if not family and pronoun:
                pronoun_role = discord.utils.get(interaction.guild.roles, name=pronoun)
                await interaction.user.add_roles(pronoun_role)
                await interaction.response.send_message("You have been assinged the role (Member) please speak with an Officer on being assigned a Family", ephemeral=True)

            else:
                await interaction.response.send_message("Sorry! Error")

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
            print(error)
            
    _RegisterModal = RegisterModal()
    return _RegisterModal


class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, view):
        super().__init__(timeout=timeout)
        self.add_item(view)

def Confirmation(checklist, pronoun=None):
    print(checklist[0][1])
    class Confirmation(discord.ui.Select):
        def __init__(self, *args, **kwargs) -> None:
            # self.checklist=checklist
            super(Confirmation, self).__init__(*args, **kwargs)
            options=[]
            for option in checklist:
                options.append(discord.SelectOption(label=f'{option[1]} {option[0]}', value=f'{option[2]}, {option[1]}, {option[0]}', description=option[2]))
            not_found = discord.SelectOption(label="Not Found", description="Select this option if you do not see name in list" ,emoji="❌")
            options.append(not_found)
            super().__init__(placeholder="Please confirm your identity",max_values=1 ,min_values=1, options=options)


        async def callback(self, interaction : discord.interactions):

            not_found = "Not Found"
            if not_found in self.values:
                await interaction.response.edit_message(content="Sorry, Error")
            
            if len(self.values) > 0 and not_found not in self.values:
                roles = []
                user = interaction.user
                guild = interaction.guild
                family_name = self.values[0].split(", ")[0]
             
                pronoun_role = discord.utils.get(guild.roles, name=pronoun) if pronoun else None
                family_role = discord.utils.get(guild.roles, name=family_name)

                await user.add_roles(family_role)
                if pronoun_role: await user.add_roles(pronoun_role)
                await interaction.response.send_message(f'Thank you for joining!', ephemeral=True)

    _Confirmation = Confirmation()
    return _Confirmation

def addRole(interaction : discord.interactions, pronoun=None, family=None):
    roles = []
    guild = interaction.guild
    family = guild.get_role(ServerConfig[pronoun]) if pronoun else None
    role = guild.get_role(ServerConfig[family]) if family else None
    roles.append(family, role)
    if role or pronoun:
        interaction.user.add_roles(roles)

