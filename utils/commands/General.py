import nextcord
from nextcord.ext import commands
from ..tools.Embeds import embeds
from ..tools.Configuration import configuration
from nextcord.ext.commands.errors import CommandError
import sys
import shutil
from uuid import uuid4
import os


class general(commands.Cog, embeds):
    def __init__(self, client):
        self.client = client
        self.client.check(self.check_authorized)

    def check_authorized(self, ctx):
        """
        Only authorized servers may use commands in this bot.
         This checks that the guild is authorized before allowing commands go go through.
        :param ctx:
        :return:
        """

        if isinstance(ctx.message.channel, nextcord.DMChannel):
            if ctx.message.author.id == 305024830758060034:
                return True  # does not apply to DM channels from the bot owner.

        if "configure_manual" in ctx.message.content:
            return True # does not apply if the bot owner is trying to configure the bot

        if ctx.message.author.id == 305024830758060034 and "authorize" in ctx.message.content:
            return True # does not apply if the bot owner is trying to authorize the bot

        if "authorized" in self.client.configs.find_guild(ctx.guild.id).__dict__.keys():
            # does checks for the authorized state, raises an error if unauthorized.
            if not self.client.configs.find_guild(ctx.guild.id).__dict__['authorized']:
                raise CommandError(
                    "This server has not been authorized. Please contact the bot owner to authorize this server")
        else:
            raise CommandError(
                "This server has not been authorized. Please contact the bot owner to authorize this server")
        return True

    @commands.command(name="athena")
    async def athena(self, ctx):
        """
        info about the bot
        :param ctx:
        :return:
        """

        embed = nextcord.Embed(title="Hi! My name is Athena.",
                               description="Hi. I'm Athena, "
                                           "I am bot designed to help with team management, "
                                           "discord server moderation, and event management.\n Use `!help` to "
                                           "see my commands. ",
                               color=self.SUCCESS)
        embed.add_field(name="Version", value=f"**{self.client.configs.version}**", inline=True)
        embed.add_field(name="Date of last upgrade", value=self.client.configs.upgrade_date, inline=True)

        await ctx.send(embed=embed)

    @commands.command("command")
    async def command_list(self, ctx):
        """
        command line output of commands list.
        :param ctx:
        :return:
        """
        for command in self.client.walk_commands():
            print(command.name)
