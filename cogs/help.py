import asyncio
import logging

import discord
from discord.ext import commands

from errors import LanguageNotFound
from src.utils import dctt

logger = logging.getLogger("lyvego")


class Help(commands.Cog):
    __slots__ = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(5, 30, commands.BucketType.user)
    @commands.command(name="help", aliases=["h"])
    @commands.bot_has_permissions(manage_messages=True)
    async def help(self, ctx: commands.Context):
        lang = await self.bot.getg_lang(ctx.guild.id)
        react_list = ["<:lyvego:703585626053673060>",
                      "<:twitch:703585214261231626>", "⚙️"]
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
            name=self.bot.locales[lang]["help_hub_twitch"].format(
                react_list[1]),
            value=self.bot.locales[lang]["help_hub_tap_to_see"].format(
                react_list[1]),
            inline=False
        )
        embed.add_field(
            name=self.bot.locales[lang]["help_hub_settings"].format(
                react_list[2]),
            value=self.bot.locales[lang]["help_hub_tap_to_see"].format(
                react_list[2]),
            inline=False
        )
        embed.set_footer(
            text="lyvego.com | help pages deleted in 5 mins",
            icon_url=ctx.me.avatar_url
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
                    name=self.bot.locales[lang]["help_hub_twitch"].format(
                        react_list[1]),
                    value=self.bot.locales[lang]["help_hub_tap_to_see"].format(
                        react_list[1]),
                    inline=False
                )
                embed.add_field(
                    name=self.bot.locales[lang]["help_hub_twitch"].format(
                        react_list[2]),
                    value=self.bot.locales[lang]["help_hub_tap_to_see"].format(
                        react_list[2]),
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
                    name=f"{ctx.prefix}stream <streamer_name> [message : Optional]",
                    value=self.bot.locales[lang]["help_streamer"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}follow <streamer_name> [message : Optional]",
                    value=self.bot.locales[lang]["help_follow"],
                    inline=False
                )

                embed.add_field(
                    name=f"{ctx.prefix}clips <streamer_name> [message : Optional]",
                    value=self.bot.locales[lang]["help_clips"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}remove <follow | stream | clips> <streamer_name>",
                    value=self.bot.locales[lang]["help_remove"],
                    inline=False
                )

                embed.add_field(
                    name=f"{ctx.prefix}topclip <streamer_name> [amount]",
                    value=self.bot.locales[lang]["help_topclip"],
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
                    name=f"{ctx.prefix}lang <--list | new_language>",
                    value=self.bot.locales[lang]["help_language"].format(
                        ", ".join([x.upper() for x in self.bot.locales]).rstrip(", ")),
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}invite",
                    value=self.bot.locales[lang]["help_invite"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}dashboard",
                    value=self.bot.locales[lang]["help_dashboard"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}ping",
                    value=self.bot.locales[lang]["help_ping"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}vote",
                    value=self.bot.locales[lang]["help_vote"],
                    inline=False
                )
                embed.add_field(
                    name=f"{ctx.prefix}about",
                    value=self.bot.locales[lang]["help_about"],
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
        # if isinstance(error, commands.MissingPermissions):
        #     await ctx.send(self.bot.locales[lang]["error_missing_manages_permissions"].format(ctx.author.mention))

        embed = discord.Embed(
            color=self.bot.color,
            description=self.bot.locales[lang]["help_description_header"].format(
                self.bot.lyvego_url),
            timestamp=dctt()
        )
        embed.set_author(
            name=self.bot.locales[lang]["author_name_commands"],
            icon_url=ctx.me.avatar_url
        )
        embed.add_field(
            name=f"<:twitch:703585214261231626> {ctx.prefix}stream <streamer_name>",
            value=self.bot.locales[lang]["help_streamer"],
            inline=False
        )
        embed.add_field(
            name=f"<:twitch:703585214261231626> {ctx.prefix}follow <streamer_name>",
            value=self.bot.locales[lang]["help_follow"],
            inline=False
        )
        embed.add_field(
            name=f"<:twitch:703585214261231626> {ctx.prefix}clips <streamer_name>",
            value=self.bot.locales[lang]["help_clips"],
            inline=False
        )
        embed.add_field(
            name=f"<:twitch:703585214261231626> {ctx.prefix}topclip <streamer_name> [amount]",
            value=self.bot.locales[lang]["help_topclip"],
            inline=False
        )
        embed.add_field(
            name=f"⚙️ {ctx.prefix}setprefix <new_prefix>",
            value=self.bot.locales[lang]["help_prefix"],
            inline=False
        )
        embed.add_field(
            name=f"⚙️ {ctx.prefix}lang <--list | new_language>",
            value=self.bot.locales[lang]["help_language"].format(
                ", ".join([x.upper() for x in self.bot.locales]).rstrip(", ")),
            inline=False
        )
        embed.add_field(
            name="⚙️ @Stream Alerts (Lyvego) getprefix",
            value=self.bot.locales[lang]["help_getprefix"],
            inline=False
        )
        embed.add_field(
            name=f"⚙️ {ctx.prefix}invite",
            value=self.bot.locales[lang]["help_invite"],
            inline=False
        )
        embed.add_field(
            name=f"⚙️ {ctx.prefix}dashboard",
            value=self.bot.locales[lang]["help_dashboard"],
            inline=False
        )
        embed.add_field(
            name=f"🤖 {ctx.prefix}ping",
            value=self.bot.locales[lang]["help_ping"],
            inline=False
        )
        embed.add_field(
            name=f"🤖 {ctx.prefix}vote",
            value=self.bot.locales[lang]["help_vote"],
            inline=False
        )
        embed.add_field(
            name=f"🤖 {ctx.prefix}about",
            value=self.bot.locales[lang]["help_about"],
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
    async def ping(self, ctx):
        embed = discord.Embed(
            timestamp=dctt(),
            color=self.bot.color,
            title="Bot latency"
        )
        embed.add_field(
            name="💗 Hearthbeat",
            value=f"`{self.bot.latencies[ctx.guild.shard_id][1]:.3f}` ms"
        )
        embed.set_footer(
            text="lyvego.com"
        )
        await ctx.send(embed=embed)
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass

    @commands.command()
    async def vote(self, ctx):
        await ctx.send("https://top.gg/bot/702648685263323187/vote")
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass

    @commands.command()
    async def about(self, ctx):
        lang = await self.bot.getg_lang(str(ctx.guild.id))
        embed = discord.Embed(
            timestamp=dctt(),
            color=self.bot.color,
            description=self.bot.locales[lang]["about_description"]
        )
        nb_users = 0
        channels = 0
        for s in self.bot.guilds:
            nb_users += len(s.members)
            channels += len(s.channels)
        embed.add_field(
            name="Dashboard",
            value="[lyvego.com](https://lyvego.com/)"
        )
        embed.add_field(
            name="<:servers:693053697453850655> Servers",
            value=len(self.bot.guilds))
        embed.add_field(
            name="<:users:693053423494365214> Members",
            value=nb_users)
        embed.add_field(
            name="<:hashtag:693056105076621342> Channels",
            value=channels)
        embed.add_field(
            name="<:stack:693054261512110091> Shards",
            value=f"{ctx.guild.shard_id + 1}/{self.bot.shard_count}")
        embed.add_field(
            name="💗 Hearthbeat shards avg",
            value=f"`{sum([x[1] for x in self.bot.latencies]) / self.bot.shard_count:.3f}` ms"
        )
        await ctx.send(embed=embed)
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass

    @commands.command()
    async def invite(self, ctx: commands.Context):
        lang = await self.bot.getg_lang(str(ctx.guild.id))
        embed = discord.Embed(
            title=self.bot.locales[lang]["title_invite_lyvego"],
            description=self.bot.locales[lang]["description_invite_lyvego"].format(
                "https://discord.com/oauth2/authorize?client_id=702648685263323187&permissions=445504&redirect_uri=https%3A%2F%2Flyvego.com%2Flogin&response_type=code&scope=bot%20identify%20email%20guilds"),
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_footer(
            text="lyvego.com",
            icon_url=ctx.me.avatar_url
        )
        await ctx.send(embed=embed)
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass

    # async def announce_owner_handler(self, user, embed):
    #     dm_notif = await user.send(embed=embed)
    #     bot_reaction = await dm_notif.add_reaction("<a:wrong_checkmark:709737435889664112>")
    #     def check(reaction, user_react):
    #         return user == user_react and "<a:wrong_checkmark:709737435889664112>" == str(reaction.emoji)

    #     while 1:
    #         try:
    #             reaction, user_react = await self.bot.wait_for('reaction_add', check=check, timeout=180.0)
    #         except asyncio.TimeoutError:
    #             return
    #             # return await dm_notif.delete()

    #         if "<a:wrong_checkmark:709737435889664112>" == str(reaction.emoji):
    #             try:
    #                 await self.bot.change_annonce(str(user.id))
    #                 break
    #             except Exception as e:
    #                 logger.exception(e, exc_info=True)

    #     try:
    #         success_disable = await user.send("Successfully disabled")
    #         await success_disable.add_reaction("<a:valid_checkmark:709737579460952145>")
    #     except Exception as e:
    #         logger.exception(e, exc_info=True)

    # @commands.command()
    # @commands.is_owner()
    # async def annonce(self, ctx, *message):
    #     message = " ".join(message)
    #     msg_send = 0
    #     embed = discord.Embed(
    #         title="Service information",
    #         timestamp=dctt(),
    #         color=self.bot.color,
    #         description=message
    #     )
    #     buffer = set()
    #     for guild in self.bot.guilds:
    #         try:
    #             await self.bot.insert_annonce(str(guild.owner.id), str(guild.id), 1)
    #         except:
    #             pass
    #         try:
    #             is_enable = await self.bot.get_annonce(str(guild.owner.id))
    #             if is_enable:
    #                 if guild.owner.id not in buffer:
    #                     self.bot.loop.create_task(self.announce_owner_handler(guild.owner, embed))
    #                     buffer.add(guild.owner.id)
    #                     msg_send += 1
    #         except Exception as e:
    #             logger.exception(e, exc_info=True)
    #     await ctx.send(content=f"{msg_send}/{len(self.bot.guilds)} ont été envoyer aux servers owner", embed=embed)

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
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass

    @commands.command()
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.guild_only()
    async def getprefix(self, ctx: commands.Context):
        prefix = await self.bot.getg_prefix(ctx.guild.id)
        await ctx.send(f"`{prefix}`")
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass

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
            raise LanguageNotFound(self.bot.locales[_lang]["error_language_not_found"].format(
                ctx.author.mention, lang))
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass


def setup(bot):
    bot.add_cog(Help(bot))
