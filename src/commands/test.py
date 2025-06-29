from pathlib import Path

cur = Path("./")

for command in [str(x) for x in cur.iterdir() if x.is_file()]:
    print(command.replace("\\", ".")[:-3])