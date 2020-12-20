import datetime as dt
import json
import logging
import time
from collections import namedtuple

import discord
from aiohttp import web
from discord.ext import commands
from src.constants import API_KEY
from src.utils import dctt

logger = logging.getLogger("lyvego")


class Receiver(commands.Cog):
    __slots__ = ("bot", "_last_follow", "_last_live", "_last_clip")

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.run_server())
        self._last_follow = None
        self._last_live = None
        self._last_clip = None

    def on_live_embed(self, em, guild: discord.Guild):
        embed = discord.Embed(
            description=f"<:rec:703677659535769710> [{em.stream.name}]({em.stream.streamer.link})",
            color=int(f"0x{em.color}", 16),
            timestamp=dctt()
        )
        embed.set_footer(icon_url=guild.me.avatar_url)
        embed.add_field(name="Viewer", value=em.stream.viewer)
        embed.add_field(name="Game", value=em.stream.game.name)
        embed.set_thumbnail(url=em.stream.game.icon)
        embed.set_author(name=em.stream.streamer.name,
                         url=em.stream.streamer.link, icon_url=em.stream.streamer.avatar)
        embed.set_image(url=em.stream.thumbnail + f"?{time.time()}")
        embed.set_footer(text="lyvego.com")
        return embed

    @staticmethod
    def _json_object_hook(d: dict):
        return namedtuple('Events', d.keys())(*d.values())

    async def _clips_event(self, events):
        for event in events:
            try:
                channel = self.bot.get_channel(int(event.channel))
            except:
                continue
            for clip in event.clips:
                try:
                    await channel.send(f"**{clip.title}**\n{clip.link}")
                except:
                    pass

    async def _stream_event(self, events):
        for event in events:
            if event.status == "ended":
                try:
                    messages = await self.bot.select_message(event.streamer)
                    for message in messages:
                        try:
                            if message["on_end"] and event.updates.on_end:
                                channel = self.bot.get_channel(
                                    int(event.channel))
                                msg = await channel.fetch_message(int(message["message_id"]))
                                await msg.delete()
                        except:
                            pass
                except Exception as exc:
                    logger.exception(
                        f"receiver.py line 68: {exc}", exc_info=True)
                await self.bot.clean_by_streamer(event.streamer)
                # logger.info(f"{event.streamer} ended")
            elif event.status == "changed":
                messages = await self.bot.select_message(event.streamer)
                checker = []
                for c in messages:
                    for v in c.values():
                        checker.append(v)
                if event.streamer in checker and event.channel in checker:
                    tmp_msg = []
                    for message in messages:
                        try:
                            if message["on_change"] and message["message_id"] not in tmp_msg:
                                channel = self.bot.get_channel(
                                    int(event.channel))
                                msg = await channel.fetch_message(int(message["message_id"]))
                                embed = self.on_live_embed(
                                    event.embed, channel.guild)
                                await msg.edit(content=event.message, embed=embed)
                                await self.bot.update_messages(message["streamer_id"])
                                tmp_msg.append(msg.id)
                                # logger.info(f"{msg.id} edited")
                        except Exception as e:
                            logger.exception(e, exc_info=True)
                else:
                    # logger.info(f"{event.streamer} started")
                    channel = self.bot.get_channel(int(event.channel))
                    embed = self.on_live_embed(event.embed, channel.guild)
                    msg = await channel.send(
                        embed=embed,
                        content=event.message
                    )
                    await self.bot.insert(
                        event.channel, str(msg.id), event.streamer,
                        event.updates.on_end, event.updates.on_change)

    async def _moderator_event(self, events):
        try:
            for event in events:
                try:
                    channel = self.bot.get_channel(int(event.channel))
                    embed = discord.Embed(
                        timestamp=dctt(),
                        description=event.message,
                        color=self.bot.green
                    )
                    embed.set_author(
                        name=f"New moderator for {event.details.username}",
                        icon_url="https://cdn4.iconfinder.com/data/icons/game-of-thrones-4/64/game_of_thrones_game_thrones_series_sword_weapon_lightbringer_fire-512.png"
                    )
                    embed.set_footer(
                        text="New moderator"
                    )
                    await channel.send(embed=embed)
                except Exception as e:
                    logger.exception(e, exc_info=True)
        except Exception as e:
            logger.exception(e, exc_info=True)

    async def _follow_event(self, events):
        for event in events:
            try:
                channel = self.bot.get_channel(int(event.channel))
                embed = discord.Embed(
                    timestamp=dctt(),
                    color=self.bot.blue,
                    description=event.message
                )
                embed.set_author(
                    name=f"{event.details.username}",
                    icon_url=event.details.avatar
                )
                embed.set_footer(
                    text="New follow 💜"
                )
                await channel.send(embed=embed)
            except:
                pass

    async def _ban_event(self, events):
        for event in events:
            try:

                channel = self.bot.get_channel(int(event.channel))
                embed = discord.Embed(
                    timestamp=dctt(),
                    color=self.bot.red,
                    description=event.message
                )
                embed.set_author(
                    name=f"Ban announce for {event.details.username}",
                    icon_url="https://cdn2.iconfinder.com/data/icons/superhero-neon-circle/64/1-superhero-512.png"
                )
                embed.set_thumbnail(
                    url=event.details.avatar
                )
                embed.set_footer(
                    text="Ban hammer 🔨"
                )
                await channel.send(embed=embed)
            except Exception as e:
                logger.exception(e, exc_info=True)

    async def handler(self, request):
        if request.headers["SuperApi"] == API_KEY:
            data = await request.text()
            events = json.loads(data, object_hook=self._json_object_hook)
            event_type = events[0].type
            if event_type == "stream":
                self._last_live = dt.datetime.now()
                await self._stream_event(events)
            # elif event_type == "moderator":
            #     await self._moderator_event(events)
            elif event_type == "follow":
                self._last_follow = dt.datetime.now()
                await self._follow_event(events)
            # elif event_type == "ban":
            #     await self._ban_event(events)
            elif event_type == "clip":
                self._last_clip = dt.datetime.now()
                await self._clips_event(events)

            return web.Response(status=200)
        return web.Response(status=401)

    async def webhook_handler(self, request):
        try:
            data = await request.json()
            user = self.bot.get_user(int(data['user']))
            channel = self.bot.get_channel(715158139242020915)
            await channel.send("**{0}** just voted for **Lyvego** OwO".format(user.name))
            return web.Response(status=200)
        except:
            return web.Response(status=404)

    async def status(self, request):
        hearthbeat = f"{sum([x[1] for x in self.bot.latencies]) / self.bot.shard_count:.3f}"
        return web.Response(body=hearthbeat, status=200)

    async def run_server(self):
        app = web.Application(loop=self.bot.loop, logger=logger)
        app.router.add_post("/lyvego", self.handler)
        app.router.add_get("/ping", self.status)
        app.router.add_post("/webhook", self.webhook_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '', 9886)
        await site.start()
        print("Server running")

    @commands.command()
    @commands.is_owner()
    async def events(self, ctx):
        await ctx.send("Last live : **{0._last_live}** --- Last follow : **{0._last_follow} --- Last clip : {0._last_clip}".format(self))

    @commands.command(aliases=["sr"])
    @commands.guild_only()
    @commands.is_owner()
    async def setrole(self, ctx, role: discord.Role):
        await self.bot.insert_server_role_activity(ctx.guild.id, role.name)
        await ctx.send(f"{role.name} successfully added")


def setup(bot):
    bot.add_cog(Receiver(bot))
