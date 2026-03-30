#!/usr/bin/env python3
# Получает метрики от Сергея через Telegram и сохраняет в metrics.json
# Запускается кроном каждые 5 минут
# Поддерживает: текстовые сообщения и скриншоты (фото → Claude Vision)

import urllib.request
import urllib.parse
import json
import os
import sys
import re
import base64
import tempfile
from datetime import datetime

sys.path.insert(0, "/Users/sss_only/VS CODE 1/bot")
from config import TELEGRAM_TOKEN as TOKEN, CHAT_ID, ANTHROPIC_KEY as ANTHROPIC_API_KEY, BOT_DIR

STATE_FILE = f"{BOT_DIR}/tg_state.json"
METRICS_DB = f"{BOT_DIR}/metrics.json"


# ---------------------------------------------------------------------------
# Telegram helpers
# ---------------------------------------------------------------------------

def api_post(method, params):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = json.dumps(params).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def send_message(text):
    api_post("sendMessage", {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })


# ---------------------------------------------------------------------------
# State (Telegram offset)
# ---------------------------------------------------------------------------

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"offset": 0}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


# ---------------------------------------------------------------------------
# Metrics DB
# ---------------------------------------------------------------------------

def load_metrics():
    if os.path.exists(METRICS_DB):
        with open(METRICS_DB, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_metrics(data):
    with open(METRICS_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Message parser
# ---------------------------------------------------------------------------

def parse_metrics_message(text):
    """
    Принимает сообщения вида:
      мечты reels: охват 500, er 5.2, сохр 3, лайки 20, комменты 0
      время карусель: охват 400, er 4.1, сохр 2
      мечты: 500, 5.2, 3          ← позиционный (охват, ER, сохр)
      мечты: 500, 5.2, 3, 20      ← + лайки

    Возвращает dict или None если не распознано.
    """
    raw = text.strip()
    lower = raw.lower()

    # Должно быть двоеточие
    if ":" not in lower:
        return None

    colon_pos = lower.index(":")
    left = lower[:colon_pos].strip()
    rest = lower[colon_pos + 1:].strip()

    # Тип поста
    post_type = None
    for word, label in [("reels", "reels"), ("рилс", "reels"),
                         ("карусель", "карусель"), ("carousel", "карусель")]:
        if word in left:
            post_type = label
            left = left.replace(word, "").strip()

    post_name = left.strip(" «»\"'").strip()
    if not post_name:
        return None

    metrics = {}

    # Именованные метрики
    named = [
        (r"охват\s*[:\s]*([\d\s]+)",                      "reach",       int),
        (r"просмотр\w*\s*[:\s]*([\d\s]+)",                "impressions", int),
        (r"(?:^|[,\s])er\s*[:\s]*(\d+(?:[.,]\d+)?)",     "er",          float),
        (r"сохр\w*\s*[:\s]*([\d\s]+)",                    "saves",       int),
        (r"лайк\w*\s*[:\s]*([\d\s]+)",                    "likes",       int),
        (r"коммент\w*\s*[:\s]*([\d\s]+)",                 "comments",    int),
        (r"перес\w*\s*[:\s]*([\d\s]+)",                   "shares",      int),
        (r"репост\w*\s*[:\s]*([\d\s]+)",                  "reposts",     int),
    ]
    for pattern, key, cast in named:
        m = re.search(pattern, rest)
        if m:
            val = m.group(1).replace(" ", "").replace(",", ".")
            try:
                metrics[key] = cast(float(val))
            except ValueError:
                pass

    # Позиционный формат: числа через запятую без ключевых слов
    if not metrics:
        nums = re.findall(r"[\d]+(?:[.,][\d]+)?", rest)
        order = ["reach", "er", "saves", "likes", "comments"]
        casts = [int, float, int, int, int]
        for i, val in enumerate(nums[:5]):
            try:
                metrics[order[i]] = casts[i](float(val.replace(",", ".")))
            except (ValueError, IndexError):
                pass

    if not metrics:
        return None

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "post": post_name,
        "type": post_type,
        **metrics
    }


# ---------------------------------------------------------------------------
# Claude Vision — extract metrics from screenshot
# ---------------------------------------------------------------------------

def download_photo(file_id):
    """Скачать фото из Telegram по file_id, вернуть bytes."""
    r = api_post("getFile", {"file_id": file_id})
    file_path = r["result"]["file_path"]
    url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        return resp.read()


def extract_metrics_from_image(image_bytes):
    """
    Отправить скриншот в Claude Haiku, получить метрики в JSON.
    Возвращает dict или None.
    """
    if not ANTHROPIC_API_KEY:
        return None

    b64 = base64.b64encode(image_bytes).decode()
    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 512,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": b64}
                },
                {
                    "type": "text",
                    "text": (
                        "Это скриншот метрик Instagram/Meta. "
                        "Извлеки все числовые метрики которые видишь. "
                        "Верни ТОЛЬКО JSON без пояснений:\n"
                        '{"post": "название поста или темы", '
                        '"type": "reels|карусель|пост", '
                        '"reach": число, '
                        '"impressions": число, '
                        '"likes": число, '
                        '"comments": число, '
                        '"saves": число, '
                        '"shares": число, '
                        '"er": число_с_плавающей_точкой}\n'
                        "Если поле не видно — не включай его. "
                        "post — короткое название на русском."
                    )
                }
            ]
        }]
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
    text = result["content"][0]["text"].strip()
    # Извлекаем JSON из ответа
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        return None
    parsed = json.loads(match.group())
    parsed["date"] = datetime.now().strftime("%Y-%m-%d")
    return parsed


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def save_parsed(db, parsed):
    existing = next(
        (r for r in db
         if r.get("post", "").lower() == parsed["post"].lower()
         and r.get("date") == parsed["date"]),
        None
    )
    if existing:
        existing.update(parsed)
        return "обновлены"
    else:
        db.append(parsed)
        return "сохранены"


def process_updates():
    state = load_state()

    result = api_post("getUpdates", {
        "offset": state["offset"],
        "timeout": 0,
        "limit": 20,
        "allowed_updates": ["message"]
    })

    updates = result.get("result", [])
    if not updates:
        return

    db = load_metrics()

    for update in updates:
        state["offset"] = update["update_id"] + 1

        msg = update.get("message", {})
        chat_id = str(msg.get("chat", {}).get("id", ""))

        if chat_id != CHAT_ID:
            continue

        parsed = None

        # Фото — скриншот метрик
        photos = msg.get("photo")
        if photos:
            largest = max(photos, key=lambda p: p.get("file_size", 0))
            try:
                image_bytes = download_photo(largest["file_id"])
                parsed = extract_metrics_from_image(image_bytes)
                if not parsed:
                    send_message("Скриншот получен, но не удалось прочитать метрики. Попробуй другой скриншот.")
            except Exception as e:
                send_message(f"Ошибка обработки фото: {e}")
        else:
            # Текстовое сообщение
            text = msg.get("text", "").strip()
            parsed = parse_metrics_message(text)

        if not parsed:
            continue

        action = save_parsed(db, parsed)
        save_metrics(db)

        reach = parsed.get("reach", "—")
        er = parsed.get("er", "—")
        saves = parsed.get("saves", "—")
        post_label = parsed.get("type", "пост")
        send_message(
            f"Метрики {action} для {post_label} «{parsed['post']}»\n"
            f"Охват: *{reach}* · ER: *{er}%* · Сохр: *{saves}*"
        )

    save_state(state)


if __name__ == "__main__":
    process_updates()
