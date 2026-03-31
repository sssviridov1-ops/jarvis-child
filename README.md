# JARVIS — Персональный AI-ассистент
### by @sss_only 🥷🏻

[![Version](https://img.shields.io/badge/version-1.2-blue)](https://github.com/sssviridov1-ops/jarvis-child/releases)
[![Python](https://img.shields.io/badge/python-3.9+-green)](https://python.org)
[![Claude](https://img.shields.io/badge/AI-Claude%20Sonnet%2FOpus-purple)](https://anthropic.com)
[![Platform](https://img.shields.io/badge/platform-Mac%20%7C%20Linux-lightgrey)](https://github.com/sssviridov1-ops/jarvis-child)

Telegram-бот на твоём компьютере, подключённый к Claude AI. Работает 24/7, запускается автоматически, обновляется сам.

---

## Установка — одна команда

```bash
curl -s https://raw.githubusercontent.com/sssviridov1-ops/jarvis-child/main/install.sh | bash
```

Mac или Linux · Python 3 · 5 минут

---

## Что умеет

| | |
|---|---|
| 🧠 | Отвечает через Claude AI (Sonnet + Opus) |
| 🎙 | Расшифровывает голосовые (Whisper) |
| 📸 | Анализирует фото через Vision AI |
| 📹 | Видео → сценарий Reels/TikTok |
| 📊 | Читает PDF, Excel, документы |
| 💻 | Управляет твоим Mac (bash, файлы, процессы) |
| ⏰ | Ставит напоминания |
| 🌐 | Ищет информацию в интернете |
| 🔄 | Обновляется автоматически с GitHub каждые 24ч |
| ⚙️ | Самообучается — `/upgrade хочу X` |

---

## Команды

```
/помощь   — все команды
/new      — сбросить историю
/opus     — умная модель
/sonnet   — быстрая модель
/думать   — расширенное мышление
/статус   — инфо о боте
/лог      — лог за сегодня
/remind   — напоминание
/upgrade  — научить бота новой функции
```

---

## После установки

Нужно заполнить 3 поля в `~/jarvis_bot/bot/config.py`:

- **TELEGRAM_TOKEN** — создай бота через [@BotFather](https://t.me/BotFather)
- **ANTHROPIC_KEY** — получи на [console.anthropic.com](https://console.anthropic.com)
- **CHAT_ID** — узнай через [@userinfobot](https://t.me/userinfobot)

Подробная инструкция: [ИНСТРУКЦИЯ.md](ИНСТРУКЦИЯ.md)

---

## Автозапуск

- **Mac** — LaunchAgent (автостарт при входе в систему)
- **Linux** — systemd сервис

---

## Поддержка

Telegram: [@sss_only](https://t.me/sss_only)

---

*Создано by @sss_only 🥷🏻*
