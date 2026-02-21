import discord
import os
import aiohttp
import asyncio
from datetime import datetime
import re  # necessário para detectar links de imagens

# ==============================
# CONFIGURAÇÕES DO BOT
# ==============================
TOKEN = "COLOQUE_TOKEN_DO_SEU_BOT"
PREFIXO = "!"
DOWNLOADS_DIR = "exportacoes"

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)


# ==============================
# FUNÇÃO PRINCIPAL DE EXPORTAÇÃO
# ==============================
async def exportar_canal(canal: discord.TextChannel):
    """Exporta mensagens e imagens (via link direto, sem baixar)."""
    pasta_canal = os.path.join(DOWNLOADS_DIR, f"{canal.guild.name}_{canal.name}")
    os.makedirs(pasta_canal, exist_ok=True)
    mensagens = []

    async for msg in canal.history(limit=None, oldest_first=True):
        mensagens.append(msg)

    html = [
        "<html><head><meta charset='utf-8'>",
        f"<title>Exportação de #{canal.name}</title>",
        "<style>"
        "body{font-family:Arial;background:#2c2f33;color:#dcddde;padding:20px;}"
        ".msg{margin-bottom:20px;}"
        ".autor{font-weight:bold;color:#7289da;}"
        ".data{font-size:0.8em;color:#999;margin-left:5px;}"
        ".texto{margin:5px 0 0 45px;}"
        "img{max-width:500px;border-radius:8px;margin-top:5px;display:block;}"
        "</style></head><body>",
        f"<h2>Exportação de #{canal.name}</h2><hr>"
    ]

    # Expressão regular para detectar links de imagem
    regex_imagem = re.compile(r'(https?://\S+\.(?:png|jpg|jpeg|gif|webp))', re.IGNORECASE)

    for msg in mensagens:
        autor = msg.author.display_name
        data = msg.created_at.strftime("%d/%m/%Y %H:%M")
        conteudo = msg.content.replace("\n", "<br>")
        avatar = msg.author.display_avatar.url if msg.author.display_avatar else ""

        # Substitui links de imagem por <img>
        conteudo = regex_imagem.sub(r'<br><img src="\1">', conteudo)

        bloco = (
            f"<div class='msg'>"
            f"<img src='{avatar}' width='32' height='32' "
            f"style='vertical-align:middle;border-radius:50%;margin-right:8px;'>"
            f"<span class='autor'>{autor}</span>"
            f"<span class='data'>{data}</span>"
            f"<div class='texto'>{conteudo}</div>"
        )

        # Exibe anexos como imagens via link direto
        if msg.attachments:
            for anexo in msg.attachments:
                url = anexo.url
                tipo = anexo.content_type or ""
                if "image" in tipo or url.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                    bloco += f"<br><img src='{url}'>"
                else:
                    bloco += f"<br><a href='{url}'>{anexo.filename}</a>"

        bloco += "</div>"
        html.append(bloco)

    html.append("</body></html>")

    caminho_html = os.path.join(pasta_canal, f"{canal.name}.html")
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    return caminho_html, pasta_canal


# ==============================
# EVENTOS DO BOT
# ==============================
@client.event
async def on_ready():
    print(f"✅ Logado como {client.user}")
    print("Use !exportar #canal para exportar mensagens com mídias.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"{PREFIXO}exportar"):
        if not message.author.guild_permissions.administrator:
            await message.channel.send("🚫 Você precisa ser administrador para usar este comando.")
            return

        if not message.channel_mentions:
            await message.channel.send("❗ Mencione o canal: !exportar #geral")
            return

        canal = message.channel_mentions[0]
        await message.channel.send(f"⏳ Exportando tudo de {canal.mention} (isso pode demorar)...")

        # Executa a exportação
        caminho_html, pasta = await exportar_canal(canal)

        # Envia o arquivo exportado
        await message.channel.send(file=discord.File(caminho_html))

        # Cria um snippet bonito estilo Neverland
        nome_arquivo = os.path.basename(caminho_html)
        mensagem_final = (
            "```ansi\n"
            "\u001b[1;35m🕸️ NEVERLAND EXPORT SYSTEM\u001b[0m\n"
            "\u001b[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            f"\u001b[1;36m📡 Canal analisado:\u001b[0m {canal.mention}\n"
            f"\u001b[1;32m💾 Arquivo exportado:\u001b[0m {nome_arquivo}\n"
            "\u001b[1;33m🖼️ Imagens:\u001b[0m ✅ Incluídas\n"
            "\u001b[1;32m⚙️ Status:\u001b[0m Concluído com sucesso\n"
            "\u001b[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m\n"
            "\u001b[1;35m> Abra o arquivo .html no navegador para visualizar.\u001b[0m\n"
            "```"
        )

        await message.channel.send(mensagem_final)


# ==============================
# INICIALIZAÇÃO
# ==============================
client.run(TOKEN)
