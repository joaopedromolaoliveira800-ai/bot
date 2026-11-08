from PIL import Image, ImageDraw, ImageFont
import io

def gerar_banner_profissional(titulo, descricao, preco_antigo="", preco_novo="", tag="OFERTA IMPERDÍVEL"):
    """
    Gera um banner visual extremamente moderno e elegante (1200x630 pixels)
    com gradientes suaves, bordas estilizadas e tipografia destacada.
    """
    largura, altura = 1200, 630
    
    # Criar fundo com gradiente escuro premium (Deep Slate to Navy)
    base = Image.new("RGB", (largura, altura))
    draw = ImageDraw.Draw(base)
    
    for y in range(altura):
        # Interpolação de cor para gradiente vertical
        r = int(15 + (y / altura) * (30 - 15))
        g = int(23 + (y / altura) * (41 - 23))
        b = int(42 + (y / altura) * (59 - 42))
        draw.line([(0, y), (largura, y)], fill=(r, g, b))
    
    # Carregar fontes padrão com fallback seguro
    try:
        fonte_tag = ImageFont.truetype("arial.ttf", 24)
        fonte_titulo = ImageFont.truetype("arial.ttf", 52)
        fonte_desc = ImageFont.truetype("arial.ttf", 30)
        fonte_preco_antigo = ImageFont.truetype("arial.ttf", 32)
        fonte_preco_novo = ImageFont.truetype("arial.ttf", 58)
    except IOError:
        fonte_tag = ImageFont.load_default()
        fonte_titulo = ImageFont.load_default()
        fonte_desc = ImageFont.load_default()
        fonte_preco_antigo = ImageFont.load_default()
        fonte_preco_novo = ImageFont.load_default()

    # Desenhar moldura interna elegante com borda neon suave
    draw.rounded_rectangle([(40, 40), (1160, 590)], radius=20, outline=(56, 189, 248), width=3)
    
    # Badge / Tag de Destaque no topo
    draw.rounded_rectangle([(70, 70), (340, 115)], radius=10, fill=(236, 72, 153))
    draw.text((85, 80), tag.upper(), fill=(255, 255, 255), font=fonte_tag)
    
    # Título Principal
    draw.text((70, 145), titulo[:40], fill=(255, 255, 255), font=fonte_titulo)
    
    # Descrição / Subtítulo
    draw.text((70, 230), descricao[:75], fill=(148, 163, 184), font=fonte_desc)
    
    # Área de Preços (Se fornecidos)
    y_preco = 360
    if preco_antigo:
        text_antigo = f"De: {preco_antigo}"
        draw.text((70, y_preco), text_antigo, fill=(239, 68, 68), font=fonte_preco_antigo)
        # Riscado no preço antigo
        bbox = draw.textbbox((70, y_preco), text_antigo, font=fonte_preco_antigo)
        draw.line([(bbox[0], bbox[1] + 18), (bbox[2], bbox[1] + 18)], fill=(239, 68, 68), width=3)
        y_preco += 50

    if preco_novo:
        draw.text((70, y_preco), f"Por: {preco_novo}", fill=(34, 197, 94), font=fonte_preco_novo)

    # Selo visual de Rodapé
    draw.text((850, 530), "⚡ Gerado via Discord Bot", fill=(100, 116, 139), font=fonte_tag)

    # Retornar imagem como BytesIO para envio direto no Discord/WhatsApp sem precisar salvar em disco
    img_byte_arr = io.BytesIO()
    base.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr
