# 🎲 Random Bot Lite

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)

A Telegram bot for discovering random channels in the depths of Telegram. Helps you explore new communities and content.

**🤖 He's already waiting for you:** [@synctgrand_bot](https://t.me/synctgrand_bot)

## ✨ Features

- **Random channels** - get suggestions for interesting Telegram channels
- **Asynchronous processing** - built on aiogram 3.x for high performance
- **Simple interface** - clear commands and quick responses

## 🎮 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and bot description |
| `/help` | List of available commands |
| `/random` | Get a random channel suggestion |
| `/info` | Bot statistics and information (**in development**) | 

## 🛠 Tech Stack

**Core:**
- Python 3.10+
- aiogram 3.x 
- Postgresql 

**DevOps:**
- Docker
- Prometheus + Grafana for monitoring
- Loki for logging

## 📦 Docker

```bash
# Build and run
# Don't forget about .env
docker compose up -d --build
```

## 🤝 Contributing

All improvements are welcome! You can:

- Report bugs via [Issues](https://github.com/Andy666Fox/random_bot_lite/issues)
- Suggest new features
- Submit Pull Requests

### Development

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Submit a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details
---

⭐ Star this repo if you found it helpful!
