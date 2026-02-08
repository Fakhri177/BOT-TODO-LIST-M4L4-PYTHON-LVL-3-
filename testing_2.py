import discord
from discord.ext import commands
import sqlite3
from config import TOKEN

# =====================
# DATABASE SETUP
# =====================
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    task TEXT
)
""")
conn.commit()

# =====================
# BOT SETUP
# =====================
intents = discord.Intents.default()
intents.message_content = True  # WAJIB
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot login sebagai {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        await channel.send("Halo! Bot To-Do List sudah online. Aku adalah bot yang bisa membantumu menyimpan tugas yang harus dikerjakan. Denganku, semua tugasmu akan menjadi lebih terorganisir. Berikut adalah kumpulan perintah yang bisa kau gunakan :" \
        "\n !add [Nama tugas] - menambahkan tugas baru." \
        "\n !list - menampilkan daftar tugas saat ini." \
        "\n !delete [ID tugas] - menghapus tugas berdasarkan ID." \
        "\n !clear - menghapus semua tugas." \
        "\n !random - menampilkan tugas acak dari daftar tugasmu.")

    else:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")




# =====================
# COMMANDS
# =====================

# Tambah todo
@bot.command()
async def add(ctx, *, task: str):
    cursor.execute(
        "INSERT INTO todos (user_id, task) VALUES (?, ?)",
        (ctx.author.id, task)
    )
    conn.commit()
    await ctx.send(f"✅ To-do ditambahkan: **{task}**")

# Lihat todo
@bot.command()
async def list(ctx):
    cursor.execute(
        "SELECT id, task FROM todos WHERE user_id = ?",
        (ctx.author.id,)
    )
    todos = cursor.fetchall()

    if not todos:
        await ctx.send("📭 To-do list kamu kosong.")
        return

    message = "**📝 To-Do List Kamu:**\n"
    for todo_id, task in todos:
        message += f"{todo_id}. {task}\n"

    await ctx.send(message)

# Hapus todo
@bot.command()
async def delete(ctx, todo_id: int):
    cursor.execute(
        "DELETE FROM todos WHERE id = ? AND user_id = ?",
        (todo_id, ctx.author.id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        await ctx.send("❌ To-do tidak ditemukan.")
    else:
        await ctx.send("🗑️ To-do berhasil dihapus.")

@bot.command()
async def random(ctx):
    cursor.execute(
        "SELECT id, task FROM todos WHERE user_id = ? ORDER BY RANDOM() LIMIT 1",
        (ctx.author.id,)
    )
    todo = cursor.fetchone()

    if todo is None:
        await ctx.send("📭 Kamu belum punya to-do.")
        return

    todo_id, task = todo
    await ctx.send(f"🎲 **Kamu harus:**\n{todo_id}. {task}")

@bot.command()
async def clear(ctx):
    cursor.execute(
        "DELETE FROM todos WHERE user_id = ?",
        (ctx.author.id,)
    )
    conn.commit()
    await ctx.send("🧹 Semua to-do kamu telah dihapus.")
# =====================
# RUN BOT
# =====================
bot.run(TOKEN_ANDA)


