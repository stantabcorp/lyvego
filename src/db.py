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
                print(r)
                await cur.close()
                return r


    async def query(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM bot_messages")
                r = await cur.fetchall()
                await cur.close()
                return r
