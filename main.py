import discord
from discord.ext import commands
import os
import asyncio
from database import init_db
from keep_alive import keep_alive

class VoiceSystemBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self):
        await init_db()
        await self.load_extension("cogs.voice_manager")
        await self.load_extension("cogs.voice_commands")
        await self.tree.sync()
        print("Mã nguồn khởi tạo hoàn tất. Cây lệnh đã đồng bộ.")

bot = VoiceSystemBot()

@bot.event
async def on_ready():
    print(f"Xác thực thành công. ID: {bot.user.id}")

if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Lỗi: Không tìm thấy DISCORD_TOKEN.")