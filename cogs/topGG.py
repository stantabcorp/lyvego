import logging

import topgg
from discord.ext import commands, tasks

from src.constants import TOPGG_API_KEY

logger = logging.getLogger("covid-19")


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""
    __slots__ = ("bot", "topgg")

    def __init__(self, bot):
        self.bot = bot
        self.topgg = topgg.DBLClient(bot, TOPGG_API_KEY)
        self.update_stats().start()

    @tasks.loop(minutes=30, reconnect=True)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        try:
            await self.topgg.post_guild_count(shard_count=self.bot.shard_count)
            logger.info(f"Posted server count ({self.topgg.guild_count})")
        except Exception as e:
            logger.error(f"Failed to post server count\n{e.__class__.__name__}: {e}")


def setup(bot):
    bot.add_cog(TopGG(bot))
