import asyncio
import logging

import discord
from discord.ext import commands

from errors import LanguageNotFound
from src.utils import dctt

logger = logging.getLogger("lyvego")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(5, 30, commands.BucketType.user)
    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx: commands.Context):
        lang = await self.bot.getg_lang(ctx.guild.id)
        embed = discord.Embed(
            color=self.bot.color,
            description=self.bot.locales[lang]["help_description_header"],
            timestamp=dctt()
        )
        embed.set_author(
            name=self.bot.locales[lang]["author_name_commands"],
            icon_url=ctx.me.avatar_url
        )
        embed.add_field(
            name=f"{ctx.prefix}stream <streamer_name>",
            value=self.bot.locales[lang]["help_streamer"],
            inline=False
        )
        embed.add_field(
            name=f"{ctx.prefix}follow <streamer_name>",
            value=self.bot.locales[lang]["help_follow"],
            inline=False
        )
        embed.add_field(
            name=f"{ctx.prefix}clip <streamer_name>",
            value=self.bot.locales[lang]["help_clip"],
            inline=False
        )
        embed.add_field(
            name=f"{ctx.prefix}setprefix <new_prefix>",
            value=self.bot.locales[lang]["help_prefix"],
            inline=False
        )
        embed.add_field(
            name=f"{ctx.prefix}lang < --list | new_language>",
            value=self.bot.locales[lang]["help_language"].format(", ".join([x.upper() for x in self.bot.locales]).rstrip(", ")),
            inline=False
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

    @commands.command()
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def setprefix(self, ctx: commands.Context, prefix: str):
        lang = await self.bot.getg_lang(ctx.guild.id)
        try:
            await self.bot.set_prefix(ctx.guild.id, prefix)
            await ctx.send(self.bot.locales[lang]["newprefix_message"].format(ctx.author.mention, prefix))
        except Exception as e:
            logger.exception(e, exc_info=True)


    @commands.command(aliases=["language"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def lang(self, ctx, lang):
        _lang = await self.bot.getg_lang(ctx.guild.id)
        lang = lang.lower()
        if lang == "--list":
            list_lang = ""
            for l in self.bot.locales.keys():
                list_lang += f"- **{l.upper()}**\n"
            return await ctx.send(self.bot.locales[_lang]["available_languages"].format(list_lang))
        elif lang in self.bot.locales.keys():
            try:
                await self.bot.set_lang(ctx.guild.id, lang)
                await ctx.send(self.bot.locales[lang]["new_language"].format(ctx.author.mention, lang.upper()))

            except Exception as e:
                logger.exception(e, exc_info=True)
        else:
            raise LanguageNotFound(self.bot.locales[_lang]["error_language_not_found"].format(ctx.author.mention, lang))
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass



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
