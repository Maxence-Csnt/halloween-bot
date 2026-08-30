import os
import json
import asyncio
import re
import discord
from discord.ext import commands, tasks
import feedparser
from dotenv import load_dotenv

# Chargement des variables d'environnement 🔐
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROLE_ID = os.getenv("ROLE_ID")

# Flux RSS officiels 📡
YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UC2glyidA33L3S8-M8eY9M4Q"
BLOG_RSS = "https://www.home-assistant.io/atom.xml"
DATA_FILE = "state.json"

# Activation des Intents Discord ⚙️
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- GESTION DU FICHIER JSON --- 📁
def load_state():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"video_id": None, "message_id": None, "is_live": False}

def save_state(state):
    with open(DATA_FILE, "w") as f:
        json.dump(state, f, indent=4)

state = load_state()

# --- RÉCUPÉRATION DYNAMIQUE DU LIEN DE LA RELEASE NOTE --- 📖
async def get_latest_release_url():
    """Récupère l'URL exacte de la release note de la nouvelle mise à jour"""
    try:
        blog_feed = feedparser.parse(BLOG_RSS)
        for entry in blog_feed.entries:
            # Recherche du post de Release officiel (ex: "/release-20268/")
            if "release" in entry.title.lower() or re.search(r"\b202\d\.\d", entry.title):
                return entry.link, entry.title
    except Exception as e:
        print(f"⚠️ Erreur récupération Release Note : {e} ❌")
    
    return "https://www.home-assistant.io/blog/", "Release Note Home Assistant"

@bot.event
async def on_ready():
    # Application du statut "BOT EN BETA !" 🤖
    activite = discord.Activity(
        type=discord.ActivityType.watching, 
        name="BOT EN BETA !"
    )
    await bot.change_presence(activity=activite)
    
    print(f"✅ Bot connecté sous l'identifiant {bot.user} 🤖")
    check_updates.start()

# --- COMMANDE DE TEST 🧪 ---
@bot.command()
async def testlive(ctx):
    """Teste l'envoi du live puis sa mise à jour automatique avec le lien de la Release Note"""
    
    # Suppression automatique du message de la commande 🗑️
    try:
        await ctx.message.delete()
    except Exception:
        pass

    role_mention = f"<@&{ROLE_ID}>" if ROLE_ID else ""

    # 1. Embed initial (Début du Live) 🔴
    embed = discord.Embed(
        title="🔴 [TEST] Live Home Assistant : Release Party",
        description="Le live mensuel Home Assistant démarre ! Clique sur le bouton ci-dessous pour suivre le direct.",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url="https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg")

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Regarder le Live 📺", url="https://www.youtube.com/@home_assistant/streams", style=discord.ButtonStyle.link))

    test_msg = await ctx.send(content=f"🔴 {role_mention} Le live va commencer !", embed=embed, view=view)
    print("🧪 Test : Live initial publié 🔴")

    # Attente de 10 secondes pour simuler la fin du live ⏳
    await asyncio.sleep(10)

    # 2. Récupération dynamique de la vraie Release Note 📝
    release_url, release_title = await get_latest_release_url()

    new_embed = test_msg.embeds[0]
    new_embed.title = f"🎬 [TEST] Live Terminé — {release_title}"
    new_embed.description = "Le live est terminé ! Retrouve l'enregistrement vidéo ainsi que la release note officielle."
    new_embed.color = discord.Color.green()

    new_view = discord.ui.View()
    new_view.add_item(discord.ui.Button(label="Revoir le Live 📺", url="https://www.youtube.com/@home_assistant/streams", style=discord.ButtonStyle.link))
    new_view.add_item(discord.ui.Button(label="Release Note 📖", url=release_url, style=discord.ButtonStyle.link))

    await test_msg.edit(content=f"🎬 {role_mention} Le live est terminé et la release note est disponible !", embed=new_embed, view=new_view)
    print(f"✅ Test : Mis à jour avec {release_url} 🟢")

# --- BOUCLE AUTOMATIQUE 🔄 ---
@tasks.loop(minutes=2)
async def check_updates():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    role_mention = f"<@&{ROLE_ID}>" if ROLE_ID else ""

    # 1. Détection du Live sur YouTube 🔴
    try:
        yt_feed = feedparser.parse(YOUTUBE_RSS)
        if yt_feed.entries:
            latest_video = yt_feed.entries[0]
            video_id = latest_video.yt_videoid
            video_url = latest_video.link
            video_title = latest_video.title

            if state["video_id"] != video_id:
                embed = discord.Embed(
                    title=f"🔴 Live Home Assistant : {video_title}",
                    description="Le live mensuel Home Assistant démarre ! Clique sur le bouton ci-dessous pour suivre la présentation.",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg")

                view = discord.ui.View()
                view.add_item(discord.ui.Button(label="Regarder le Live 📺", url=video_url, style=discord.ButtonStyle.link))

                message = await channel.send(content=f"🔴 {role_mention} Le live commence !", embed=embed, view=view)

                state["video_id"] = video_id
                state["message_id"] = message.id
                state["is_live"] = True
                save_state(state)
                print(f"🎬 Nouveau live détecté : {video_title} 🔴")

    except Exception as e:
        print(f"⚠️ Erreur YouTube RSS : {e} ❌")

    # 2. Détection et mise à jour avec la nouvelle Release Note 📝
    if state["is_live"] and state["message_id"]:
        try:
            release_url, release_title = await get_latest_release_url()

            message = await channel.fetch_message(state["message_id"])

            new_embed = message.embeds[0]
            new_embed.title = f"🎬 Live Terminé — {release_title}"
            new_embed.description = "Le live est terminé ! Retrouve l'enregistrement vidéo ainsi que la release note officielle."
            new_embed.color = discord.Color.green()

            new_view = discord.ui.View()
            yt_url = f"https://www.youtube.com/watch?v={state['video_id']}"
            new_view.add_item(discord.ui.Button(label="Revoir le Live 📺", url=yt_url, style=discord.ButtonStyle.link))
            new_view.add_item(discord.ui.Button(label="Release Note 📖", url=release_url, style=discord.ButtonStyle.link))

            await message.edit(content=f"🎬 {role_mention} Le live est terminé et la release note officielle est disponible !", embed=new_embed, view=new_view)

            state["is_live"] = False
            save_state(state)
            print(f"✅ Message mis à jour avec la Release Note ({release_url}) 🟢")

        except discord.NotFound:
            print("❌ Message introuvable sur Discord.")
        except Exception as e:
            print(f"⚠️ Erreur mise à jour Release Note : {e} ❌")

bot.run(DISCORD_TOKEN)