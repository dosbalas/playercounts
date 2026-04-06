import discord
import requests
import asyncio
import os

# ==============================
# CONFIG
# ==============================
SERVER_ID = "38544553"  # Cambia esto si cambia tu server
UPDATE_INTERVAL = 60    # segundos (cada cuánto se actualiza)

# ==============================
# DISCORD CONFIG
# ==============================
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# ==============================
# FUNCION PARA OBTENER DATOS
# ==============================
def get_server_data():
    try:
        url = f"https://api.battlemetrics.com/servers/{SERVER_ID}"
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            print(f"Error HTTP: {res.status_code}")
            return None, None

        json_data = res.json()
        data = json_data["data"]["attributes"]

        players = data.get("players")
        max_players = data.get("maxPlayers")

        return players, max_players

    except Exception as e:
        print("Error al obtener datos:", e)
        return None, None

# ==============================
# EVENTO PRINCIPAL
# ==============================
@client.event
async def on_ready():
    print(f"✅ Bot en línea como: {client.user}")

    while True:
        players, max_players = get_server_data()

        if players is not None:
            status_text = f"{players}/{max_players} Jugadores"
        else:
            status_text = "Servidor offline ❌"

        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=status_text
        )

        await client.change_presence(activity=activity)

        await asyncio.sleep(UPDATE_INTERVAL)

# ==============================
# INICIO DEL BOT
# ==============================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ No se encontró el TOKEN. Asegúrate de configurarlo como variable de entorno.")
else:
    client.run(TOKEN)