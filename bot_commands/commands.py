import discord
import re
from random import randint
from log.log_client import LogClient


class Commands:
    Prefix = "!"
    Jokes_mama_path = "text_files/yomama_jokes.txt"
    Jokes_path = "text_files/jokes.txt"

    def __init__(self, message=discord.Message, client=discord.Client):
        self.message = message
        self.client = client

    def _getCommands(self):
        methods = dir(self)
        commands = {}
        for method in methods:
            if method.startswith("c_"):
                commands.update({method[2:]: method})

        return commands

    async def findResponse(self):
        commandList = self._getCommands()

        command = self.message.content.split(" ")[0][1:].lower()
        if command in commandList:
            try:
                await getattr(self, commandList[command])()
            except discord.Forbidden as e:
                await self.logException(e)
            except discord.NotFound as e:
                await self.logException(e)

    async def logException(self, e):
        LogClient.LogException(self.message, e)
        await self.sendString(e.__class__.__name__)

    # Extra Line
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Methods Up there!
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    async def sendString(self, string=""):
        await self.client.send_message(destination=self.message.channel, content=string)

    # Send methods here --------------------------------------------------------------------------------------------------------------------------------------------------

    async def sendEmbed(self, embed=discord.Embed):
        await self.client.send_message(destination=self.message.channel, embed=embed)

    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # botCommands Down here!
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Extra Line

    async def c_hi(self):
        # The bot says Hi back

        await self.sendString("Hello " + self.message.author.mention)

    async def c_example(self):
        # Shows examples for the commands
        responses = []
        responses.append("!hi            !hi")
        responses.append("!say           !say hi or !say @User l2p")
        responses.append("!help          !help")
        responses.append("!joke          !joke")
        responses.append("!mjoke         !mjoke or !mjoke @User")
        responses.append("!8ball         !8ball am i pro?  (Yes or no question)")
        #responses.append("!insult        !insult or !insult @User")
        responses.append("!nickname      !nickname @User  (User must't be the owner)")
        responses.append("!example       ...")

        value = "```"
        for i in responses:
            value += i + "\n"
        value += "```"
        await self.sendString(value)

    async def c_help(self):
        # The bot shows the help menu

        value = ""
        for i in sorted(self._getCommands(), key=len):
            value += "`!" + i + "`, "
        embed = discord.Embed()
        embed.add_field(name="Commands", value=value[:-2])
        embed.add_field(name="TMX Command",
                        value="- Just paste a tmx map link and the bot will return information about the map\n"
                              + "- Example: https://tmnforever.tm-exchange.com/main.aspx?action=trackshow&id=6854724#auto\n"
                              + "- *Many hard. Such expert. Very difficult. 10/10 Example.*")
        embed.add_field(name="For examples", value="!example")
        embed.color = discord.Color.orange()
        await self.sendEmbed(embed)

    async def c_8ball(self):
        # The bot senses the users future and creates a response

        if self.message.content.lower() == "!8ball":
            await self.sendString("Example: `!8ball is @User good?`")
            return

        responses = {}
        responses.update({1: "It is certain"})
        responses.update({2: "My reply is no"})
        responses.update({3: "Without a doubt"})
        responses.update({4: "Yes definitely"})
        responses.update({5: "You may rely on it"})
        responses.update({6: "Don\'t count on it"})
        responses.update({7: "Most likely"})
        responses.update({8: "Outlook good"})
        responses.update({9: "Very doubtful"})
        responses.update({10: "Signs point to yes"})
        responses.update({11: "As I see it, yes"})
        responses.update({12: "It is decidedly so"})
        responses.update({13: "My sources say no"})
        responses.update({14: "Outlook not so good"})
        responses.update({15: "Yes"})

        number = randint(1, 15)

        await self.sendString(responses.get(number))

    async def c_say(self):
        # The bot says what the user wants
        # The try catch is here because some other bot could have the same command..
        # So there is a chance that the message would get erased before this bot can do it
        try:
            await self.client.delete_message(message=self.message)
        except discord.NotFound:
            pass
        if len(self.message.content) == 4:
            await self.sendString("What do you want me to say? " + self.message.author.mention)
            return

        await self.sendString(self.message.content[4:])

    async def c_nickname(self):
        # Changes the nickname of the mentioned user
        # The bot can't change the name of the owner (discord policy)
        # The bot won't change the nickname of @everyone

        if self.message.content.lower() == "!nickname":
            await self.sendString("Example: `!nickname @User nickname` or `!nickname nickname @User`")
            return

        nickname = re.sub("<@.*?>", "", self.message.content)[9:].strip()
        if self.message.mention_everyone:
            await self.sendString("I refuse!")
            return

        for mention in self.message.mentions:
            if self.message.server.owner == mention:
                await self.sendString("I can't change the owners nickname")
            else:
                await self.client.change_nickname(member=mention, nickname=nickname)
                await self.sendString("Done!")

    async def c_joke(self):
        maxline = 570
        random_line = randint(1, maxline)
        with open(self.Jokes_path, "r", encoding="utf8") as file:
            for i, line in enumerate(file):
                if i == random_line:
                    await self.sendString(line)
                    break

    async def c_mjoke(self):
        mentions = ""
        if len(self.message.mentions) > 0:
            for mention in self.message.mentions:
                mentions += mention.mention + " "
        maxline = 1049
        random_line = randint(1, maxline)
        with open(self.Jokes_mama_path, "r", encoding="utf8") as file:
            for i, line in enumerate(file):
                if i == random_line:
                    await self.sendString(mentions + line)
                    break

    # async def c_insult(self):
    #     maxline = 2279
    #     random_line = randint(1, maxline)
    #     with open(self.bad_words_path, "r", encoding="utf8") as file:
    #         for i, line in enumerate(file):
    #             if i == random_line and self.message.mention_everyone:
    #                 await self.sendString(line[:-1] + " @everyone")
    #             elif i == random_line and len(self.message.mentions) == 0:
    #                 await self.sendString(line)
    #                 break
    #             elif i == random_line and len(self.message.mentions) > 0:
    #                 text = line[:-1]
    #                 for m in self.message.mentions:
    #                     text += " " + m.mention
    #                 await self.sendString(text)
    #                 break

    async def c_info(self):
        embed = discord.Embed()
        if self.client.connection.user.avatar_url == "":
            embed.set_author(name=self.client.connection.user.name,
                             icon_url=self.client.connection.user.default_avatar_url)
        else:
            embed.set_author(name=self.client.connection.user.name, icon_url=self.client.connection.user.avatar_url)

        embed.title = "Github Repository"
        embed.url = "https://github.com/Jubast/JBot"
        embed.add_field(name="Number of servers: ", value=len(self.client.connection._servers))
        embed.color = discord.Color.green()
        await self.sendEmbed(embed)
