import os
import discord
from discord.ext import commands

# Configuration des intentions (intents)
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire le contenu des messages / commandes

# Création du bot avec le préfixe '!'
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"🎃 Bot Halloween connecté avec succès en tant que {bot.user} !")
    # Change l'activité du bot dans Discord
    await bot.change_presence(activity=discord.Game(name="Distribuer des bonbons 🍬 | !halloween"))

@bot.command()
async def halloween(ctx):
    """Commande de test pour vérifier que le bot répond !"""
    embed = discord.Embed(
        title="🎃 Joyeux Halloween ! 👻",
        description="Des bonbons ou un sort ? 🍬🧹\nTon bot Halloween tourne parfaitement sur ton NAS QNAP !",
        color=discord.Color.orange()
    )
    embed.set_footer(text="Hébergé sur QNAP via GitHub Container Registry 🚀")
    await ctx.send(embed=embed)

# Récupération du token depuis la variable d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Erreur : La variable d'environnement DISCORD_TOKEN n'a pas été trouvée !")
