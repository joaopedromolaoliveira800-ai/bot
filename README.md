# 🚀 Bot de Promoções VIP com Painel Admin completo (Discord + WhatsApp)

Este é um bot completo, moderno e caprichado para Discord com controle de vendas, estoque, chave PIX, minigame do Dinossauro e envio para WhatsApp.

---

## 🔐 Controle de Acesso (Cargo de Admin)
Para usar qualquer comando de administração ou o minigame, o usuário precisa ter o cargo definido como `Admin` no servidor do Discord.

---

## 🎨 Recursos do Sistema
- 🛡️ **Verificação de Cargo Admin:** Proteção em todos os comandos administrativos.
- 📦 **Gestão de Produtos e Estoque:** Adicione produtos, estoque e valores de vendas.
- 🔗 **Links de Afiliados:** Altere e gerencie links de afiliados por produto.
- 🖼️ **Gerador de Imagens & Textos:** Criação de banners HD automáticos e copys de vendas.
- 📊 **Relatório Diário de Vendas & PIX:** Acompanhe o faturamento do dia, chave PIX e lista de clientes que pagaram via PIX.
- 🦖 **Jogo do Dinossauro (Mini-game no Discord):** Jogo interativo no chat com botões para pular e esquivar dos cactos!

---

## 💻 Lista de Comandos para Admins

### 📦 Gestão de Produtos, Estoque e PIX
- `!addproduto <nome> | <preco_antigo> | <preco_novo> | <estoque> | <link>` - Adiciona ou atualiza um produto no estoque.
- `!addestoque <nome_produto> <quantidade>` - Adiciona unidades ao estoque existente.
- `!setlink <nome_produto> <novo_link>` - Altera o link de afiliado do produto.
- `!setpix <chave_pix>` - Define a chave PIX configurada para receber pagamentos.
- `!registrarpix <nome_cliente> | <valor> | <produto>` - Registra um pagamento PIX efetuado por um cliente.
- `!relatorio` - Exibe o total faturado no dia, chave PIX atual e lista de clientes que pagaram.

### 🎨 Geração de Conteúdo
- `!gerartermo <nome_produto>` - Gera a cópia/texto formatado da promoção pronto para divulgar.
- `!gerarimagem <nome_produto>` - Gera o banner visual em alta qualidade para o produto.

### 🦖 Mini-game
- `!dino` - Inicia o Jogo do Dinossauro interativo diretamente no Discord!
