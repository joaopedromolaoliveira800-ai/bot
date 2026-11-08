import os
import threading
import requests
from flask import Flask
import discord
from discord.ext import commands
from banner_generator import gerar_banner_profissional

# -------------------------------------------------------------
# CONFIGURAÇÃO DO SERVIDOR WEB (FLASK) PARA MANTER A RENDER ATIVA
# -------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Bot de Promoções VIP (Discord + WhatsApp) está ativo e operando!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# -------------------------------------------------------------
# CONFIGURAÇÃO DO BOT DISCORD E VARIÁVEIS GLOBAIS
# -------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configurações da API do WhatsApp (Evolution API)
EVOLUTION_URL = os.environ.get("EVOLUTION_URL", "https://sua-instancia-evolution.com")
EVOLUTION_API_KEY = os.environ.get("EVOLUTION_API_KEY", "sua_chave_api")
INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "bot_promo")

headers_api = {
    "apikey": EVOLUTION_API_KEY,
    "Content-Type": "application/json"
}

# Estado da Promoção Editável
promocao = {
    "titulo": "🔥 SMARTPHONE PREMIUM COM 40% OFF",
    "descricao": "Garanta a melhor tecnologia com preço imbatível e frete grátis para todo o Brasil!",
    "link": "https://sualoja.com/promocao-especial",
    "preco_antigo": "R$ 2.999,00",
    "preco_novo": "R$ 1.799,00"
}

@bot.event
async def on_ready():
    print(f"✅ Bot conectado com sucesso como: {bot.user}")
    print("📌 Servidor Flask pronto para pings de sustentação na Render.")

# -------------------------------------------------------------
# COMANDOS DE GERENCIAMENTO E EDIÇÃO DE PROMOÇÕES (DISCORD)
# -------------------------------------------------------------
@bot.command(name="setpromo")
async def setpromo(ctx, *, conteudo: str):
    """Define o título e a descrição separados por '|'. Ex: !setpromo Título | Descrição"""
    global promocao
    if "|" in conteudo:
        t, d = conteudo.split("|", 1)
        promocao["titulo"] = t.strip()
        promocao["descricao"] = d.strip()
        await ctx.send(f"✅ **Título e Descrição atualizados!**\n📌 **Título:** {promocao['titulo']}\n📝 **Descrição:** {promocao['descricao']}")
    else:
        await ctx.send("⚠️ Use o separador `|`. Exemplo: `!setpromo Título da Oferta | Descrição da Oferta`")

@bot.command(name="setlink")
async def setlink(ctx, link: str):
    """Atualiza o link de destino da promoção."""
    global promocao
    promocao["link"] = link.strip()
    await ctx.send(f"✅ **Link atualizado:** {promocao['link']}")

@bot.command(name="setpreco")
async def setpreco(ctx, *, precos: str):
    """Define os preços antigo e novo. Ex: !setpreco R$ 199,90 | R$ 99,90"""
    global promocao
    if "|" in precos:
        pa, pn = precos.split("|", 1)
        promocao["preco_antigo"] = pa.strip()
        promocao["preco_novo"] = pn.strip()
        await ctx.send(f"✅ **Preços Atualizados!**\n❌ De: {promocao['preco_antigo']} ➔ ✅ Por: {promocao['preco_novo']}")
    else:
        promocao["preco_novo"] = precos.strip()
        await ctx.send(f"✅ **Preço Novo Atualizado:** {promocao['preco_novo']}")

@bot.command(name="verpromo")
async def verpromo(ctx):
    """Exibe uma prévia estilizada no Discord com os dados atuais."""
    embed = discord.Embed(
        title=promocao["titulo"],
        description=promocao["descricao"],
        color=0x38bdf8
    )
    embed.add_field(name="💰 Preço Antigo", value=promocao["preco_antigo"] or "N/A", inline=True)
    embed.add_field(name="🔥 Preço Promo", value=promocao["preco_novo"] or "N/A", inline=True)
    embed.add_field(name="🔗 Link de Afiliado", value=promocao["link"], inline=False)
    embed.set_footer(text="Use !gerarimagem para criar o banner visual ou !disparar_wa para enviar ao WhatsApp.")
    await ctx.send(embed=embed)

@bot.command(name="gerarimagem")
async def gerarimagem(ctx):
    """Gera um banner visual caprichado usando o Pillow e envia no Discord."""
    img_bytes = gerar_banner_profissional(
        titulo=promocao["titulo"],
        descricao=promocao["descricao"],
        preco_antigo=promocao["preco_antigo"],
        preco_novo=promocao["preco_novo"]
    )
    file = discord.File(fp=img_bytes, filename="banner_promo.png")
    await ctx.send("🎨 **Banner Profissional Gerado com Sucesso!**", file=file)

# -------------------------------------------------------------
# COMANDOS DE CONEXÃO E DISPARO DO WHATSAPP (EVOLUTION API)
# -------------------------------------------------------------
@bot.command(name="conectar_codigo")
async def conectar_codigo(ctx, numero_telefone: str):
    """Gera o código de pareamento de 8 dígitos para o número informado (ex: 5511999999999)."""
    url = f"{EVOLUTION_URL}/instance/connect/{INSTANCE_NAME}"
    payload = {"number": numero_telefone}
    
    try:
        res = requests.post(url, json=payload, headers=headers_api, timeout=10)
        dados = res.json()
        codigo = dados.get("pairingCode")
        
        if codigo:
            await ctx.send(
                f"🔢 **Código de Pareamento WhatsApp:** `{codigo}`\n\n"
                f"📲 Abra seu WhatsApp ➔ **Aparelhos Conectados** ➔ **Conectar com número de telefone** e digite o código acima."
            )
        else:
            await ctx.send(f"⚠️ Resposta da API: {dados}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao conectar com a Evolution API: {e}")

@bot.command(name="conectar_qr")
async def conectar_qr(ctx):
    """Obtém as informações de conexão via QR Code."""
    url = f"{EVOLUTION_URL}/instance/connect/{INSTANCE_NAME}"
    try:
        res = requests.get(url, headers=headers_api, timeout=10)
        dados = res.json()
        await ctx.send(f"📱 **Status da Conexão:**\n```{dados}```")
    except Exception as e:
        await ctx.send(f"❌ Erro ao solicitar QR Code: {e}")

@bot.command(name="disparar_wa")
async def disparar_wa(ctx, destino: str):
    """Envia a mensagem da promoção para um número ou ID de grupo (ex: 5511999999999)."""
    url = f"{EVOLUTION_URL}/message/sendText/{INSTANCE_NAME}"
    
    texto_formatado = (
        f"*{promocao['titulo']}*\n\n"
        f"{promocao['descricao']}\n\n"
        f"❌ ~De: {promocao['preco_antigo']}~\n"
        f"✅ *Por apenas: {promocao['preco_novo']}*\n\n"
        f"🛒 *Garanta o seu aqui:* {promocao['link']}"
    )
    
    payload = {
        "number": destino,
        "text": texto_formatado
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers_api, timeout=10)
        if res.status_code in [200, 201]:
            await ctx.send(f"🚀 **Promoção disparada com sucesso para WhatsApp:** `{destino}`!")
        else:
            await ctx.send(f"❌ Falha no disparo: {res.text}")
    except Exception as e:
        await ctx.send(f"❌ Erro de conexão com a API do WhatsApp: {e}")

# -------------------------------------------------------------
# INICIALIZAÇÃO DA APLICAÇÃO
# -------------------------------------------------------------
if __name__ == "__main__":
    # Inicia o servidor web Flask em uma thread separada para a Render
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # Inicia o bot do Discord
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("⚠️ ALERTA: 'DISCORD_TOKEN' não foi encontrado nas variáveis de ambiente.")
