#!/usr/bin/env python3
# Утренняя рассылка метрик — запускается cron в 9:00 каждый день
# Отправляет в топик "Задачи" группы

import sys
import urllib.request
import urllib.parse
sys.path.insert(0, "/Users/sss_only/VS CODE 1/bot")
from config import TELEGRAM_TOKEN, GROUP_ID, TOPIC_ZADACHI
from metrics_tracker import build_metrics_summary


def send_message(text, thread_id=None):
    url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id":    GROUP_ID,
        "text":       text,
        "parse_mode": "Markdown"
    }
    if thread_id:
        data["message_thread_id"] = str(thread_id)
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded)
    urllib.request.urlopen(req)


def main():
    summary = build_metrics_summary(days=14)

    hint = (
        "\n\n*Как внести метрики:*\n"
        "В лог дня (`ДД_ММ_ГГГГ.md`) добавь:\n"
        "```\n"
        "## Метрики Название поста (ДД.ММ.ГГГГ)\n"
        "охват 540\n"
        "просмотры 1200\n"
        "лайки 38\n"
        "комменты 5\n"
        "сохр 14\n"
        "er 9.6\n"
        "```"
    )

    if summary:
        message = f"📊 *Метрики — доброе утро*\n\n{summary}{hint}"
    else:
        message = f"📊 *Метрики — доброе утро*\n\nДанных пока нет.{hint}"

    send_message(message, thread_id=TOPIC_ZADACHI)
    print("Метрики отправлены в топик Задачи")


if __name__ == "__main__":
    main()
