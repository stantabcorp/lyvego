import asyncio
import logging

import discord
from discord.ext import commands

from src.utils import dctt


logger = logging.getLogger("lyvego")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    @commands.cooldown(5, 30, commands.BucketType.user)
    async def help(self, ctx: commands.Context):
        embed = discord.Embed(
            color=self.bot.color,
            description=f"You can configure the bot on [lyvego.com]({self.bot.lyvego_url})\nRemove the <> when you are using a command.",
            timestamp=dctt()
        )
        embed.set_author(
            name="Lyvego commands",
            icon_url=ctx.me.avatar_url
        )
        embed.add_field(
            name="!streamer <streamer_name>",
            value="Send notification when the streamer goes live. (Server only - Admin required)"
        )
        embed.add_field(
            name="!follow <streamer_name>",
            value="Send notification when someone follow this streamer. (Server only - Admin required)"
        )
        embed.add_field(
            name="!clip <streamer_name>",
            value="Get the 5 most watch clips for the past last week. (Server only)"
        )
        embed.set_thumbnail(url=ctx.me.avatar_url)
        embed.set_footer(
            text="lyvego.com",
            icon_url=ctx.me.avatar_url
        )
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
        await ctx.send(embed=embed)


    @commands.command(name="clean")
    async def testsend(self, ctx):
        await self.bot.clean_all()

    @commands.command()
    async def test(self, ctx):
        await ctx.send("<a:valid_checkmark:709737579460952145> <a:twitch_anim:709737519264301107> <a:wrong_checkmark:709737435889664112>")


    @commands.command(name="edit")
    async def testedit(self, ctx, id, _id):
        channel = self.bot.get_channel(int(id))
        msg = await channel.fetch_message(int(_id))
        print("edit", channel, msg)
        await msg.edit(content="changed")
        await msg.delete()
        await ctx.send("message deleted")
        # for message in channel.message:
        #     print(message)


def setup(bot):
    bot.add_cog(Help(bot))
