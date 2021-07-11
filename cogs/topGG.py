import logging

import topgg
from discord.ext import commands, tasks
import asyncio
from src.constants import TOPGG_API_KEY
from main import Lyvego


logger = logging.getLogger("covid-19")


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""
    __slots__ = ("bot", "topgg")

    def __init__(self, bot):
        self.bot: Lyvego = bot
        self.topgg = topgg.DBLClient(bot, TOPGG_API_KEY)
        if not self.bot._debug:
            self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        while True:
            try:
                await self.topgg.post_guild_count(shard_count=self.bot.shard_count)
                logger.info(f"Posted server count ({self.topgg.guild_count})")
            except Exception as e:
                logger.error(f"Failed to post server count\n{e.__class__.__name__}: {e}")
            finally:
                await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(TopGG(bot))
