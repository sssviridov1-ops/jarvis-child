#!/usr/bin/env python3
# Утренний план — отправляется в топик "Задачи" в 8:00
# + блок идей для Jarvis: поиск GitHub/интернет через Claude

import os
import glob
import urllib.request
import urllib.parse
from datetime import datetime

import sys
sys.path.insert(0, "/Users/sss_only/VS CODE 1/bot")
from config import TELEGRAM_TOKEN, GROUP_ID, TOPIC_ZADACHI, DRAFTS_DIR, ANTHROPIC_KEY


def send(text, thread_id=None, retries=3):
    url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": GROUP_ID, "text": text[:4000], "parse_mode": "Markdown"}
    if thread_id:
        data["message_thread_id"] = str(thread_id)
    encoded = urllib.parse.urlencode(data).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=encoded)
            urllib.request.urlopen(req, timeout=15)
            return
        except Exception as e:
            print(f"[WARN] send attempt {attempt+1} failed: {e}", flush=True)
            import time; time.sleep(5)
    print("[ERR] Не удалось отправить после 3 попыток", flush=True)


def get_draft():
    """Берём черновик на сегодня или последний сохранённый."""
    today = datetime.now().strftime("%d_%m_%Y")
    path  = os.path.join(DRAFTS_DIR, f"plan_{today}.txt")
    if os.path.exists(path):
        return open(path, encoding="utf-8").read().strip()
    drafts = sorted(glob.glob(os.path.join(DRAFTS_DIR, "plan_*.txt")))
    if drafts:
        return open(drafts[-1], encoding="utf-8").read().strip()
    return None


def get_jarvis_ideas():
    """Ищет свежие идеи для Jarvis через Claude + WebSearch."""
    try:
        import anthropic, subprocess, os as _os

        # Путь к Claude CLI
        claude_bin = "/Users/sss_only/.vscode/extensions/anthropic.claude-code-2.1.87-darwin-arm64/resources/native-binary/claude"
        if not _os.path.exists(claude_bin):
            return None

        prompt = (
            "Используй WebSearch чтобы найти 3-5 свежих идей для персонального AI Telegram бота на Claude. "
            "Ищи: 'telegram bot AI features 2025', 'Claude API new features', 'personal AI assistant ideas github'. "
            "Выбери самые интересные и практичные идеи которых ещё нет в боте. "
            "Формат ответа — короткий список с эмодзи, без воды. Максимум 10 строк."
        )

        r = subprocess.run(
            [claude_bin, "--print", "--dangerously-skip-permissions", "--bare", prompt],
            capture_output=True, text=True, timeout=60,
            cwd="/Users/sss_only/VS CODE 1",
            env={**_os.environ, "HOME": _os.path.expanduser("~"), "ANTHROPIC_API_KEY": ANTHROPIC_KEY}
        )
        result = (r.stdout + r.stderr).strip()
        if result and len(result) > 20:
            return result[:800]
    except Exception as e:
        print(f"[IDEAS] {e}", flush=True)
    return None


def main():
    now   = datetime.now()
    draft = get_draft()

    # Основной план
    if draft:
        plan_text = draft
    else:
        plan_text = (
            f"☀️ Доброе утро, Сергей. {now.strftime('%d.%m.%Y')}\n\n"
            "Черновика плана нет — сформируй задачи на день."
        )

    send(plan_text, thread_id=TOPIC_ZADACHI)
    print(f"Утренний план отправлен ({now:%H:%M})")

    # Блок идей для Jarvis — отдельным сообщением
    print("Ищу идеи для Jarvis...", flush=True)
    ideas = get_jarvis_ideas()
    if ideas:
        ideas_text = f"💡 *Идеи для Jarvis на сегодня:*\n\n{ideas}"
        send(ideas_text, thread_id=TOPIC_ZADACHI)
        print("Идеи отправлены")
    else:
        print("Идеи не найдены (пропускаем)")


if __name__ == "__main__":
    main()
