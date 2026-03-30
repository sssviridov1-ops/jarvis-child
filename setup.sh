#!/bin/bash
# ═══════════════════════════════════════════════════
#  JARVIS BOT — Установщик
#  Автор: @sss_only
#  Запуск: bash setup.sh
# ═══════════════════════════════════════════════════

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║        JARVIS BOT — Установка        ║${NC}"
echo -e "${CYAN}║           by @sss_only 🥷🏻            ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
echo ""

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
OS="$(uname -s)"

# ── Проверяем Python ──────────────────────────────
echo -e "${YELLOW}[1/5] Проверяю Python...${NC}"
if command -v python3 &>/dev/null; then
    PY=$(python3 --version)
    echo -e "  ${GREEN}✓ $PY${NC}"
else
    echo -e "  ${RED}✗ Python3 не найден. Установи с python.org${NC}"
    exit 1
fi

# ── Устанавливаем зависимости ─────────────────────
echo -e "${YELLOW}[2/5] Устанавливаю зависимости...${NC}"
pip3 install -q anthropic requests Pillow openai-whisper static-ffmpeg openpyxl pdfminer.six 2>&1 | tail -3
echo -e "  ${GREEN}✓ Готово${NC}"

# ── Проверяем config.py ───────────────────────────
echo -e "${YELLOW}[3/5] Проверяю конфигурацию...${NC}"
CONFIG="$BOT_DIR/bot/config.py"
if grep -q "ВСТАВЬ_ТОКЕН_БОТА" "$CONFIG"; then
    echo ""
    echo -e "${YELLOW}  Нужно заполнить 3 параметра в bot/config.py:${NC}"
    echo ""
    echo -e "${CYAN}  TELEGRAM_TOKEN${NC} — создай бота через @BotFather в Telegram"
    echo -e "${CYAN}  ANTHROPIC_KEY${NC}  — получи на console.anthropic.com"
    echo -e "${CYAN}  CHAT_ID${NC}        — напиши @userinfobot в Telegram"
    echo ""
    read -p "  Открыть config.py для редактирования сейчас? [y/n]: " EDIT
    if [ "$EDIT" = "y" ] || [ "$EDIT" = "Y" ]; then
        if command -v nano &>/dev/null; then
            nano "$CONFIG"
        elif command -v vim &>/dev/null; then
            vim "$CONFIG"
        else
            echo -e "  Открой файл вручную: ${CYAN}$CONFIG${NC}"
            exit 1
        fi
    else
        echo -e "  ${YELLOW}Заполни config.py и запусти setup.sh снова.${NC}"
        exit 0
    fi
fi

# Финальная проверка
if grep -q "ВСТАВЬ_ТОКЕН_БОТА" "$CONFIG"; then
    echo -e "  ${RED}✗ config.py не заполнен. Заполни и запусти снова.${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓ config.py заполнен${NC}"

# ── Создаём папки ─────────────────────────────────
echo -e "${YELLOW}[4/5] Создаю рабочие папки...${NC}"
mkdir -p "$BOT_DIR/Логи"
mkdir -p "$BOT_DIR/Медиа"
mkdir -p "$BOT_DIR/bot/drafts"
mkdir -p "/tmp/jarvis_bot_media"
echo -e "  ${GREEN}✓ Папки созданы${NC}"

# ── Настраиваем автозапуск ────────────────────────
echo -e "${YELLOW}[5/5] Настраиваю автозапуск...${NC}"

if [ "$OS" = "Darwin" ]; then
    # macOS — LaunchAgent
    PLIST="$HOME/Library/LaunchAgents/com.jarvis.bot.plist"
    cat > "$PLIST" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.jarvis.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$BOT_DIR/bot/claude_bot.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>10</integer>
    <key>StandardOutPath</key>
    <string>$BOT_DIR/bot/claude_bot.log</string>
    <key>StandardErrorPath</key>
    <string>$BOT_DIR/bot/claude_bot.log</string>
    <key>WorkingDirectory</key>
    <string>$BOT_DIR</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>$HOME</string>
    </dict>
</dict>
</plist>
EOF
    launchctl unload "$PLIST" 2>/dev/null || true
    launchctl load "$PLIST"
    echo -e "  ${GREEN}✓ LaunchAgent настроен (автозапуск при входе в систему)${NC}"

elif [ "$OS" = "Linux" ]; then
    # Linux — systemd user service
    SVCDIR="$HOME/.config/systemd/user"
    mkdir -p "$SVCDIR"
    cat > "$SVCDIR/jarvis-bot.service" << EOF
[Unit]
Description=Jarvis Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=$BOT_DIR
ExecStart=/usr/bin/python3 $BOT_DIR/bot/claude_bot.py
Restart=always
RestartSec=10
StandardOutput=append:$BOT_DIR/bot/claude_bot.log
StandardError=append:$BOT_DIR/bot/claude_bot.log

[Install]
WantedBy=default.target
EOF
    systemctl --user enable jarvis-bot
    systemctl --user start jarvis-bot
    echo -e "  ${GREEN}✓ systemd сервис настроен${NC}"
else
    # Fallback — просто запускаем
    echo -e "  ${YELLOW}⚠ Автозапуск для $OS не настроен, запускаю вручную${NC}"
    nohup python3 "$BOT_DIR/bot/claude_bot.py" >> "$BOT_DIR/bot/claude_bot.log" 2>&1 &
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          ✓ Установка готова!          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "  Бот запущен и работает."
echo -e "  Напиши своему боту в Telegram — он ответит."
echo -e "  Логи: ${CYAN}$BOT_DIR/bot/claude_bot.log${NC}"
echo ""
echo -e "  ${CYAN}Создано by @sss_only 🥷🏻${NC}"
echo ""
