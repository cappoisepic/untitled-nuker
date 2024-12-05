import discord
import asyncio

ASCII_ART = r"""
██╗   ██╗███╗   ██╗████████╗██╗████████╗██╗     ███████╗██████╗
██║   ██║████╗  ██║╚══██╔══╝██║╚══██╔══╝██║     ██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║   ██║   ██║   ██║   ██║     █████╗  ██║  ██║
██║   ██║██║╚██╗██║   ██║   ██║   ██║   ██║     ██╔══╝  ██║  ██║
╚██████╔╝██║ ╚████║   ██║   ██║   ██║   ███████╗███████╗██████╔╝
 ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝   ╚═╝   ╚══════╝╚══════╝╚═════╝
███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗
████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

MENU_TEXT = """
                            - :3
                                version : 0.2 
                                    by cappo 
---------------------------menu---------------------------
 | * token - bot token
 | * cname - channel name
 | * msg   - message/content
 | * start - starts the bot
 | * exit  - exit
----------------------------------------------------------

"""

def gradient_text(text, start_color, end_color):
    lines = text.splitlines()
    total_lines = len(lines)
    return "\n".join(
        f"\033[38;2;{int((1 - i / max(1, total_lines - 1)) * start_color[0] + i / max(1, total_lines - 1) * end_color[0])};"
        f"{int((1 - i / max(1, total_lines - 1)) * start_color[1] + i / max(1, total_lines - 1) * end_color[1])};"
        f"{int((1 - i / max(1, total_lines - 1)) * start_color[2] + i / max(1, total_lines - 1) * end_color[2])}m"
        + line + "\033[0m" if line.strip() else line
        for i, line in enumerate(lines)
    )

def display_menu():
    print(gradient_text(ASCII_ART, (0, 0, 255), (255, 0, 0)))

class MeowBot:
    def __init__(self):
        self.bot_token = self.spam_channel_name = self.spam_message = None
        self.client = discord.Client(intents=discord.Intents.all())
        self.spam_delay = 0

    async def on_ready(self):
        guild = self.client.guilds[0] if self.client.guilds else None
        if not guild:
            print("\033[91mno servers\033[0m")
            await self.client.close()
            return
        await self.spam_actions(guild)

    async def spam_actions(self, guild):
        while True:
            try:
                if self.spam_channel_name:
                    await guild.create_text_channel(self.spam_channel_name)
                    await asyncio.sleep(self.spam_delay)

                if self.spam_message:
                    for channel in guild.text_channels:
                        await channel.send(self.spam_message)
                        await asyncio.sleep(self.spam_delay)

            except Exception as e:
                print(f"\033[91merror: {e}\033[0m")

    async def start_bot(self):
        try:
            await self.client.start(self.bot_token)
        except Exception as e:
            print(f"\033[91mfailed to start bot: {e}\033[0m")

    def get_user_input(self):
        while True:
            command = input("command: ").strip().lower()
            if command == "token": self.bot_token = input("").strip()
            elif command == "cname": self.spam_channel_name = input("").strip()
            elif command == "msg": self.spam_message = input("").strip()
            elif command == "start":
                if not self.bot_token: print("\033[91merror: no token provided\033[0m")
                elif not (self.spam_channel_name or self.spam_message): 
                    print("\033[91merror: provide atleast a channel name or message to spam\033[0m")
                else: return
            elif command == "exit": exit(0)
            else: print("\033[91minvalid command\033[0m")

async def main():
    display_menu()
    await asyncio.sleep(1)
    print(gradient_text(MENU_TEXT, (0, 0, 255), (255, 0, 0)))
    bot = MeowBot()
    bot.get_user_input()
    await bot.start_bot()

if __name__ == "__main__":
    asyncio.run(main())