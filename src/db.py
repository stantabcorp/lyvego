import os
import asyncio
import aiomysql


class Pool:
    async def insert(self, channel_id, message_id, streamer_id, on_end, on_change):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO bot_messages(channel_id, message_id, streamer_id, on_end, on_change) VALUES(%s, %s, %s, %s, %s)", (channel_id, message_id, streamer_id, on_end, on_change, ))
                await conn.commit()
                await cur.close()

    async def clean_all(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM bot_messages")
                await conn.commit()
                await cur.close()

    async def clean(self, message_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM bot_messages WHERE message_id=%s", (message_id, ))
                await conn.commit()
                await cur.close()

    async def select_message(self, streamer_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM bot_messages WHERE streamer_id=%s", (streamer_id, ))
                r = await cur.fetchall()
                await cur.close()
                return r


    async def get_topgg_user(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT is_accepted FROM topgg_users WHERE id=%s", (id, ))
                r = await cur.fetchone()
                await cur.close()
                return r["is_accepted"]

    async def insert_topgg(self, id, name):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO topgg_users(id, name) VALUES(%s, %s)", (id, name, ))
                await conn.commit()
                await cur.close()

    async def change_topgg(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE topgg_users SET is_accepted=0 WHERE id=%s", (id, ))
                await conn.commit()
                await cur.close()

    async def get_guilds_registered(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT discord_id FROM servers")
                r = await cur.fetchall()
                await cur.close()
                return [x[0] for x in r]


    def _close(self):
        self.pool.close()
        self.pool.wait_closed()
        self.loop.close()