import asyncio
import datetime as dt
import json
import logging
import os
import time
from collections import namedtuple

import discord
from aiohttp import web
from discord.ext import commands

from src.emojis import flags
from src.utils import API_KEY, dctt


logger = logging.getLogger("lyvego")



class Receiver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.run_server())

    def on_live_embed(self, em: object, guild: discord.Guild):
        embed = discord.Embed(
            description=f"<:rec:703677659535769710> [{em.stream.name}]({em.stream.streamer.link})",
            color=int(f"0x{em.color}", 16),
            timestamp=dctt()
        )
        embed.set_footer(icon_url=guild.me.avatar_url)
        embed.add_field(name="Viewer", value=em.stream.viewer)
        embed.add_field(name="Game", value=em.stream.game.name)
        embed.set_thumbnail(url=em.stream.game.icon)
        embed.set_author(name=em.stream.streamer.name, url=em.stream.streamer.link, icon_url=em.stream.streamer.avatar)
        embed.set_image(url=em.stream.thumbnail)
        return embed

    @staticmethod
    def _json_object_hook(d: dict):
        return namedtuple('Events', d.keys())(*d.values())

    async def _stream_event(self, events):
        try:
            for event in events:
                try:
                    channel = self.bot.get_channel(int(event.channel))
                    embed = self.on_live_embed(event.embed, channel.guild)
                    msg = await channel.send(
                        embed=embed,
                        content=event.message
                    )
                except Exception as e:
                    logger.exception(e, exc_info=True)
        except Exception as e:
            logger.exception(e, exc_info=True)

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
                    logger.info(e, exc_info=True)
        except Exception as e:
            logger.info(e, exc_info=True)

    async def _follow_event(self, events):
        try:
            for event in events:
                try:
                    channel = self.bot.get_channel(int(event.channel))
                    embed = discord.Embed(
                        timestamp=dctt(),
                        color=self.bot.blue,
                        description=event.message
                    )
                    embed.set_author(
                        name=f"New follower for {event.details.username}",
                        icon_url=event.details.avatar
                    )
                    embed.set_footer(
                        text="New follow ❤️"
                    )
                    await channel.send(embed=embed)
                except:
                    pass
        except Exception as e:
            logger.info(e, exc_info=True)

    async def _ban_event(self, events):
        try:
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
                    logger.info(e, exc_info=True)
        except Exception as e:
            logger.info(e, exc_info=True)


    async def handler(self, request):
        if request.headers["SuperApi"] == API_KEY:
            data = await request.text()
            events = json.loads(data, object_hook=self._json_object_hook)
            print(events)
            event_type = events[0].type
            if event_type == "stream":
                await self._stream_event(events)
            elif event_type == "moderator":
                await self._moderator_event(events)
            elif event_type == "follow":
                await self._follow_event(events)
            elif event_type == "ban":
                await self._ban_event(events)

            return web.Response()


    async def webhook_handler(self, request):
        data = await request.json()
        user = self.bot.get_user(int(data['user']))
        logger.info("voted")
        embed = discord.Embed(
            title="TOP.GG upvote",
            description="Your vote has been register! Thank you❤️! You can vote again in 12 hours on the same [link](https://top.gg/bot/702648685263323187/vote).\nIf you have any question come over my [discord server](https://discord.gg/E4nVPd2)",
            timestamp=datetime.datetime.utcnow(),
            color=utils.COLOR
        )
        embed.set_thumbnail(url="https://top.gg/images/dblnew.png")
        embed.set_footer(
            text="Made by Taki#0853 (WIP)",
            icon_url=user.avatar_url
        )
        await user.send(embed=embed)
        # channel = self.bot.get_channel(702682984519696424)
        # await channel.send(data)
        return web.Response()

    async def test(self, request):
        return web.Response(text="yeee")

    async def run_server(self):
        app = web.Application()
        app.router.add_post("/", self.handler)
        app.router.add_post("/webhook", self.webhook_handler)
        app.router.add_get("/get", self.test)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        print("Server running")



def setup(bot):
    bot.add_cog(Receiver(bot))
