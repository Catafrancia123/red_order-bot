![Version](https://img.shields.io/badge/version-1.2-red?style=plastic) [![Discord](https://img.shields.io/discord/990326151987724378?logo=discord&logoColor=white&color=5865F2)](https://discord.gg/JaDcEjNyfk) 
# red_order-bot
This repository is for one of my commisions in Discord for the SCP:RP faction: The Red Order. This repository is for open-source purposes.
> [!NOTE]
> The bot isn't fully completed yet, there are many commands to add or even debug. Also, this is the dev branch, expect lots of errors.
# Download
## Prerequesites/Dependencies
What you need to run the bot is the newest Python version, find [here](https://python.org "Official Python Website"). And some third party packages listed below:

- `discord.py` - This is what discord package the bot runs on.
- `rich` (local) - This adds colors and many other stuff you cant do in basic python.
- `playsound3` (local) - This plays a sound to alert you that the bot is ready.
- `python-dotenv` (local) - This is for loading a enviroment file for the discord token.
- `asqlite` (database) - This is the database the bot is going to be using.
- `jishaku` (misc) - Library for bot statistics, etc.

> [!NOTE]
> The packages with `(local)` tag have to be installed to prevent any errors in the file (i just used them to make your command line look better lol - catamapp).

If you want to install these packages fast, run the `setup.py` file.

# Running The Bot
## Setup
Before running the bot, you need a `.env` file with the code below:
```env
token="your_discord_bot_token_here"
```
Then you need a `config.toml` file as the config for the bot, with the code below:
```toml
title = "Config file"

[guild-settings]
admin_roles = [128880188670686008, 1378763072357011566, ...]
```
And you also need a database file (.db) with the SQL code below:
```sql
CREATE TABLE social_credit (username TEXT NOT NULL ON CONFLICT ABORT, amount INTEGER NOT NULL DEFAULT 0)
CREATE TABLE ration (username TEXT NOT NULL ON CONFLICT ABORT, amount INTEGER NOT NULL DEFAULT 0)
```

Sorry for the hassle!
## Running it
Run the `main.py` file and wait for the setup process to complete. Once you hear a *beep* sound, it's ready to use.
You can monitor the bot via the command line for errors and events.
