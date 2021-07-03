import datetime as dt

import aiomysql


class Pool:
    async def insert(self, channel_id, message_id, streamer_id, on_end, on_change):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO bot_messages(channel_id, message_id, streamer_id, on_end, on_change) VALUES(%s, %s, %s, %s, %s)",
                    (channel_id, message_id, streamer_id, on_end, on_change,))
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
                await cur.execute("DELETE FROM bot_messages WHERE message_id=%s", (message_id,))
                await conn.commit()
                await cur.close()

    async def clean_by_streamer(self, streamer_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM bot_messages WHERE streamer_id=%s", (streamer_id,))
                await conn.commit()
                await cur.close()

    async def select_message(self, streamer_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT * FROM bot_messages WHERE streamer_id=%s", (streamer_id,))
                r = await cur.fetchall()
                await cur.close()

                return r

    async def get_topgg_user(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT is_accepted FROM topgg_users WHERE id=%s", (id,))
                r = await cur.fetchone()
                await cur.close()

                return r["is_accepted"]

    async def insert_topgg(self, id, name):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO topgg_users(id, name) VALUES(%s, %s)", (id, name,))
                await conn.commit()
                await cur.close()

    async def insert_annonce(self, owner_id, guild_id, enable):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO annonce_notif(owner_id, guild_id, enable) VALUES(%s, %s, %s)",
                                  (owner_id, guild_id, enable,))
                await conn.commit()
                await cur.close()

    async def get_annonce(self, owner_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT enable FROM annonce_notif WHERE owner_id=%s", (owner_id,))
                r = await cur.fetchone()
                await cur.close()
                return r["enable"]

    async def change_annonce(self, owner_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE annonce_notif SET enable=0 WHERE owner_id=%s", (owner_id,))
                await conn.commit()
                await cur.close()

    async def change_topgg(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE topgg_users SET is_accepted=0 WHERE id=%s", (id,))
                await conn.commit()
                await cur.close()

    async def get_guilds_registered(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT discord_id FROM servers")
                r = await cur.fetchall()
                await cur.close()
                return [x[0] for x in r]

    async def getg_prefix(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT prefix FROM servers WHERE discord_id=%s", (id,))
                prefix, = await cur.fetchone()
                await cur.close()

                return prefix

    async def getg_lang(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT lang FROM servers WHERE discord_id=%s", (id,))
                lang, = await cur.fetchone()
                await cur.close()

                return lang

    async def set_prefix(self, id, prefix):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE servers SET prefix=%s WHERE discord_id=%s", (prefix, id,))
                await conn.commit()
                await cur.close()

    async def set_lang(self, id, lang):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE servers SET lang=%s WHERE discord_id=%s", (lang, id,))
                await conn.commit()
                await cur.close()

    async def update_messages(self, id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE bot_messages SET updated_at=%s WHERE streamer_id=%s AND on_change=1",
                                  (dt.datetime.now(), id,))
                await conn.commit()
                await cur.close()

    async def get_server_role_activity(self, server_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT role_name FROM servers_change_role WHERE server_id=%s", (server_id,))
                role, = await cur.fetchone()
                await cur.close()

                return role

    async def update_server_role_activity(self, server_id, role_name):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("UPDATE servers_change_role SET updated_at=%s, role_name=%s WHERE server_id=%s",
                                  (dt.datetime.now(), role_name, server_id,))
                await conn.commit()
                await cur.close()

    async def insert_server_role_activity(self, server_id, role_name):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO servers_change_role(server_id, role_name) VALUES(%s, %s) ON DUPLICATE KEY UPDATE role_name=%s, updated_at=%s",
                    (server_id, role_name, role_name, dt.datetime.now()))
                await conn.commit()
                await cur.close()

    async def remove_server_role_activity(self, server_id, role_name):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "DELETE FROM servers_change_role WHERE role_name=%s",
                    (role_name, ))
                await conn.commit()
                await cur.close()

    async def _close(self):
        self.pool.close()
        await self.pool.wait_closed()
        self.loop.close()
