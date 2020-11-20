import asyncio
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
    __slots__ = ("bot")
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.run_server())

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
        embed.set_author(name=em.stream.streamer.name, url=em.stream.streamer.link, icon_url=em.stream.streamer.avatar)
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
                                channel = self.bot.get_channel(int(event.channel))
                                msg = await channel.fetch_message(int(message["message_id"]))
                                await msg.delete()
                        except:
                            pass
                except Exception as exc:
                    logger.exception(f"receiver.py line 68: {exc}", exc_info=True)
                await self.bot.clean_by_streamer(event.streamer)
                logger.info(f"{event.streamer} ended")
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
                                channel = self.bot.get_channel(int(event.channel))
                                msg = await channel.fetch_message(int(message["message_id"]))
                                embed = self.on_live_embed(event.embed, channel.guild)
                                await msg.edit(content=event.message, embed=embed)
                                await self.bot.update_messages(message["streamer_id"])
                                tmp_msg.append(msg.id)
                                logger.info(f"{msg.id} edited")
                        except Exception as e:
                            logger.exception(e, exc_info=True)
                else:
                    logger.info(f"{event.streamer} started")
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
                    logger.info(e, exc_info=True)
        except Exception as e:
            logger.info(e, exc_info=True)

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
                logger.info(e, exc_info=True)

    async def handler(self, request):
        if request.headers["SuperApi"] == API_KEY:
            data = await request.text()
            events = json.loads(data, object_hook=self._json_object_hook)
            event_type = events[0].type
            # print(event_type)
            if event_type == "stream":
                await self._stream_event(events)
            # elif event_type == "moderator":
            #     await self._moderator_event(events)
            elif event_type == "follow":
                await self._follow_event(events)
            # elif event_type == "ban":
            #     await self._ban_event(events)
            elif event_type == "clip":
                await self._clips_event(events)

            return web.Response()

    async def webhook_handler(self, request):
        data = await request.json()
        resp = web.Response()
        user = self.bot.get_user(int(data['user']))
        channel = self.bot.get_channel(715158139242020915)
        await channel.send("**{0}** just voted for **Lyvego** OwO".format(user.name))
        return resp
        # try:
        #     await self.bot.insert_topgg(str(user.id), str(user.name))
        # except: # already in the db
        #     pass
        # is_accepted = await self.bot.get_topgg_user(user.id)
        # if not is_accepted:
        #     return
        # embed = discord.Embed(
        #     title="TOP.GG upvote",
        #     description="Your vote has been registered ! Thank you ❤️\nYou can vote again in 12 hours on the same [link](https://top.gg/bot/702648685263323187/vote).\nIf you have any question come over our [discord server](https://discord.gg/E4nVPd2)\nYou can react below for the next 360s to disable notification on upvote.",
        #     timestamp=dctt(),
        #     color=self.bot.blue
        # )
        # embed.set_thumbnail(url="https://top.gg/images/dblnew.png")
        # embed.set_footer(
        #     text="lyvego.com",
        #     icon_url=user.avatar_url
        # )
        # dm_notif = await user.send(embed=embed)

        # bot_reaction = await dm_notif.add_reaction("<a:wrong_checkmark:709737435889664112>")

        # def check(reaction, user_react):
        #     return user == user_react and "<a:wrong_checkmark:709737435889664112>" == str(reaction.emoji)

        # while 1:
        #     try:
        #         logger.info(f"wait for reaction {user.name}")
        #         reaction, user_react = await self.bot.wait_for('reaction_add', check=check, timeout=360.0)
        #     except asyncio.TimeoutError:
        #         await dm_notif.remove_reaction(bot_reaction, dm_notif.author)
        #         return
        #         # return await dm_notif.delete()

        #     if "<a:wrong_checkmark:709737435889664112>" == str(reaction.emoji):
        #         try:
        #             await self.bot.change_topgg(str(user.id))
        #             break
        #         except Exception as e:
        #             logger.exception(e, exc_info=True)

        # try:
        #     success_disable = await user.send("Successfully disabled")
        #     await success_disable.add_reaction("<a:valid_checkmark:709737579460952145>")
        #     await dm_notif.remove_reaction(bot_reaction, dm_notif.author)
        # except Exception as e:
        #     logger.exception(e, exc_info=True)

        # await channel.send(data)

    # async def test(self, request):
    #     return web.Response(text="yeee")

    async def status(self, request):
        hearthbeat = f"{sum([x[1] for x in self.bot.latencies]) / self.bot.shard_count:.3f}"
        return web.Response(body=hearthbeat, status=200)

    async def run_server(self):
        app = web.Application(loop=self.bot.loop)
        app.router.add_post("/lyvego", self.handler)
        app.router.add_get("/ping", self.status)
        app.router.add_post("/webhook", self.webhook_handler)
        # app.router.add_get("/get", self.test)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '', 9886)
        await site.start()
        print("Server running")


def setup(bot):
    bot.add_cog(Receiver(bot))
