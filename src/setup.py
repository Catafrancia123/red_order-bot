import subprocess, sys, os, asyncio
packages = ["rich", "discord.py", "playsound3", "python-dotenv", "jishaku", "asqlite"]

def clear():
    if sys.platform.startswith(('win32')):
        os.system('cls')
    elif sys.platform.startswith(('linux', 'cygwin', 'darwin', 'freebsd')):
        os.system('clear')

def install_pkg():
    clear()
    print("Setup\n")
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "pip", "-q"], check=True)
    counter = 1
    for package in packages:
        subprocess.run([sys.executable, "-m", "pip", "install", package,  "-q", "-U"], check=True)
        print(f"[OK] {package} has been installed. (PKG-{counter:02d})")

        counter += 1

async def setup_db():
    import asqlite
    tables = ["social_credit", "ration"]
    async with asqlite.connect("save.db") as conn, conn.cursor() as cursor:
        for table in tables:
            cursor.execute(f"CREATE TABLE {table} IF NOT EXISTS (username TEXT NOT NULL ON CONFLICT ABORT, amount INTEGER NOT NULL DEFAULT 0)")
    print("[OK] Database has been set up.")
    
if __name__ == "__main__":
    install_pkg()
    asyncio.run(setup_db)