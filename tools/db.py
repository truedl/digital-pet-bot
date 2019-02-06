import aiosqlite

class Database:
    def __init__(self, file):
        self.file = file

    async def query(self, sql):
        async with aiosqlite.connect(self.file) as db:
            await db.execute(sql)
            await db.commit()

    async def fetch(self, sql):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(sql)
            rows = await cursor.fetchall()
            await cursor.close()
        return rows
