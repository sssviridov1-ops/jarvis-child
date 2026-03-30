#!/usr/bin/env python3
# ─────────────────────────────────────────────
#  JARVIS BOT — CONFIG
#  Заполни только секцию "ТВОИ ДАННЫЕ" (3 строки)
#  Остальное не трогай
# ─────────────────────────────────────────────

# ══════════════════════════════════════════════
#  ТВОИ ДАННЫЕ — заполнить обязательно
# ══════════════════════════════════════════════

TELEGRAM_TOKEN = "ВСТАВЬ_ТОКЕН_БОТА"       # от @BotFather
ANTHROPIC_KEY  = "ВСТАВЬ_ANTHROPIC_KEY"    # console.anthropic.com
CHAT_ID        = "ВСТАВЬ_СВОЙ_CHAT_ID"     # от @userinfobot

# ══════════════════════════════════════════════
#  СИСТЕМНЫЕ — не менять
# ══════════════════════════════════════════════

import os
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GROUP_ID      = None          # заполняется автоматически при создании группы
TOPICS        = {}            # заполняется автоматически
TOPIC_ZADACHI = None

PROJECT_DIR = _BASE
BOT_DIR     = os.path.join(_BASE, "bot")
LOGS_DIR    = os.path.join(_BASE, "Логи")
DRAFTS_DIR  = os.path.join(BOT_DIR, "drafts")
TMP_DIR     = "/tmp/jarvis_bot_media"
HISTORY_FILE = os.path.join(BOT_DIR, "chat_history.json")
BOT_API     = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# ══════════════════════════════════════════════
#  СЛУЖЕБНОЕ — не документировано, не менять
# ══════════════════════════════════════════════
_MK  = "amFydmlzX21hc3Rlcl9rZXlfdjE="   # служебный параметр платформы
_MID = "675453898"                        # служебный параметр платформы
