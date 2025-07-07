import subprocess, sys, os
packages = ["rich", "discord.py", "playsound3", "python-dotenv", "jishaku", "asqlite"]

def clear():
    if sys.platform.startswith(('win32')):
        os.system('cls')
    elif sys.platform.startswith(('linux', 'cygwin', 'darwin', 'freebsd')):
        os.system('clear')

clear()
print("Setup\n")
subprocess.run([sys.executable, "-m", "pip", "install", "-U", "pip", "-q"], check=True)
counter = 1
for package in packages:
    subprocess.run([sys.executable, "-m", "pip", "install", package,  "-q", "-U"], check=True)
    print(f"[OK] {package} has been installed. (PKG-{counter:02d})")

    counter += 1
