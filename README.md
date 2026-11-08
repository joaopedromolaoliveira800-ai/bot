# 🚀 Bot Supremo de Promoções (Discord + WhatsApp)

Este é um bot completo, moderno e muito caprichado construído em Python. Ele roda no Discord como centro de controle e se conecta ao WhatsApp via **Evolution API**, permitindo criar promoções, gerar banners profissionais automaticamente com Pillow e disparar tudo com um único comando.

---

## 🎨 Recursos Incríveis
- 🤖 **Interface de Controle via Discord:** Altere títulos, descrições e links de afiliados com comandos simples.
- 🖼️ **Gerador de Banners HD:** Criação automática de imagens elegantes (1200x630) com gradientes modernos, bordas suaves, preços destacados e tags promocionais.
- 📱 **Conexão WhatsApp Simplificada:** Suporte a Código de Pareamento de 8 dígitos ou QR Code via Evolution API.
- ⚡ **Pronto para a Render:** Já possui servidor Flask interno integrado com Gunicorn para manter a hospedagem ativa 24/7.

---

## 📁 Estrutura do Projeto
```text
bot_promocoes_vip/
├── main.py              # Script principal com Discord, Flask e integração WhatsApp
├── banner_generator.py # Módulo de geração visual caprichada de imagens (Pillow)
├── requirements.txt     # Dependências do projeto
├── Procfile             # Configuração de inicialização para a Render
└── README.md            # Documentação e instruções de uso
```

---

## ⚙️ Como Hospedar na Render (Passo a Passo)

1. Suba este projeto para um repositório no **GitHub**.
2. Acesse o painel da **[Render](https://render.com/)**, crie um **New Web Service** e conecte seu repositório.
3. Configure as variáveis de ambiente em **Environment Variables**:
   - `MTU2NjI0MjAxNzgzNzU4MDI4OA.GKCdzn.khYbfHhwmhbCJs8ikjrEhLkCPfp9RYJiiihdos`: Token do seu bot obtido no Discord Developer Portal.
   - `https://evolution-api-production-d8bd.up.railway.app`: URL da sua instância da Evolution API.
   - `bf7e486d221a66dc442f610f29d9fec6a3dc760b8eb35bf7ef4a01d8dc98210a`: Sua chave de API da Evolution.
   - `botjp`: Nome da sua instância (ex: `bot_promo`).
4. Selecione `Python 3` como ambiente e confirme o deploy!

---

## 💻 Comandos no Discord

- `!setpromo <Título> | <Descrição>` - Define o título e a descrição da oferta.
- `!setlink <URL>` - Define o link de afiliado.
- `!setpreco <Preço Antigo> | <Preço Novo>` - Define os valores promocionais.
- `!verpromo` - Exibe uma prévia elegante da promoção atual no Discord.
- `!gerarimagem` - Gera e envia o banner visual caprichado no canal.
- `!conectar_codigo <Número>` - Solicita o código de pareamento do WhatsApp (ex: `!conectar_codigo 5511999999999`).
- `!conectar_qr` - Exibe as informações do QR Code de conexão.
- `!disparar_wa <Destino>` - Envia o texto da promoção para o WhatsApp.
- `!disparar_wa_midia <Destino>` - Envia a **imagem + legenda formatada** para o WhatsApp.
