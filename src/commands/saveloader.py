import asqlite, asyncio

"""SQLite Notes:
1. Data Types
NULL - None
INTEGER - int
STRING - str
REAL - decimals
BLOB - any 

1.1 Data Type Requirements
NN (Not Null) - The data must not be empty.
"""

async def edit(path: str, table: str, column: str, value: str):
    async with asqlite.connect(path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"UPDATE OR ABORT {table} SET {column} = {value}")
            await conn.commit()

async def add(path: str, table: str, column: str, value: str):
    async with asqlite.connect(path) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                                INSERT OR ABORT INTO {table} ({column}) VALUES({value})""")
            await conn.commit()

async def load(path: str, table: str, column: str, column_index: str,  to_load: str) -> any:
    async with asqlite.connect(path) as conn:
        async with conn.cursor() as cursor:
            data = await cursor.execute(f"SELECT {to_load} FROM {table} WHERE {column} = {column_index}")
            
            if data is None:
                raise KeyError("Data not found, please check the inputs again.")
            else:
                return data

print(asyncio.run(load("../save.db", "settings", "name")))