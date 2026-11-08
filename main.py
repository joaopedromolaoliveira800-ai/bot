import os
import random
import datetime
import threading
from flask import Flask
import discord
from discord.ext import commands
from discord.ui import Button, View
from banner_generator import gerar_banner_produto

# -------------------------------------------------------------
# FLASK PARA RENDER
# -------------------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Bot Admin & Estoque & Dino Ativo!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# -------------------------------------------------------------
# BOT DISCORD COM VERIFICAÇÃO DE CARGO ADMIN
# -------------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Banco de dados em memória
produtos = {}
chave_pix = "Chave PIX não configurada"
vendas_dia = []  # Lista de dicts: {"cliente": str, "valor": float, "produto": str, "data": str}

def eh_admin():
    """Decorator para verificar se o usuário tem o cargo 'Admin'."""
    async def predicate(ctx):
        cargo = discord.utils.get(ctx.author.roles, name="Admin")
        if cargo is None:
            await ctx.send("❌ **Acesso Negado!** Apenas usuários com o cargo **Admin** podem usar este comando.")
            return False
        return True
    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f"✅ Bot Admin conectado como {bot.user}")

# -------------------------------------------------------------
# COMANDOS DE ADMINISTRAÇÃO (ESTOQUE, PRODUTO, LINK, PIX)
# -------------------------------------------------------------
@bot.command(name="addproduto")
@eh_admin()
async def addproduto(ctx, *, dados: str):
    """Uso: !addproduto Nome | Preço Antigo | Preço Novo | Estoque | Link Afiliado"""
    try:
        partes = [p.strip() for p in dados.split("|")]
        nome, preco_ant, preco_novo, qtd, link = partes[0], partes[1], partes[2], int(partes[3]), partes[4]
        produtos[nome.lower()] = {
            "nome": nome,
            "preco_antigo": preco_ant,
            "preco_novo": preco_novo,
            "estoque": qtd,
            "link": link
        }
        await ctx.send(f"✅ **Produto '{nome}' cadastrado com sucesso!**\n📦 Estoque: {qtd} un | 🔗 Link: {link}")
    except Exception:
        await ctx.send("⚠️ Formato incorreto! Use: `!addproduto Nome | Preço Antigo | Preço Novo | Estoque | Link`")

@bot.command(name="addestoque")
@eh_admin()
async def addestoque(ctx, nome_produto: str, quantidade: int):
    """Adiciona unidades ao estoque de um produto."""
    prod_key = nome_produto.lower()
    if prod_key in produtos:
        produtos[prod_key]["estoque"] += quantidade
        await ctx.send(f"📦 **Estoque atualizado!** Produto '{produtos[prod_key]['nome']}' agora possui **{produtos[prod_key]['estoque']}** unidades.")
    else:
        await ctx.send(f"❌ Produto '{nome_produto}' não encontrado no estoque.")

@bot.command(name="setlink")
@eh_admin()
async def setlink(ctx, nome_produto: str, novo_link: str):
    """Altera o link de afiliado de um produto."""
    prod_key = nome_produto.lower()
    if prod_key in produtos:
        produtos[prod_key]["link"] = novo_link
        await ctx.send(f"🔗 **Link de Afiliado atualizado!** Produto '{produtos[prod_key]['nome']}' ➔ {novo_link}")
    else:
        await ctx.send(f"❌ Produto '{nome_produto}' não encontrado.")

@bot.command(name="setpix")
@eh_admin()
async def setpix(ctx, *, nova_chave: str):
    """Define a chave PIX atual."""
    global chave_pix
    chave_pix = nova_chave.strip()
    await ctx.send(f"🔑 **Chave PIX atualizada para:** `{chave_pix}`")

@bot.command(name="registrarpix")
@eh_admin()
async def registrarpix(ctx, *, dados: str):
    """Uso: !registrarpix Nome Cliente | Valor | Produto"""
    try:
        cliente, valor, prod = [p.strip() for p in dados.split("|")]
        vendas_dia.append({
            "cliente": cliente,
            "valor": float(valor.replace("R$", "").replace(",", ".").strip()),
            "produto": prod,
            "horario": datetime.datetime.now().strftime("%H:%M")
        })
        await ctx.send(f"💸 **Pagamento PIX registrado!** Cliente: `{cliente}` | Valor: `R$ {valor}`")
    except Exception:
        await ctx.send("⚠️ Formato incorreto! Use: `!registrarpix Nome Cliente | Valor | Nome Produto`")

@bot.command(name="relatorio")
@eh_admin()
async def relatorio(ctx):
    """Relatório diário de faturamento, chave PIX e clientes que pagaram."""
    total_hoje = sum(v["valor"] for v in vendas_dia)
    embed = discord.Embed(title="📊 Relatório Diário de Vendas & PIX", color=0x34d399)
    embed.add_field(name="🔑 Chave PIX Atual", value=f"`{chave_pix}`", inline=False)
    embed.add_field(name="💰 Total Faturado Hoje", value=f"**R$ {total_hoje:.2f}**", inline=False)
    
    if vendas_dia:
        lista_clientes = "\n".join([f"• **{v['cliente']}** - R$ {v['valor']:.2f} ({v['produto']}) às {v['horario']}" for v in vendas_dia])
        embed.add_field(name="👥 Clientes que fizeram PIX hoje", value=lista_clientes, inline=False)
    else:
        embed.add_field(name="👥 Clientes que fizeram PIX hoje", value="Nenhum pagamento registrado hoje ainda.", inline=False)
        
    await ctx.send(embed=embed)

# -------------------------------------------------------------
# GERAÇÃO DE IMAGEM E TEXTO
# -------------------------------------------------------------
@bot.command(name="gerartermo")
@eh_admin()
async def gerartermo(ctx, *, nome_produto: str):
    """Gera o texto copys de divulgação do produto."""
    prod_key = nome_produto.lower()
    if prod_key in produtos:
        p = produtos[prod_key]
        texto = (
            f"🔥 **SUPER OFERTA: {p['nome'].upper()}** 🔥\n\n"
            f"❌ De: ~{p['preco_antigo']}~\n"
            f"✅ **Por Apenas: {p['preco_novo']}**\n"
            f"📦 Restam apenas **{p['estoque']} unidades** em estoque!\n\n"
            f"🛒 **Compre pelo Link de Afiliado:** {p['link']}\n"
            f"💳 **Pagamentos via PIX:** `{chave_pix}`"
        )
        await ctx.send(f"📝 **Texto Gerado para o Produto:**\n\n{texto}")
    else:
        await ctx.send(f"❌ Produto '{nome_produto}' não encontrado. Cadastre com `!addproduto`.")

@bot.command(name="gerarimagem")
@eh_admin()
async def gerarimagem(ctx, *, nome_produto: str):
    """Gera o banner em imagem do produto."""
    prod_key = nome_produto.lower()
    if prod_key in produtos:
        p = produtos[prod_key]
        img_bytes = gerar_banner_produto(
            titulo=p['nome'],
            preco_antigo=p['preco_antigo'],
            preco_novo=p['preco_novo']
        )
        file = discord.File(fp=img_bytes, filename=f"promo_{prod_key}.png")
        await ctx.send("🖼️ **Banner Gerado com Sucesso!**", file=file)
    else:
        await ctx.send(f"❌ Produto '{nome_produto}' não encontrado.")

# -------------------------------------------------------------
# JOGUINHO DO DINOSSAURO PARA O ADMIN 🦖
# -------------------------------------------------------------
class DinoGameView(View):
    def __init__(self, author):
        super().__init__(timeout=60)
        self.author = author
        self.score = 0
        self.game_over = False

    def render_game(self):
        if self.game_over:
            return f"🦖💥 **GAME OVER!**\nCacto atingido! PONTUAÇÃO FINAL: **{self.score} pontos**."
        
        trilhos = ["⬛"] * 8
        pos_dino = 1
        pos_cacto = 7 - (self.score % 6)
        
        if pos_dino == pos_cacto:
            self.game_over = True
            return f"🦖💥 **GAME OVER!**\nO Dino bateu no cacto 🌵! Pontuação: **{self.score}**"
            
        trilhos[pos_dino] = "🦖"
        trilhos[pos_cacto] = "🌵"
        
        return f"🎮 **Jogo do Dinossauro Admin**\nPontuação: **{self.score}**\n\n" + "".join(trilhos)

    @discord.ui.button(label="🦘 Pular / Avançar", style=discord.ButtonStyle.green)
    async def pular(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.author:
            await interaction.response.send_message("Apenas o Admin que iniciou o jogo pode jogar!", ephemeral=True)
            return
        
        self.score += 1
        msg = self.render_game()
        if self.game_over:
            for item in self.children:
                item.disabled = True
        await interaction.response.edit_message(content=msg, view=self)

@bot.command(name="dino")
@eh_admin()
async def dino(ctx):
    """Inicia o minigame do Dinossauro exclusivo para Admins!"""
    view = DinoGameView(ctx.author)
    await ctx.send(view.render_game(), view=view)

# -------------------------------------------------------------
# INICIALIZAÇÃO
# -------------------------------------------------------------
if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
    
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("⚠️ TOKEN do Discord não configurado!")
