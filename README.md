# Endless Arm Center Patcher
This is a patcher that adds an endless mode to Bowser's Inside Story's arm center minigame, utilizing unused light orb arcs and custom score-keeping scripting to bring brand new depth to the game.
Simply run the program, follow the instructions, and play!

![Screenshot of Endless Arm Center 1.0.0 in-game](docs/1.0.0.png)

# Credits
[ThePurpleAnon](https://bsky.app/profile/thepurpleanon.bsky.social) ![Bluesky](endless_arm_center/files/img_soc_bsky.png) - Python Code, Endless Mode Design

[DimiDimit](https://github.com/DimiDimit) ![Github](endless_arm_center/files/img_soc_github.png) - [`mnllib.py`](https://github.com/MnL-Modding/mnllib.py) / [`mnlscript.py`](https://github.com/MnL-Modding/mnlscript.py)

# Running the Program
There are 3 ways to run this program, from easiest to most complicated:

1. Download the binary from [Releases](https://github.com/MnL-Modding/Endless-Arm-Center/releases) and run it. (Use the `.exe` for Windows, and the `.bin` for Linux)

3. Clone the repository, install the dependencies with Poetry (assuming you already have Poetry installed with `python3 -m pip install poetry`):
```bash
poetry install
```
and run the program through Poetry:
```bash
poetry run python3 -m endless_arm_center
```

4. Clone the repository, install the dependencies through `pip` with:
```bash
python3 -m pip install -r requirements.txt
```
and run it from the current directory with `python3 -m endless_arm_center`. Alternatively, it can be run through the `run.bat` if you use Windows.
