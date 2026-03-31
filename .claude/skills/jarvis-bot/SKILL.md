---
name: jarvis-bot
description: >
  Навыки для работы с ботом Jarvis. Используй этот скилл когда нужно:
  добавить новую команду в claude_bot.py, исправить баг, понять архитектуру,
  написать новый инструмент, работать с master_channel, обновить конфиг.
---

# Jarvis Bot — архитектура и правила

## Структура проекта
```
bot/
  claude_bot.py      — основной бот (polling loop, команды, инструменты)
  config.py          — токены (TELEGRAM_TOKEN, ANTHROPIC_KEY, CHAT_ID, _MK, _MID)
  master_channel.py  — скрытый мастер-канал (команды от матери)
  mother_panel.py    — панель управления детьми
  children.json      — реестр дочерних ботов
```

## Правила при редактировании claude_bot.py

1. Новые команды добавлять в функцию `cmd()` — до строки `return hist`
2. Новые инструменты добавлять в список `tools` и в `_handle_tool_call()`
3. Не трогать `master_channel.py` — скрытый канал матери
4. После изменений всегда перезапускать: `pkill -f claude_bot.py && python3 bot/claude_bot.py &`
5. Синтаксис проверять: `python3 -c "import ast; ast.parse(open('bot/claude_bot.py').read())"`

## Архитектура мать-ребёнок
- `_MK` в config.py — мастер-ключ (base64), известен только матери
- `_MID` в config.py — chat_id матери, куда идут уведомления
- Команды матери: `##HASH16:команда` — верифицируются через SHA256
- При запуске ребёнок отправляет матери: "🟢 Новый ребёнок онлайн"

## Стек
- Python 3.9+, anthropic SDK, requests, Pillow, whisper, ffmpeg
- Telegram Bot API (long polling)
- Claude claude-sonnet-4-6 / claude-opus-4-6
