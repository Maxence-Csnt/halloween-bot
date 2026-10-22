import os
import discord
from discord import app_commands

# Configuration des intentions (pas besoin d'intents privilégiés pour les slash commands de base !)
intents = discord.Intents.default()

class HalloweenBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Synchronise les commandes slash avec Discord
        await self.tree.sync()
        print("🎃 Commandes slash synchronisées avec succès !")

client = HalloweenBot()

@client.event
async def on_ready():
    print(f"👻 Bot Halloween connecté et prêt en tant que {client.user} !")
    await client.change_presence(activity=discord.Game(name="Distribuer des bonbons 🍬 | /halloween"))

# Définition de la commande slash /halloween
@client.tree.command(name="halloween", description="Reçois un message terrifiant et festif d'Halloween ! 🎃")
async def halloween(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎃 Joyeux Halloween ! 👻",
        description="Des bonbons ou un sort ? 🍬🧹\nTon bot Halloween tourne à merveille sur ton NAS QNAP !",
        color=discord.Color.orange()
    )
    embed.set_footer(text="Hébergé sur QNAP via GitHub Container Registry 🚀")
    await interaction.response.send_message(embed=embed)

# Récupération du token depuis la variable d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    client.run(TOKEN)
else:
    print("❌ Erreur : La variable d'environnement DISCORD_TOKEN n'a pas été trouvée !")
