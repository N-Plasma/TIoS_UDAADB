import UDAADB_Func
import UDAADB_GetToken
from typing import Optional
import logging
import logging.handlers
import subprocess
import time
import discord
from discord.ext import commands
from discord import app_commands
import os
from pymongo.mongo_client import MongoClient

DeltaID = [1178623681329647627, 926634820740710451, 1198292466533666902]

logging.basicConfig(
    filename='logging.log',
    filemode='w',
    encoding='utf-8',
    level=logging.INFO,
    format='%(levelname)s:%(asctime)s:%(funcName)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)



class Client(commands.Bot):
    async def on_ready(self):
        print('Logged on as ',self.user)
        logger.info('Logged on as ',self.user)

intents = discord.Intents.all()
client = Client(command_prefix='*',intents=intents)

monclient = MongoClient('localhost', 27017)
db = monclient.UDAADB
users = db.users
incidentreports = db.incidents

token = UDAADB_GetToken.Get()
UDAADB_Func.UpdateCheck()

logger.info('UDAADB_Core PreSetup Completed')
print('UDAADB_Core PreSetup Completed')

@client.command()
async def sync(ctx: commands.Context):
    id = discord.User.id
    if id in DeltaID:
        await ctx.bot.tree.sync(guild=ctx.guild)
        print(id,' Synced Commands')
        logger.info(id,' Synced Commands')
        await ctx.send('Synced',ephemeral=True)
    else:
        print(id,' Failed to Sync Commands (Low Rank)')
        logger.info(id,' Failed to Sync Commands (Low Rank)')
        await ctx.send('Failed, You are not ranked high enough to sync',ephemeral=True)

@client.tree.command(name='ping_database',description='Pings Connected Database')
async def dbping(interaction: discord.Interaction):
    id = discord.User.id
    if id in DeltaID:
        resp = UDAADB_Func.dbping()
        await interaction.response.send_message(resp,ephemeral=True)

@client.tree.command(name='create_user',description='Creates a user & currency entry')
async def makeusr(interaction: discord.Interaction, id: discord.Member, user: str, display: str, role: str, rank: str):
        id = discord.User.id
        if id in DeltaID:
            own_id = discord.Interaction.user.id
            UDAADB_Func.makeusr(id,user,display,role,rank,own_id)
            await interaction.response.send_message('User Entry Created!',ephemeral=True)

@client.tree.command(name='create_incident_report',description='Creates a incident report')
async def makeinci(interaction: discord.Interaction, name: str, public: bool, involved: str, body: str):
        id = discord.User.id
        if id in DeltaID:
            own_id = discord.Interaction.user.id
            UDAADB_Func.incimake(name,public,involved,body,own_id)
            await interaction.response.send_message('Incident Report Entry Created!',ephemeral=True)

#@client.tree.command(name='edit_user_entry',description='Edits user entry')

#@client.tree.command(name='edit_currency_entry',description='Edits user currency entry')

#@client.tree.command(name='edit_incident_report',description='Edits incident entry')

#@client.tree.command(name='read_user_entry',description='Reads selected users entry')

#@client.tree.command(name='read_incident_report',description='Reads selected incident report (only public ones are listed, non-public reports can only be read by L4+)')

#@client.tree.command(name='read_xp',description='Shows selected users XP')

#@client.tree.command(name='auto_xp',description='Automatically gives users xp for events')

#@client.tree.command(name='man_xp',description='Manually updates XP')

#@client.tree.command(name='check_bot_version',description='Checks if the bot is up to date')

#@client.tree.command(name='announce_event',description='Announces selected event in a embed')

#@client.tree.command(name='announce_news',description='Announces news in a embed')

#@client.tree.command(name='auto_update',description='Updates user roles')

#END CODE
client.run(token)