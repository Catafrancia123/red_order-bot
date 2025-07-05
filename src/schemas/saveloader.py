import sqlite3, asyncio

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

def edit(path: str, table: str, column: str, column_index: str, to_change: str, value):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    try:
        cursor.execute(f"UPDATE OR ABORT {table} SET {to_change} = {value} WHERE {column} = {column_index}")
    except sqlite3.OperationalError:
        raise KeyError("Data can not be updated, please check the data types of the column and the input.")
    conn.commit()

def add(path: str, table: str, column: str, value, default_value: bool = False):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    try:
        if not default_value:
            cursor.execute(f"INSERT OR ABORT INTO {table} ({column}) VALUES({value})")
        else:
            cursor.execute(f"INSERT OR ABORT INTO {table} ({column}) DEFAULT VALUES")
            
        conn.commit()
    except sqlite3.OperationalError:
        raise KeyError("Data can not be updated, please check the data types of the column and the input.")

def load(path: str, table: str, column: str, column_index: str, to_load: str) -> any:
    """
    Loads data from a database file.
    
    Args:
        path (str): The path of the database file.
        table (str): The table that the data is in.
        column (str): The data's column that hosts the name.
        column_index (str): The data's name.
        to_load (str): The data's column that hosts the value.
        
    Returns: 
        any: The data itself.
    """
    
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    try:
        #cursor.execute(f"SELECT {to_load} FROM {table} WHERE {column} = '{column_index}'")
        cursor.execute("SELECT value FROM settings WHERE name = 'admin_role'")
        data = cursor.fetchone()
    except Exception as e:
        raise KeyError(e)
            
    if data is None:
        raise KeyError("Data not found, please check the inputs again.")
    else:
        return data[0]

if __name__ == "__main__":
    print(load("save.db", "settings", "name", "admin_role", "value"))