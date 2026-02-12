import UDAADB_Func
from typing import Optional
import logging
import subprocess
import time
import discord
from discord.ext import commands
from discord import app_commands
import os
from os import load_dotenv
from pymongo.mongo_client import MongoClient

class Client(commands.Bot):
    async def on_ready(self):
        print('Logged on as ',self.user)
        logging.INFO('Logged on as ',self.user)

intents = discord.Intents.all()
client = Client(command_prefix='*',intents=intents)

monclient = MongoClient('localhost', 27017)
db = monclient.UDAADB
users = db.users
incidentreports = db.incidents

load_dotenv()
token = os.getenv('token')
UDAADB_Func.UpdateCheck()

logging.basicConfig(level=logging.INFO)
logging.INFO('UDAADB_Core PreSetup Completed')
print('UDAADB_Core PreSetup Completed')

@client.tree.command(name='ping database',description='Pings Connected Database')
async def dbping(interaction: discord.Interaction):
    resp = UDAADB_Func.dbping()
    await interaction.response.send_message(resp)

@client.tree.command(name='create user',description='Creates a user & currency entry')
async def makeusr(interaction: discord.Interaction, id: discord.Member, user: str, display: str, role: str, rank: str):
    own_id = discord.Interaction.user.id
    UDAADB_Func.makeusr(id,user,display,role,rank,own_id)
    await interaction.response.send_message('User Entry Created!')

@client.tree.command(name='create incident report',description='Creates a incident report')
async def makeinci(interaction: discord.Interaction, name: str, public: bool, involved: str, body: str):
    UDAADB_Func.incimake(name,public,involved,body,)

@client.tree.command(name='edit user entry',description='Edits user entry')

@client.tree.command(name='edit currency entry',description='Edits user currency entry')

@client.tree.command(name='edit incident report',description='Edits incident entry')

@client.tree.command(name='read user entry',description='Reads selected users entry')

@client.tree.command(name='read incident report',description='Reads selected incident report (only public ones are listed, non-public reports can only be read by L4+)')

@client.tree.command(name='read xp',description='Shows selected users XP')

@client.tree.command(name='auto xp',description='Automatically gives users xp for events')

@client.tree.command(name='man xp',description='Manually updates XP')

@client.tree.command(name='check bot version',description='Checks if the bot is up to date')

@client.tree.command(name='announce event',description='Announces selected event in a embed')

@client.tree.command(name='announce news',description='Announces news in a embed')

@client.tree.command(name='auto update',description='Updates user roles')

#END CODE
client.run(token)