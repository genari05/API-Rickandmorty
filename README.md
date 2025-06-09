# 📊 Projeto de Coleta e Processamento de Dados - Rick and Morty API

Este projeto tem como objetivo integrar uma API pública com um sistema automatizado de coleta, processamento, armazenamento e envio de relatórios por e-mail. A API escolhida foi a [Rick and Morty API](https://rickandmortyapi.com/), que fornece dados ricos e diversos sobre personagens, episódios e localizações do universo da série.

## 🔍 Descrição

O sistema realiza as seguintes etapas:

1. **Coleta Manual de IDs**  
   O usuário informa os IDs de personagens, episódios e localizações desejados.

2. **Requisição à API**  
   São feitas requisições HTTP para buscar os dados diretamente da API Rick and Morty.

3. **Armazenamento em Banco de Dados**  
   Os dados são armazenados localmente utilizando SQLite, com tabelas específicas para personagens, episódios, localizações e dados processados.

4. **Processamento de Dados**  
   Validação e transformação de campos como:
   - Nome válido com regex
   - Espécie convertida para letras maiúsculas
   - Verificação de HTTPS em imagens

5. **Geração de Relatório**  
   Um relatório resumo em texto é criado, contendo estatísticas e exemplos dos dados coletados.

6. **Envio de E-mail Automático**  
   O sistema envia um e-mail com:
   - O resumo do relatório no corpo da mensagem
   - Um relatório final completo em PDF como anexo

---

## 🧰 Tecnologias Utilizadas

- **Python 3**
- **SQLite** (via `sqlite3`)
- **Requests** (para integração com a API)
- **Regex** (`re`) para validação de dados
- **FPDF** (para gerar o PDF)
- **smtplib** e **email** (para envio de e-mails)

---

