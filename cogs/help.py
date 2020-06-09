import asyncio
import logging
import os

import discord
from discord.ext import commands

from errors import LanguageNotFound
from src.constants import AUTHORIZATION
from src.utils import dctt


logger = logging.getLogger("lyvego")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(5, 30, commands.BucketType.user)
    @commands.command(name="help", aliases=["h"])
    @commands.bot_has_permissions(manage_messages=True)
    async def help(self, ctx: commands.Context):
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
        lang = await self.bot.getg_lang(ctx.guild.id)
        react_list = ["<:lyvego:703585626053673060>", "<:twitch:703585214261231626>", "⚙️"]
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
            name=f"{react_list[1]} Views commands related to stream",
            value=f"Tap {react_list[1]} to see them !",
            inline=False
        )
        embed.add_field(
            name=f"{react_list[2]} Views commands related to bot settings",
            value=f"Tap {react_list[2]} to see them !",
            inline=False
        )
        pages = await ctx.send(embed=embed)

        for reaction in react_list:
            await pages.add_reaction(reaction)

        def predicate(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in react_list

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=predicate, timeout=300.0)
            except asyncio.TimeoutError:
                try:
                    await ctx.message.delete()
                except:
                    pass
                await pages.delete()
                return

            if react_list[0] == str(reaction.emoji):
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
                    name=f"{react_list[1]} Views commands related to stream",
                    value=f"Tap {react_list[1]} to see them !",
                    inline=False
                )
                embed.add_field(
                    name=f"{react_list[2]} Views commands related to bot settings",
                    value=f"Tap {react_list[2]} to see them !",
                    inline=False
                )
            elif react_list[1] == str(reaction.emoji):
                embed = discord.Embed(
                    timestamp=dctt(),
                    color=self.bot.color,
                )
                embed.set_author(
                    name=self.bot.locales[lang]["paginated_author_twitch_commands"],
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

            elif react_list[2] == reaction.emoji:
                embed = discord.Embed(
                    timestamp=dctt(),
                    color=self.bot.color
                )
                embed.set_author(
                    name=self.bot.locales[lang]["paginated_author_settings_commands"],
                    icon_url=ctx.me.avatar_url
                )
                embed.add_field(
                    name=f"{ctx.prefix}setprefix <new_prefix>",
                    value=self.bot.locales[lang]["help_prefix"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}getprefix",
                    value=self.bot.locales[lang]["help_getprefix"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}lang < --list | new_language>",
                    value=self.bot.locales[lang]["help_language"].format(", ".join([x.upper() for x in self.bot.locales]).rstrip(", ")),
                    inline=False
                )


            embed.set_footer(
                text="lyvego.com",
                icon_url=ctx.me.avatar_url
            )
            await pages.remove_reaction(reaction.emoji, user)
            await pages.edit(embed=embed)


    @help.error
    async def help_error(self, ctx: commands.Context, error):
        lang = await self.bot.getg_lang(ctx.guild.id)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(self.bot.locales[lang]["error_missing_manages_permissions"].format(ctx.author.mention))

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
        embed.add_field(
            name="@Stream Alerts (Lyvego) getprefix",
            value=self.bot.locales[lang]["help_getprefix"],
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
    async def invite(self, ctx: commands.Context):
        lang = await self.bot.getg_lang(str(ctx.guild.id))
        embed = discord.Embed(
            title=self.bot.locales[lang]["title_invite_lyvego"],
            description=self.bot.locales[lang]["description_invite_lyvego"].format("https://discord.com/oauth2/authorize?client_id=702648685263323187&permissions=445504&redirect_uri=https%3A%2F%2Flyvego.com%2Flogin&response_type=code&scope=bot%20identify%20email%20guilds"),
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_footer(
            text="lyvego.com",
            icon_url=ctx.me.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def dashboard(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Lyvego Dashboard",
            description="[lyvego.com](https://lyvego.com/)",
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_footer(
            text="lyvego.com",
            icon_url=ctx.me.avatar_url
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.guild_only()
    async def getprefix(self, ctx: commands.Context):
        prefix = await self.bot.getg_prefix(ctx.guild.id)
        await ctx.send(f"Guild prefix for **{ctx.guild.name}** : `{prefix}`")

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


def setup(bot):
    bot.add_cog(Help(bot))
