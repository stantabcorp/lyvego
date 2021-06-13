import asyncio
import logging

import discord
import math

import errors
from src import *

logger = logging.getLogger("lyvego")


class Settings(commands.Cog):
    __slots__ = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context):
        try:
            self.bot.loader(reloading=True)
            await ctx.send("Reloaded")
        except Exception as e:
            await ctx.send(e)

    @commands.command(name="follow")
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_follow(self, ctx: commands.Context, streamer: str, *message):
        lang = await self.bot.getg_lang(ctx.guild.id)
        resp = await post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                    "type": "follow_announcement",
                    "channel_id": ctx.channel.id,
                    "streamer": streamer,
                    "message": " ".join(message) if len(message)
                    else self.bot.locales[lang]["message_started_following"],
                    "color": self.bot.color_str,
                    "update_message_on_change": False,
                    "delete_message_on_change": False
                }
            ]
        )
        if resp.status in range(200, 300):

            embed = discord.Embed(
                description=self.bot.locales[lang]["description_configure_lyvego"].format(
                    self.bot.lyvego_url),
                color=self.bot.color,
                timestamp=dctt()
            )
            embed.set_author(
                name=f"{streamer} successfully added",
                icon_url=ctx.author.avatar_url
            )
            embed.set_thumbnail(
                url=ctx.me.avatar_url
            )
            try:
                await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
            except:
                pass
            await ctx.send(embed=embed)
        else:
            raise errors.StreamerNotFound(
                self.bot.locales[lang]["error_streamer_not_found"].format(ctx.author))

    @commands.command(name="clips", aliases=["clip"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_clips(self, ctx: commands.Context, streamer: str):
        lang = await self.bot.getg_lang(ctx.guild.id)
        resp = await post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                    "type": "clip_announcement",
                    "channel_id": ctx.channel.id,
                    "streamer": streamer
                }
            ]
        )
        if resp.status in range(200, 300):

            embed = discord.Embed(
                description=self.bot.locales[lang]["description_configure_lyvego"].format(
                    self.bot.lyvego_url),
                color=self.bot.color,
                timestamp=dctt()
            )
            embed.set_author(
                name=self.bot.locales[lang]["author_name_success_added"].format(
                    streamer),
                icon_url=ctx.author.avatar_url
            )
            embed.set_thumbnail(
                url=ctx.me.avatar_url
            )
            try:
                await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
            except:
                pass
            await ctx.send(embed=embed)
        else:
            raise errors.StreamerNotFound(
                self.bot.locales[lang]["error_streamer_not_found"].format(ctx.author))

    @commands.command(name="stream")
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def add_streamer(self, ctx: commands.Context, streamer: str, *message):
        lang = await self.bot.getg_lang(ctx.guild.id)
        resp = await post_streamer(
            ctx,
            self.bot.http_session,
            json=[
                {
                    "type": "live_announcement",
                    "channel_id": ctx.channel.id,
                    "streamer": streamer,
                    "message": " ".join(message) if len(message) else self.bot.locales[lang]["message_stream_live"],
                    "color": self.bot.color_str,
                    "update_message_on_change": False,
                    "delete_message_on_change": False
                }
            ]
        )
        if resp.status in range(200, 300):

            embed = discord.Embed(
                description=self.bot.locales[lang]["description_configure_lyvego"].format(
                    self.bot.lyvego_url),
                color=self.bot.color,
                timestamp=dctt()
            )
            embed.set_author(
                name=self.bot.locales[lang]["author_name_success_added"].format(
                    streamer),
                icon_url=ctx.author.avatar_url
            )
            embed.set_thumbnail(
                url=ctx.me.avatar_url
            )
            try:
                await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
            except:
                pass
            await ctx.send(embed=embed)
        else:
            raise errors.StreamerNotFound(
                self.bot.locales[lang]["error_streamer_not_found"].format(ctx.author))

    @commands.command(aliases=["remove"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def remove_event(self, ctx: commands.Context, event: str, streamer: str):
        lang = await self.bot.getg_lang(ctx.guild.id)
        resp = await remove_user_event(ctx, self.bot.http_session, event, streamer)
        if resp.status >= 200 and resp.status < 300:
            embed = discord.Embed(
                description=self.bot.locales[lang]["description_configure_lyvego"].format(
                    self.bot.lyvego_url),
                color=self.bot.color,
                timestamp=dctt()
            )
            embed.set_author(
                name=self.bot.locales[lang]["author_name_success_removed"].format(
                    streamer),
                icon_url=ctx.author.avatar_url
            )
            embed.set_thumbnail(
                url=ctx.me.avatar_url
            )
            try:
                await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
            except:
                pass
            await ctx.send(embed=embed)
        else:
            raise errors.StreamerNotFound(
                self.bot.locales[lang]["error_streamer_not_found"].format(ctx.author))

    # @commands.command()
    # @commands.cooldown(4, 30, commands.BucketType.user)
    # @commands.has_permissions(administrator=True)
    # @commands.guild_only()
    # async def purge(self, ctx):
    #     def is_me(user):
    #         return ctx.me == user.author
    #
    #     deleted = await ctx.channel.purge(check=is_me)
    #     await ctx.message.delete()

    def __next(self, embed, clips, start, end, lang):
        medals = {
            1: "🥇",
            2: "🥈",
            3: "🥉"
        }
        embed.clear_fields()
        acc = 0
        for i in range(start, end):

            if acc * 3 >= 25:
                break
            try:
                if (i + 1) < 4:
                    embed.add_field(
                        name=f"{medals[i + 1]} {clips[i]['title']}",
                        value=self.bot.locales[lang]["field_value_view_clip"].format(
                            clips[i]['link'])
                    )
                else:
                    embed.add_field(
                        name=f"{clips[i]['title']}",
                        value=self.bot.locales[lang]["field_value_view_clip"].format(
                            clips[i]['link'])
                    )
                embed.add_field(
                    name=self.bot.locales[lang]["field_name_views"],
                    value=clips[i]["views"]
                )
                embed.add_field(
                    name=self.bot.locales[lang]["field_value_clipper"],
                    value=clips[i]["creator"]
                )
                embed.set_footer(
                    text=f"lyvego.com | Pages {end // 8}/{math.ceil(len(clips) / 8)}"
                )
                acc += 1

            except:
                break

    @commands.command(aliases=["topclips", "tc"])
    @commands.cooldown(4, 30, commands.BucketType.user)
    @commands.guild_only()
    async def topclip(self, ctx: commands.Context, streamer: str, amount=5):
        lang = await self.bot.getg_lang(ctx.guild.id)
        if amount > 100:
            raise Exception(self.bot.locales[lang]["error_amount_topclips"])
        try:
            clips = await top_clips(self.bot.http_session, streamer, parameters=f"&amount={amount}")
            if clips == None:
                raise errors.StreamerNotFound(
                    self.bot.locales[lang]["error_streamer_not_found"].format(ctx.author))
            clips = clips["clips"]
            if clips[0]:
                pass
            try:
                await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
            except:
                pass
        except (IndexError, KeyError):
            raise errors.ClipsNotFound(
                self.bot.locales[lang]["error_clips_not_found"].format(ctx.author))

        embed = discord.Embed(
            timestamp=dctt(),
            color=self.bot.color
        )
        embed.set_author(
            name=self.bot.locales[lang]["author_name_most_viewed_clips"].format(
                clips[0]["streamer"]["name"]),
            url=f"https://twitch.tv/{clips[0]['streamer']['name']}",
            icon_url=clips[0]["streamer"]["avatar"]
        )

        embed.set_thumbnail(
            url=clips[0]["thumbnail"]
        )
        start = 0
        end = 8
        self.__next(embed, clips, start, end, lang)

        if len(clips) * 3 <= 25:
            return await ctx.send(embed=embed)
        embed.set_footer(
            text=f"lyvego.com | Pages {end // 8}/{math.ceil(len(clips) / 8)}"
        )

        pages = await ctx.send(embed=embed)
        react_list = ["◀️", "▶️"]
        for reaction in react_list:
            await pages.add_reaction(reaction)

        def predicate(reaction, user):
            return ctx.message.author == user and str(reaction.emoji) in react_list

        start += 8
        end += 8
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=predicate, timeout=180.0)
            except asyncio.TimeoutError:
                try:
                    await ctx.message.delete()
                except:
                    pass
                await pages.delete()
                return

            if react_list[0] == str(reaction.emoji):
                self.__next(embed, clips, start, end, lang)

                start -= 8
                end -= 8
                if start < 0:
                    end = len(clips)
                    start = end - 8

            if react_list[1] == str(reaction.emoji):
                self.__next(embed, clips, start, end, lang)
                start += 8
                end += 8
                if end > len(clips):
                    start = 0
                    end = 8

            await pages.remove_reaction(reaction.emoji, user)
            await pages.edit(embed=embed)

    @commands.command(aliases=["locales"])
    @commands.is_owner()
    async def reload_locales(self, ctx):
        try:
            self.bot.load_locales()
        except Exception as e:
            return await ctx.send(f"Cannot load locales : {e}")

        await ctx.send(f"Locales loaded for those languages : **{' '.join(list(self.bot.locales.keys()))}**")


def setup(bot):
    bot.add_cog(Settings(bot))
