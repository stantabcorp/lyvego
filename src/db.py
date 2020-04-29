import os
from databases import Database
import asyncio
import aiomysql

HOST = os.environ["HOST"]
PORT = 3306
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]

class Pool:
    async def _connect(self):

        if not self._pool_created:
            print("creating pool")

            self.pool = await aiomysql.create_pool(
                host=HOST,
                port=PORT,
                user=USER,
                password=PASSWORD,
                db=USER,
                loop=self.pool_loop
            )
            self._pool_created = True
            self.connected = True
            # await self.pool.connect()

    async def main(self):
        if not self.connected:
            await self._connect()

        # await self.clean()
        # await self.insert()
        await self.query()

    async def insert(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO bot_messages(channel_id, message_id, streamer_id) VALUES(%s, %s, %s)", ("test", "test", "test", ))
                await conn.commit()
                await cur.close()

    async def clean(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM bot_messages")
                await conn.commit()
                await cur.close()


    async def query(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM bot_messages")
                (r,) = await cur.fetchall()
                print(r)
                await cur.close()


# if __name__ == "__main__":


#     loop = asyncio.get_event_loop()
#     pool = Pool(loop=loop)
#     loop.run_until_complete(pool.main())
