#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  JARVIS BOT — Быстрая установка одной командой
#
#  Использование:
#  curl -s https://raw.githubusercontent.com/sviridovss/jarvis-child/main/install.sh | bash
#
#  by @sss_only 🥷🏻
# ═══════════════════════════════════════════════════════════════

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo ""
echo -e "${CYAN}${BOLD}"
echo "   ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗"
echo "   ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝"
echo "   ██║███████║██████╔╝██║   ██║██║███████╗"
echo "██╗██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║"
echo "╚████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║"
echo " ╚═══╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝"
echo -e "${NC}"
echo -e "${CYAN}${BOLD}           Персональный AI-ассистент${NC}"
echo -e "${CYAN}           Telegram + Claude + Mac/Linux${NC}"
echo ""
echo -e "${YELLOW}  Что умеет JARVIS:${NC}"
echo "  🧠  Думает и отвечает через Claude AI (Sonnet + Opus)"
echo "  🎙  Распознаёт голосовые сообщения (Whisper)"
echo "  📹  Превращает видео в сценарий Reel + текст поста"
echo "  📸  Анализирует фото через Vision AI"
echo "  📊  Читает PDF, Excel, документы"
echo "  🖼  Генерирует карусели PNG в твоём стиле"
echo "  💻  Управляет твоим Mac (bash, файлы, процессы)"
echo "  📷  Делает снимок с веб-камеры по команде"
echo "  ⏰  Ставит напоминания"
echo "  📋  Ведёт дневные логи и историю"
echo "  🌐  Ищет информацию в интернете"
echo "  🗂  Работает в разных топиках группы с отдельным контекстом"
echo "  🔁  Запускается автоматически, переживает перезагрузки"
echo ""
echo -e "${CYAN}  by @sss_only 🥷🏻${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ── Проверки ──────────────────────────────────────────────────
echo -e "${YELLOW}[1/4] Проверяю систему...${NC}"

OS="$(uname -s)"
echo -e "  Система: ${CYAN}$OS$(uname -m)${NC}"

if ! command -v python3 &>/dev/null; then
    echo -e "  ${RED}✗ Python3 не найден.${NC}"
    if [ "$OS" = "Darwin" ]; then
        echo "  Установи через: brew install python3"
        echo "  или скачай с: python.org"
    else
        echo "  Установи через: sudo apt install python3 python3-pip"
    fi
    exit 1
fi
echo -e "  ${GREEN}✓ Python: $(python3 --version)${NC}"

if ! command -v git &>/dev/null; then
    echo -e "  ${RED}✗ Git не найден.${NC}"
    if [ "$OS" = "Darwin" ]; then
        echo "  Установи: xcode-select --install"
    else
        echo "  Установи: sudo apt install git"
    fi
    exit 1
fi
echo -e "  ${GREEN}✓ Git: $(git --version | head -1)${NC}"

# ── Клонируем репо ────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[2/4] Скачиваю JARVIS...${NC}"
INSTALL_DIR="$HOME/jarvis_bot"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "  Папка уже существует — обновляю..."
    cd "$INSTALL_DIR" && git pull
else
    git clone https://github.com/sviridovss/jarvis-child "$INSTALL_DIR" 2>&1 | tail -3
fi
echo -e "  ${GREEN}✓ Скачано в: $INSTALL_DIR${NC}"

# ── Запускаем setup.sh ────────────────────────────────────────
echo ""
echo -e "${YELLOW}[3/4] Запускаю установщик...${NC}"
cd "$INSTALL_DIR"
bash setup.sh

echo ""
echo -e "${GREEN}${BOLD}  JARVIS установлен и запущен! 🚀${NC}"
echo ""
echo -e "  ${CYAN}Создано by @sss_only 🥷🏻${NC}"
echo "  t.me/sviridovss"
echo ""
