# Telegram Ollama Bot

AI bot Telegram powered by Ollama (llama2-uncensored:7b).

## Setup Lokal (Docker)

### Requirement
- Docker + Docker Compose
- Token Telegram (dari @BotFather)

### Langkah

1. **Clone repo:**
```bash
git clone https://github.com/EarlPhantom2-dev/telegram-ollama-bot.git
cd telegram-ollama-bot
```

2. **Setup env:**
```bash
cp .env.example .env
# Edit .env, masukkan TELEGRAM_TOKEN yang valid
```

3. **Jalankan Docker:**
```bash
docker-compose up -d
```

4. **Pull model Ollama** (first run, ~5-15 menit tergantung koneksi):
```bash
docker exec ollama-container ollama pull llama2-uncensored:7b
```

5. **Test bot di Telegram:**
   - Cari bot di Telegram
   - Kirim `/start`
   - Kirim pesan, tunggu respons

### Stop
```bash
docker-compose down
```

## VPS Deployment

1. SSH ke VPS
2. Clone repo
3. Setup .env (dengan token yang **baru**, jangan yang terekspos)
4. `docker-compose up -d`
5. Wait untuk model auto-pull

## Resources

- **7B model:** 8–12 GB RAM
- **CPU:** 2+ cores recommended
- **Storage:** 20 GB+ untuk model + cache

## Troubleshooting

**Bot tidak respond:**
- Cek token Telegram di `.env`
- Jalankan `docker logs telegram-bot`
- Pastikan model sudah pull: `docker exec ollama-container ollama list`

**Ollama error:**
- Cek RAM tersedia: `docker stats ollama-container`
- Cek storage: `docker exec ollama-container df -h`

## Security

⚠️ **Jangan share `.env` file!** Token Telegram sudah terekspos di commit history — **regenerate token baru** di @BotFather setelah deploy.
