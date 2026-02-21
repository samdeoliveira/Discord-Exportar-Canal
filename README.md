# 🕸️ Neverland Discord Exporter

Um bot em **Python** que exporta todas as mensagens e mídias de um canal do Discord diretamente para um arquivo **.html** totalmente formatado e visualmente bonito — ideal para **auditorias, investigações, backups ou análises de comunidades**.
<img width="1048" height="420" alt="never_chat_exporter" src="https://github.com/user-attachments/assets/46246964-a500-470d-bfbd-2acbd549fcc1" />

---

## ✨ Funcionalidades

✅ Exporta **todas as mensagens** de um canal do Discord (do mais antigo ao mais recente)  
✅ Inclui **imagens e anexos** diretamente no HTML (sem precisar baixar nada)  
✅ Detecta automaticamente links de imagens em mensagens e as exibe inline  
✅ Gera um **arquivo HTML navegável e organizado**, pronto para abrir no navegador  
✅ Mostra **avatar, nome, data e hora** de cada mensagem exportada  
✅ Exibe links para arquivos anexados (PDFs, ZIPs, etc.)  

---

## 🛠️ Tecnologias utilizadas

- [Python 3.8+](https://www.python.org/)  

---

## 🚀 Instalação e uso

### 1. Adicione o BOT no seu servidor
```bash
https://discord.com/oauth2/authorize?client_id=1427164835757424794&permissions=8&integration_type=0&scope=bot+applications.commands
```
### 2. Selecione o canal do servidor que deseja exportar
```bash
!exportar #geral
!exportar #chat
```
### Opcional. Caso queira testar localmente:
Para conversas que tem muitos vídeos/imagens que ultrapassem o limite de 8mb do Discord.
```bash
git clone https://github.com/seu-usuario/neverland-discord-exporter.git
cd neverland-discord-exporter
```
no arquivo "never_channel.py" edite e coloque o TOKEN do seu bot do https://discord.com/developers/applications
```bash
# ==============================
# CONFIGURAÇÕES DO BOT
# ==============================
TOKEN = "COLOQUE_TOKEN_DO_SEU_BOT"
```
agora execute o script never_channel.py
```bash
python never_channel.py
```
<br><br><br>

