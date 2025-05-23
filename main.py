import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = 1257169646101069895  # 🛑 Thay bằng Channel ID thật của bạn

scheduler = AsyncIOScheduler(timezone=timezone("Asia/Ho_Chi_Minh"))

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên: {bot.user}")
    scheduler.start()

    # Lên lịch chạy lúc 3h sáng giờ Việt Nam mỗi ngày
    scheduler.add_job(delete_old_messages, 'cron', hour=3, minute=0)

async def delete_old_messages():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Không tìm thấy kênh.")
        return

    now = datetime.utcnow()
    cutoff = now - timedelta(days=7)
    deleted_count = 0

    async for msg in channel.history(limit=None):
        if msg.created_at < cutoff:
            try:
                await msg.delete()
                deleted_count += 1
                await asyncio.sleep(1)
            except:
                continue

    print(f"[{datetime.now()}] ✅ Đã xóa {deleted_count} tin nhắn cũ hơn 7 ngày.")

bot.run("MTM3NTM0ODQ5ODg1MzAwMzMwNA.GOX7jF.J9WDPGyzGwpTVsUs_abMWrHMmfDpvaWsjxHE7k")  # 🛑 Dán token thật của bạn tại đây
