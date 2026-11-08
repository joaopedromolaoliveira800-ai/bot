from PIL import Image, ImageDraw, ImageFont
import io

def gerar_banner_produto(titulo, preco_antigo="", preco_novo="", tag="OFERTA VIP"):
    """Gera um banner visual elegante (1200x630 pixels) para o produto."""
    largura, altura = 1200, 630
    base = Image.new("RGB", (largura, altura))
    draw = ImageDraw.Draw(base)
    
    # Gradiente escuro de fundo
    for y in range(altura):
        r = int(15 + (y / altura) * (30 - 15))
        g = int(23 + (y / altura) * (41 - 23))
        b = int(42 + (y / altura) * (59 - 42))
        draw.line([(0, y), (largura, y)], fill=(r, g, b))
    
    try:
        fonte_tag = ImageFont.truetype("arial.ttf", 24)
        fonte_titulo = ImageFont.truetype("arial.ttf", 50)
        fonte_preco_antigo = ImageFont.truetype("arial.ttf", 32)
        fonte_preco_novo = ImageFont.truetype("arial.ttf", 58)
    except IOError:
        fonte_tag = ImageFont.load_default()
        fonte_titulo = ImageFont.load_default()
        fonte_preco_antigo = ImageFont.load_default()
        fonte_preco_novo = ImageFont.load_default()

    # Borda neon
    draw.rounded_rectangle([(40, 40), (1160, 590)], radius=20, outline=(56, 189, 248), width=3)
    
    # Tag no topo
    draw.rounded_rectangle([(70, 70), (320, 115)], radius=10, fill=(236, 72, 153))
    draw.text((85, 80), tag.upper(), fill=(255, 255, 255), font=fonte_tag)
    
    # Título do produto
    draw.text((70, 150), titulo[:45], fill=(255, 255, 255), font=fonte_titulo)
    
    # Preços
    y_preco = 300
    if preco_antigo:
        text_antigo = f"De: {preco_antigo}"
        draw.text((70, y_preco), text_antigo, fill=(239, 68, 68), font=fonte_preco_antigo)
        bbox = draw.textbbox((70, y_preco), text_antigo, font=fonte_preco_antigo)
        draw.line([(bbox[0], bbox[1] + 18), (bbox[2], bbox[1] + 18)], fill=(239, 68, 68), width=3)
        y_preco += 60

    if preco_novo:
        draw.text((70, y_preco), f"Por: {preco_novo}", fill=(34, 197, 94), font=fonte_preco_novo)

    draw.text((820, 530), "⚡ Gerado pelo Bot Admin", fill=(100, 116, 139), font=fonte_tag)

    img_byte_arr = io.BytesIO()
    base.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr
