#!/usr/bin/env python3
# Еженедельный дайджест — каждое воскресенье в 10:00
# Анализирует логи недели и отправляет summary в топик Задачи

import os
import glob
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta

import sys
sys.path.insert(0, "/Users/sss_only/VS CODE 1/bot")
from config import TELEGRAM_TOKEN, GROUP_ID, TOPIC_ZADACHI, LOGS_DIR, ANTHROPIC_KEY

try:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    HAS_ANTHROPIC = True
except Exception:
    HAS_ANTHROPIC = False


def send(text, thread_id=None, retries=3):
    url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": GROUP_ID, "text": text[:4000], "parse_mode": "Markdown"}
    if thread_id:
        data["message_thread_id"] = str(thread_id)
    for attempt in range(retries):
        try:
            encoded = urllib.parse.urlencode(data).encode()
            urllib.request.urlopen(urllib.request.Request(url, data=encoded), timeout=15)
            return
        except Exception as e:
            print(f"[WARN] send attempt {attempt+1}: {e}")
            import time; time.sleep(5)


def get_week_logs():
    """Собирает логи за последние 7 дней."""
    logs = []
    for i in range(7):
        day = (datetime.now() - timedelta(days=i)).strftime("%d_%m_%Y")
        path = os.path.join(LOGS_DIR, f"{day}.md")
        if os.path.exists(path):
            content = open(path, encoding="utf-8").read().strip()
            if content:
                logs.append(f"=== {day} ===\n{content[:3000]}")
    return "\n\n".join(logs)


def build_digest(logs_text):
    if not HAS_ANTHROPIC or not logs_text:
        return None
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content":
            f"Ты анализируешь рабочую неделю Сергея Свиридова. Вот логи за 7 дней:\n\n{logs_text[:12000]}\n\n"
            f"Напиши еженедельный дайджест в формате:\n"
            f"1. ✅ Что сделано (топ-5)\n"
            f"2. ❌ Что не сделано / перенесено\n"
            f"3. 📊 Метрики если есть\n"
            f"4. 💡 Главный вывод недели (1-2 предложения)\n"
            f"5. 🎯 Фокус на следующую неделю (3 приоритета)\n\n"
            f"Пиши кратко, по делу, без воды."
        }]
    )
    return resp.content[0].text.strip()


def main():
    now = datetime.now()
    week_num = now.isocalendar()[1]
    logs = get_week_logs()

    if logs:
        digest = build_digest(logs)
    else:
        digest = None

    if digest:
        text = f"📋 *Дайджест недели #{week_num}* ({now.strftime('%d.%m.%Y')})\n\n{digest}"
    else:
        text = (
            f"📋 *Дайджест недели #{week_num}* ({now.strftime('%d.%m.%Y')})\n\n"
            "Логов за неделю нет — веди записи в логи чтобы дайджест был содержательным."
        )

    send(text, thread_id=TOPIC_ZADACHI)
    print(f"Дайджест недели #{week_num} отправлен")


if __name__ == "__main__":
    main()
