import os
import uuid
import random
from datetime import datetime, timedelta

MEDIA_DIR = "media"


def format_price(price, currency="$"):
    price = float(price)
    if price == int(price):
        return f"{int(price)}{currency}"
    return f"{price:.2f}{currency}"


async def save_telegram_photo(bot, file_id, subdir):
    """Telegram file_ids only work with the bot that received them.
    Since we run multiple bots, download the photo once and re-serve it from disk."""
    folder = os.path.join(MEDIA_DIR, subdir)
    os.makedirs(folder, exist_ok=True)
    tg_file = await bot.get_file(file_id)
    path = os.path.join(folder, f"{uuid.uuid4().hex}.jpg")
    await tg_file.download_to_drive(path)
    return path


def generate_khqr_image(account_id, merchant_name, merchant_city, amount, bill_number):
    """Generate a real Cambodia KHQR (EMV-compliant) with the exact amount baked in,
    so the buyer's banking app auto-fills the correct amount when they scan.
    Returns a local PNG path on success, or None on any failure (caller should fall
    back to the static uploaded QR photo instead)."""
    try:
        from bakong_khqr import KHQR
    except ImportError:
        return None

    try:
        khqr = KHQR()
        qr_string = khqr.create_qr(
            account_id=account_id,
            merchant_name=merchant_name,
            merchant_city=merchant_city or "Phnom Penh",
            amount=float(amount),
            currency="USD",
            store_label="Uchiro Store",
            bill_number=bill_number,
            static=False,
        )
        folder = os.path.join(MEDIA_DIR, "khqr")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{uuid.uuid4().hex}.png")
        khqr.qr_image(qr_string, output_path=path, format="png")
        return path if os.path.exists(path) else None
    except Exception:
        return None


def verify_webapp_init_data(init_data: str, bot_token: str):
    """Validate Telegram WebApp initData per Telegram's documented HMAC scheme, so the
    Mini App backend can trust the telegram user id it receives instead of anyone being
    able to POST orders as an arbitrary user. Returns the parsed user dict on success,
    or None if the signature is missing/invalid."""
    import hashlib
    import hmac
    import json
    from urllib.parse import parse_qsl

    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
        received_hash = parsed.pop("hash", None)
        if not received_hash:
            return None
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(computed_hash, received_hash):
            return None
        user_json = parsed.get("user")
        return json.loads(user_json) if user_json else None
    except Exception:
        return None


def warranty_status(approved_at, warranty_days):
    """Human-readable Khmer warranty countdown for an approved order.
    Returns None if the item has no warranty (warranty_days=0) or the order isn't approved yet."""
    if not approved_at or not warranty_days:
        return None
    try:
        approved = datetime.strptime(approved_at, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    expires = approved + timedelta(days=warranty_days)
    remaining = (expires - datetime.utcnow()).days
    if remaining < 0:
        return f"❌ Warranty ផុតកំណត់ (ផុតកាលពី {expires.strftime('%d/%m/%Y')})"
    return f"🛡️ Warranty នៅសល់ {remaining} ថ្ងៃ (ផុតកំណត់ {expires.strftime('%d/%m/%Y')})"


def pick_weighted_spin(pool):
    """pool: list of rows with 'name' and 'weight'. Picks one item, probability proportional
    to its weight relative to the total (weights don't need to sum to 100 - they're normalized)."""
    if not pool:
        return None
    total = sum(row["weight"] for row in pool)
    if total <= 0:
        return None
    r = random.uniform(0, total)
    upto = 0
    for row in pool:
        upto += row["weight"]
        if upto >= r:
            return row
    return pool[-1]  # floating point safety net
