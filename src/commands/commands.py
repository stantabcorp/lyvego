import asyncio
import logging
import math
from typing import Union

import discord
from discord.ext import commands
from discord_slash.context import SlashContext

import errors
import src as utils
from main import Lyvego


logger = logging.getLogger("lyvego")


def __next(bot: Lyvego, embed: discord.Embed, clips, start, end, lang):
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
                    value=bot.locales[lang]["field_value_view_clip"].format(
                        clips[i]['link'])
                )
            else:
                embed.add_field(
                    name=f"{clips[i]['title']}",
                    value=bot.locales[lang]["field_value_view_clip"].format(
                        clips[i]['link'])
                )
            embed.add_field(
                name=bot.locales[lang]["field_name_views"],
                value=clips[i]["views"]
            )
            embed.add_field(
                name=bot.locales[lang]["field_value_clipper"],
                value=clips[i]["creator"]
            )
            embed.set_footer(
                text=f"lyvego.com | Pages {end // 8}/{math.ceil(len(clips) / 8)}"
            )
            acc += 1

        except:
            break


async def add_follow_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context], streamer, message=""):
    lang = await bot.getg_lang(ctx.guild.id)
    resp = await utils.post_streamer(
        ctx,
        bot.http_session,
        json=[
            {
                "type": "follow_announcement",
                "channel_id": ctx.channel.id,
                "streamer": streamer,
                "message": message if len(message)
                else bot.locales[lang]["message_started_following"],
                "color": bot.color_str,
                "update_message_on_change": False,
                "delete_message_on_change": False
            }
        ]
    )
    if resp.status in range(200, 300):

        embed = discord.Embed(
            description=bot.locales[lang]["description_configure_lyvego"].format(
                bot.lyvego_url),
            color=bot.color,
            timestamp=utils.dctt()
        )
        embed.set_author(
            name=f"{streamer} successfully added",
            icon_url=ctx.author.avatar_url
        )
        embed.set_thumbnail(
            url=ctx.guild.me.avatar_url
        )
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
        await ctx.send(embed=embed)
    else:
        logger.debug(f"Add follow : STATUS CODE {resp.status} for {streamer}")
        raise errors.StreamerNotFound(
            bot.locales[lang]["error_streamer_not_found"].format(ctx.author))


async def add_clip_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context], streamer):
    lang = await bot.getg_lang(ctx.guild.id)
    resp = await utils.post_streamer(
        ctx,
        bot.http_session,
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
            description=bot.locales[lang]["description_configure_lyvego"].format(
                bot.lyvego_url),
            color=bot.color,
            timestamp=utils.dctt()
        )
        embed.set_author(
            name=bot.locales[lang]["author_name_success_added"].format(
                streamer),
            icon_url=ctx.author.avatar_url
        )
        embed.set_thumbnail(
            url=ctx.guild.me.avatar_url
        )
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
        await ctx.send(embed=embed)
    else:
        logger.debug(f"Add clip : STATUS CODE {resp.status} for {streamer}")
        raise errors.StreamerNotFound(
            bot.locales[lang]["error_streamer_not_found"].format(ctx.author))


async def add_streamer_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context], streamer, message=""):
    lang = await bot.getg_lang(ctx.guild.id)
    resp = await utils.post_streamer(
        ctx,
        bot.http_session,
        json=[
            {
                "type": "live_announcement",
                "channel_id": ctx.channel.id,
                "streamer": streamer,
                "message": " ".join(message) if len(message) else bot.locales[lang]["message_stream_live"],
                "color": bot.color_str,
                "update_message_on_change": False,
                "delete_message_on_change": False
            }
        ]
    )
    if resp.status in range(200, 300):

        embed = discord.Embed(
            description=bot.locales[lang]["description_configure_lyvego"].format(
                bot.lyvego_url),
            color=bot.color,
            timestamp=utils.dctt()
        )
        embed.set_author(
            name=bot.locales[lang]["author_name_success_added"].format(
                streamer),
            icon_url=ctx.author.avatar_url
        )
        embed.set_thumbnail(
            url=ctx.guild.me.avatar_url
        )
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
        await ctx.send(embed=embed)
    else:
        logger.debug(f"Add streamer : STATUS CODE {resp.status} for {streamer}")
        raise errors.StreamerNotFound(
            bot.locales[lang]["error_streamer_not_found"].format(ctx.author))


async def remove_event_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context], event: str, streamer: str):
    lang = await bot.getg_lang(ctx.guild.id)
    resp = await utils.remove_user_event(ctx, bot.http_session, event, streamer)
    if resp.status >= 200 and resp.status < 300:
        embed = discord.Embed(
            description=bot.locales[lang]["description_configure_lyvego"].format(
                bot.lyvego_url),
            color=bot.color,
            timestamp=utils.dctt()
        )
        embed.set_author(
            name=bot.locales[lang]["author_name_success_removed"].format(
                streamer),
            icon_url=ctx.author.avatar_url
        )
        embed.set_thumbnail(
            url=ctx.guild.me.avatar_url
        )
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
        await ctx.send(embed=embed)
    else:
        logger.debug(f"Remove {event} : STATUS CODE {resp.status} for {streamer}")
        raise errors.StreamerNotFound(
            bot.locales[lang]["error_streamer_not_found"].format(ctx.author))


async def topclips_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context], streamer, amount):
    lang = await bot.getg_lang(ctx.guild.id)
    if amount > 100:
        raise Exception(bot.locales[lang]["error_amount_topclips"])
    try:
        clips = await utils.top_clips(bot.http_session, streamer, parameters=f"&amount={amount}")
        if clips == None:
            raise errors.StreamerNotFound(
                bot.locales[lang]["error_streamer_not_found"].format(ctx.author))
        clips = clips["clips"]
        if clips[0]:
            pass
        try:
            await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
        except:
            pass
    except (IndexError, KeyError):
        raise errors.ClipsNotFound(
            bot.locales[lang]["error_clips_not_found"].format(ctx.author))

    embed = discord.Embed(
        timestamp=utils.dctt(),
        color=bot.color
    )
    embed.set_author(
        name=bot.locales[lang]["author_name_most_viewed_clips"].format(
            clips[0]["streamer"]["name"]),
        url=f"https://twitch.tv/{clips[0]['streamer']['name']}",
        icon_url=clips[0]["streamer"]["avatar"]
    )

    embed.set_thumbnail(
        url=clips[0]["thumbnail"]
    )
    start = 0
    end = 8
    __next(bot, embed, clips, start, end, lang)

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
            reaction, user = await bot.wait_for('reaction_add', check=predicate, timeout=180.0)
        except asyncio.TimeoutError:
            try:
                await ctx.message.delete()
            except:
                pass
            await pages.delete()
            return

        if react_list[0] == str(reaction.emoji):
            __next(bot, embed, clips, start, end, lang)

            start -= 8
            end -= 8
            if start < 0:
                end = len(clips)
                start = end - 8

        if react_list[1] == str(reaction.emoji):
            __next(bot, embed, clips, start, end, lang)
            start += 8
            end += 8
            if end > len(clips):
                start = 0
                end = 8

        await pages.remove_reaction(reaction.emoji, user)
        await pages.edit(embed=embed)


async def help_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context]):
    lang = await bot.getg_lang(ctx.guild.id)
    react_list = ["<:lyvego:703585626053673060>",
                  "<:twitch:703585214261231626>", "⚙️"]
    embed = discord.Embed(
        color=bot.color,
        description=bot.locales[lang]["help_description_header"],
        timestamp=utils.dctt()
    )
    embed.set_author(
        name=bot.locales[lang]["author_name_commands"],
        icon_url=ctx.guild.me.avatar_url
    )
    embed.add_field(
        name=bot.locales[lang]["help_hub_twitch"].format(
            react_list[1]),
        value=bot.locales[lang]["help_hub_tap_to_see"].format(
            react_list[1]),
        inline=False
    )
    embed.add_field(
        name=bot.locales[lang]["help_hub_settings"].format(
            react_list[2]),
        value=bot.locales[lang]["help_hub_tap_to_see"].format(
            react_list[2]),
        inline=False
    )
    embed.set_footer(
        text="lyvego.com | help pages deleted in 5 mins",
        icon_url=ctx.guild.me.avatar_url
    )
    pages = await ctx.send(embed=embed)

    for reaction in react_list:
        await pages.add_reaction(reaction)

    def predicate(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in react_list

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', check=predicate, timeout=300.0)
        except asyncio.TimeoutError:
            try:
                await ctx.message.delete()
            except:
                pass
            await pages.delete()
            return

        if react_list[0] == str(reaction.emoji):
            embed = discord.Embed(
                color=bot.color,
                description=bot.locales[lang]["help_description_header"],
                timestamp=utils.dctt()
            )
            embed.set_author(
                name=bot.locales[lang]["author_name_commands"],
                icon_url=ctx.guild.me.avatar_url
            )
            embed.add_field(
                name=bot.locales[lang]["help_hub_twitch"].format(
                    react_list[1]),
                value=bot.locales[lang]["help_hub_tap_to_see"].format(
                    react_list[1]),
                inline=False
            )
            embed.add_field(
                name=bot.locales[lang]["help_hub_twitch"].format(
                    react_list[2]),
                value=bot.locales[lang]["help_hub_tap_to_see"].format(
                    react_list[2]),
                inline=False
            )
        elif react_list[1] == str(reaction.emoji):
            embed = discord.Embed(
                timestamp=utils.dctt(),
                color=bot.color,
            )
            embed.set_author(
                name=bot.locales[lang]["paginated_author_twitch_commands"],
                icon_url=ctx.guild.me.avatar_url
            )
            embed.add_field(
                name=f"{ctx.prefix}stream <streamer_name> [message : Optional]",
                value=bot.locales[lang]["help_streamer"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}follow <streamer_name> [message : Optional]",
                value=bot.locales[lang]["help_follow"],
                inline=False
            )

            embed.add_field(
                name=f"{ctx.prefix}clips <streamer_name> [message : Optional]",
                value=bot.locales[lang]["help_clips"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}remove <follow | stream | clips> <streamer_name>",
                value=bot.locales[lang]["help_remove"],
                inline=False
            )

            embed.add_field(
                name=f"{ctx.prefix}topclip <streamer_name> [amount]",
                value=bot.locales[lang]["help_topclip"],
                inline=False
            )

        elif react_list[2] == reaction.emoji:
            embed = discord.Embed(
                timestamp=utils.dctt(),
                color=bot.color
            )
            embed.set_author(
                name=bot.locales[lang]["paginated_author_settings_commands"],
                icon_url=ctx.guild.me.avatar_url
            )
            embed.add_field(
                name=f"{ctx.prefix}setprefix <new_prefix>",
                value=bot.locales[lang]["help_prefix"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}getprefix",
                value=bot.locales[lang]["help_getprefix"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}lang <--list | new_language>",
                value=bot.locales[lang]["help_language"].format(
                    ", ".join([x.upper() for x in bot.locales]).rstrip(", ")),
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}invite",
                value=bot.locales[lang]["help_invite"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}dashboard",
                value=bot.locales[lang]["help_dashboard"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}ping",
                value=bot.locales[lang]["help_ping"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}vote",
                value=bot.locales[lang]["help_vote"],
                inline=False
            )
            embed.add_field(
                name=f"{ctx.prefix}about",
                value=bot.locales[lang]["help_about"],
                inline=False
            )

        embed.set_footer(
            text="lyvego.com",
            icon_url=ctx.guild.me.avatar_url
        )
        await pages.remove_reaction(reaction.emoji, user)
        await pages.edit(embed=embed)

async def ping_command(bot:Lyvego, ctx: Union[SlashContext, commands.Context]):
    embed = discord.Embed(
        timestamp=utils.dctt(),
        color=bot.color,
        title="Bot latency"
    )
    embed.add_field(
        name="💗 Hearthbeat",
        value=f"`{sum([x[1] for x in bot.latencies]) / bot.shard_count:.3f}` ms"
    )
    embed.set_footer(
        text="lyvego.com"
    )
    await ctx.send(embed=embed)
    try:
        await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
    except:
        pass

async def vote_command(ctx: Union[SlashContext, commands.Context]):
    await ctx.send("https://top.gg/bot/702648685263323187/vote")
    try:
        await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
    except:
        pass

async def about_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context]):
    lang = await bot.getg_lang(str(ctx.guild.id))
    embed = discord.Embed(
        timestamp=utils.dctt(),
        color=bot.color,
        description=bot.locales[lang]["about_description"]
    )
    embed.add_field(
        name="Dashboard",
        value="[lyvego.com](https://lyvego.com/)"
    )
    embed.add_field(
        name="<:servers:693053697453850655> Servers",
        value=len(bot.guilds))
    embed.add_field(
        name="<:stack:693054261512110091> Shards",
        value=f"{ctx.guild.shard_id + 1}/{bot.shard_count}")
    embed.add_field(
        name="💗 Hearthbeat shards avg",
        value=f"`{sum([x[1] for x in bot.latencies]) / bot.shard_count:.3f}` ms"
    )
    await ctx.send(embed=embed)
    try:
        await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
    except:
        pass

async def invite_command(bot: Lyvego, ctx: Union[SlashContext, commands.Context]):
    lang = await bot.getg_lang(str(ctx.guild.id))
    embed = discord.Embed(
        title=bot.locales[lang]["title_invite_lyvego"],
        description=bot.locales[lang]["description_invite_lyvego"].format(
            "https://discord.com/oauth2/authorize?client_id=702648685263323187&permissions=445504&redirect_uri=https%3A%2F%2Flyvego.com%2Flogin&response_type=code&scope=bot%20identify%20email%20guilds"),
        timestamp=utils.dctt(),
        color=bot.color
    )
    embed.set_footer(
        text="lyvego.com",
        icon_url=ctx.guild.me.avatar_url
    )
    await ctx.send(embed=embed)
    try:
        await ctx.message.add_reaction("<a:valid_checkmark:709737579460952145>")
    except:
        pass