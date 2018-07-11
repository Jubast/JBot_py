import discord
import sys
import re

from bot_commands.commands import Commands
from log.log_client import LogClient
from trackmania.trackmania_client import TrackmaniaClient
from trackmania.trackmania_embed_builder import TrackmaniaEmbedBuilder
from time import gmtime, strftime

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name=Commands.Prefix + "help"))
    LogClient.Log("Logged in as: " + client.user.name + "\n" + strftime('%Y-%m-%d %H:%M:%S', gmtime()) + "\n--------")


@client.event
async def on_message(message=discord.Message):
    # Discord on_message_recived event
    # Logs the input
    # Responds to non-bot users
    try:
        log = "[" + message.timestamp.strftime('%Y-%m-%d %H:%M:%S') + "][Server: " + message.server.name + " " + message.server.id + "][Channel: " + message.channel.name + \
              " " + message.channel.id + "][" + message.author.name + " => " + message.content + "]"
        LogClient.Log(log)

        if message.author.bot:
            return

        # Checks if the message starts with the bot prefix
        if message.content.startswith('!'):
            await Commands(message, client).findResponse()
            return

        # Checks if the message includes the trackmania link
        result = re.search("https://tmnforever\.tm-exchange\.com/main\.aspx\?action=trackshow&id=(\d+)", message.content)
        if result is not None:
            t = await TrackmaniaClient().getInfo(result.group(1))
            embed = TrackmaniaEmbedBuilder().CreateDiscordEmbeded(t)
            await client.send_message(message.channel, "", embed=embed)
    except:
        e = sys.exc_info()[1]
        LogClient.LogException(message, e)
        await client.logout()
        exit(1)

with open("text_files/token.txt", "r") as file:
    lines = file.readlines()
    if sys.gettrace():
        LogClient.CanLog = True
        print("Debuging")
        key = lines[0][:-1]  # to remove \n
    else:
        key = lines[1]

client.run(key)
