#!/usr/bin/env python3
# Сохраняет черновик плана + отправляет в топик "Задачи"
# Использование:
#   echo "текст" | python3 send_tomorrow.py
#   echo "текст" | python3 send_tomorrow.py --photos-dir /path/to/folder

import sys
import os
import json
import argparse
from datetime import datetime, timedelta

sys.path.insert(0, "/Users/sss_only/VS CODE 1/bot")
from config import TELEGRAM_TOKEN, GROUP_ID, TOPIC_ZADACHI, DRAFTS_DIR

try:
    import requests
except ImportError:
    requests = None

BASE = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_text(text, thread_id=None):
    if not requests:
        return
    data = {"chat_id": GROUP_ID, "text": text}
    if thread_id:
        data["message_thread_id"] = thread_id
    requests.post(f"{BASE}/sendMessage", data=data)


def send_photos(folder, caption="", thread_id=None):
    if not requests or not folder or not os.path.isdir(folder):
        return
    pngs = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".png") and not f.startswith(".")
    ])
    if not pngs:
        return

    media = []
    files = {}
    for i, path in enumerate(pngs):
        key = f"photo{i}"
        files[key] = open(path, "rb")
        item = {"type": "photo", "media": f"attach://{key}"}
        if i == 0 and caption:
            item["caption"] = caption
        media.append(item)

    data = {"chat_id": GROUP_ID, "media": json.dumps(media)}
    if thread_id:
        data["message_thread_id"] = thread_id

    requests.post(f"{BASE}/sendMediaGroup", data=data, files=files)
    for f in files.values():
        f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--photos-dir", default="", help="Папка с PNG слайдами карусели")
    parser.add_argument("--photos-caption", default="🖼 Карусель — готова к публикации")
    args = parser.parse_args()

    message = sys.stdin.read().strip()

    # Сохранить черновик — morning_plan.py его подхватит утром
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d_%m_%Y")
    draft_path = os.path.join(DRAFTS_DIR, f"plan_{tomorrow}.txt")
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(message)

    # Отправить в топик Задачи
    if message:
        send_text(message, thread_id=TOPIC_ZADACHI)

    if args.photos_dir:
        send_photos(args.photos_dir, args.photos_caption, thread_id=TOPIC_ZADACHI)

    print(f"Отправлено в топик Задачи + черновик сохранён ({draft_path})")
