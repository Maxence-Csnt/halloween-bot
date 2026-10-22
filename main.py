import os
import random
import discord
from discord import app_codes if False else app_commands

intents = discord.Intents.default()

class HalloweenBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("🎃 Commandes slash d'Halloween synchronisées avec succès !")

client = HalloweenBot()

@client.event
async def on_ready():
    print(f"👻 Bot Halloween connecté en tant -> {client.user} !")
    await client.change_presence(activity=discord.Game(name="Distribuer des bonbons 🍬 | /don-bonbon"))

# 1. Commande /don-bonbon (Donner des bonbons à quelqu'un)
@client.tree.command(name="don-bonbon", description="Offre des bonbons terrifiants à un autre membre ! 🍬")
@app_commands.describe(membre="La personne à qui offrir des bonbons", nombre="Nombre de bonbons à offrir")
async def don_bonbon(interaction: discord.Interaction, membre: discord.Member, nombre: int):
    if membre == interaction.user:
        await interaction.response.send_message("❌ Tu ne peux pas t'offrir des bonbons à toi-même, petit gourmand ! 🎃", ephemeral=True)
        return
    
    if nombre <= 0:
        await interaction.response.send_message("❌ Il faut offrir au moins 1 bonbon ! 🦇", ephemeral=True)
        return

    embed = discord.Embed(
        title="🍬 Distribution de friandises !",
        description=f"{interaction.user.mention} offre **{nombre}** délicieux bonbons empoisonnés (ou pas) à {membre.mention} ! 🍫👻",
        color=discord.Color.orange()
    )
    embed.set_footer(text="Joyeux Halloween ! 🕸️")
    await interaction.response.send_message(embed=embed)

# 2. Commande /chance (Tenter sa chance ou affronter une autre personne)
@client.tree.command(name="chance", description="Affronte une autre personne à un jeu de chance d'Halloween 🎲🧙‍♂️")
@app_commands.describe(adversaire="La personne que tu souhaites défier")
async def chance(interaction: discord.Interaction, adversaire: discord.Member):
    if adversaire == interaction.user:
        await interaction.response.send_message("❌ Tu ne peux pas te défier toi-même ! Trouve une victime... un partenaire ! 🦇", ephemeral=True)
        return

    if adversaire.bot:
        await interaction.response.send_message("❌ Les robots ne jouent pas aux jeux de sorcellerie ! 🤖", ephemeral=True)
        return

    gagnant = random.choice([interaction.user, adversaire])
    perdant = adversaire if gagnant == interaction.user else interaction.user

    embed = discord.Embed(
        title="🎲 Duel de Sorcellerie !",
        description=f"{interaction.user.mention} affronte {adversaire.mention} dans un duel mystique...\n\n🏆 Les esprits ont choisi leur champion : **{gagnant.mention}** remporte le magot de bonbons ! 🍬\n💀 {perdant.mention} repart les mains vides et ensorcelé !",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Que le meilleur monstre gagne !")
    await interaction.response.send_message(embed=embed)

# 3. Commande /sort (Jeter un sort terrifiant à quelqu'un)
@client.tree.command(name="sort", description="Jette un sort maléfique à un membre du serveur ! 🧙‍♀️⚡")
@app_commands.describe(membre="La personne à ensorceler")
async def sort(interaction: discord.Interaction, membre: discord.Member):
    sorts = [
        "transformé en chat noir poilu 🐈‍⬛",
        "puni à nettoyer les chaudrons de la sorcière pendant 100 ans 🧹",
        "attaqué par une invasion de chauves-souris enragées 🦇",
        "gelé sur place par un souffle glacial d'outre-tombe ❄️👻",
        "maudit avec des murmures fantomatiques dans ses écouteurs 🎧💀"
    ]
    
    malediction = random.choice(sorts)

    embed = discord.Embed(
        title="⚡ Sortilège Lancé !",
        description=f"{interaction.user.mention} lance un sort terrifiant sur {membre.mention} !\n\n🔮 Résultat : Il se retrouve **{malediction}** !",
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text="Attention au retour de flamme... 🕯️")
    await interaction.response.send_message(embed=embed)

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    client.run(TOKEN)
else:
    print("❌ Erreur : La variable d'environnement DISCORD_TOKEN n'a pas été trouvée !")
