import aiosqlite

DB_NAME = "voice_system.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS server_config (
                guild_id INTEGER PRIMARY KEY,
                category_id INTEGER,
                creator_channel_id INTEGER
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS active_channels (
                channel_id INTEGER PRIMARY KEY,
                owner_id INTEGER,
                guild_id INTEGER
            )
        """)
        await db.commit()

async def get_server_config(guild_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT category_id, creator_channel_id FROM server_config WHERE guild_id = ?", (guild_id,)) as cursor:
            return await cursor.fetchone()

async def set_server_config(guild_id: int, category_id: int, creator_channel_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("REPLACE INTO server_config (guild_id, category_id, creator_channel_id) VALUES (?, ?, ?)", (guild_id, category_id, creator_channel_id))
        await db.commit()

async def register_channel(channel_id: int, owner_id: int, guild_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO active_channels (channel_id, owner_id, guild_id) VALUES (?, ?, ?)", (channel_id, owner_id, guild_id))
        await db.commit()

async def remove_channel(channel_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM active_channels WHERE channel_id = ?", (channel_id,))
        await db.commit()

async def get_channel_owner(channel_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT owner_id FROM active_channels WHERE channel_id = ?", (channel_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def update_channel_owner(channel_id: int, new_owner_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE active_channels SET owner_id = ? WHERE channel_id = ?", (new_owner_id, channel_id))
        await db.commit()