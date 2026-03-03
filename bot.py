# ns.py — FINAL ULTIMATE FUNNEL BOT (IMAGE + CAPTION + INLINE BUTTON FIXED)

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import segno

# ================== 🔑 SETTINGS ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [6411315434, 7565335801]

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

USERS_FILE = "users.json"
CONFIG_FILE = "config.json"
PENDING_FILE = "pending.json"
ADMIN_STATE = {}

# ================== ⚙️ DEFAULT CONFIG ==================
DEFAULT_CONFIG = {
    "start_photo": "",   # 🔥 NEW: file_id store hoga
    "start_caption": (
        "<b>Premium Access Channel 🌸\n\n"
        "For Exclusive Content Lovers 😋\n\n"
        "51000+ rare content available 🎀\n\n"
        "Direct video No Link 🔥\n\n"
        "Price :- ₹99.00/-\n"
        "Validity :- lifetime</b>"
    ),
    "upi_id": "sohilkhan.21@fam",
    "demo_link": "https://t.me/",
    "howto_link": "https://t.me/",
    "private_message": "🎉 Payment Approved!\nHere is your Premium Access Link.",
    "price_main": 99,
    "price_offer": 59
}

# ================== FILE SAFETY ==================
def ensure_files():
    if not os.path.exists(USERS_FILE):
        json.dump([], open(USERS_FILE, "w"), indent=4)

    if not os.path.exists(PENDING_FILE):
        json.dump({}, open(PENDING_FILE, "w"), indent=4)

    if not os.path.exists(CONFIG_FILE):
        json.dump(DEFAULT_CONFIG, open(CONFIG_FILE, "w"), indent=4)

ensure_files()

def load_users():
    try:
        return json.load(open(USERS_FILE))
    except:
        return []

def save_users(data):
    json.dump(data, open(USERS_FILE, "w"), indent=4)

def load_pending():
    try:
        return json.load(open(PENDING_FILE))
    except:
        return {}

def save_pending(data):
    json.dump(data, open(PENDING_FILE, "w"), indent=4)

def load_config():
    try:
        cfg = json.load(open(CONFIG_FILE))
    except:
        cfg = DEFAULT_CONFIG
    return cfg

def save_config(cfg):
    json.dump(cfg, open(CONFIG_FILE, "w"), indent=4)

# ================== USER REGISTER ==================
def register_user(user):
    users = load_users()
    if user.id not in users:
        users.append(user.id)
        save_users(users)
        for admin in ADMIN_IDS:
            try:
                bot.send_message(
                    admin,
                    f"🆕 New User Joined\n\n"
                    f"👤 {user.first_name}\n"
                    f"🆔 {user.id}\n"
                    f"📊 Total Users: {len(users)}"
                )
            except:
                pass

# ================== START (FIXED) ==================
@bot.message_handler(commands=['start'])
def start(m):
    cfg = load_config()
    register_user(m.from_user)

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("💎 Get Premium", callback_data="buy"))
    kb.add(InlineKeyboardButton("🎥 Premium Demo", url=cfg["demo_link"]))
    kb.add(InlineKeyboardButton("✅ How to Get Premium", url=cfg["howto_link"]))

    # 🔥 If photo set → send photo + caption + buttons together
    if cfg.get("start_photo"):
        try:
            bot.send_photo(
                m.chat.id,
                cfg["start_photo"],
                caption=cfg["start_caption"],
                reply_markup=kb
            )
        except:
            bot.send_message(m.chat.id, cfg["start_caption"], reply_markup=kb)
    else:
        bot.send_message(m.chat.id, cfg["start_caption"], reply_markup=kb)

# ================== ADMIN SET START IMAGE ==================
@bot.message_handler(commands=['setstart'])
def set_start_photo(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    bot.send_message(m.chat.id, "Send start image now.")

    ADMIN_STATE[m.from_user.id] = "waiting_photo"

@bot.message_handler(content_types=['photo'])
def save_start_photo(m):
    if m.from_user.id not in ADMIN_IDS:
        return

    if ADMIN_STATE.get(m.from_user.id) == "waiting_photo":
        cfg = load_config()
        cfg["start_photo"] = m.photo[-1].file_id
        save_config(cfg)

        bot.send_message(m.chat.id, "Start image saved successfully ✅")
        del ADMIN_STATE[m.from_user.id]

# ================== BUY PANEL ==================
@bot.callback_query_handler(func=lambda c: c.data == "buy")
def buy(c):
    cfg = load_config()
    link = f"upi://pay?pa={cfg['upi_id']}&pn=VIP&am={cfg['price_main']}&cu=INR"
    qr = f"qr_{c.from_user.id}.png"
    segno.make(link).save(qr, scale=6)

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📸 I HAVE PAID", callback_data="ss"))

    bot.send_photo(
        c.message.chat.id,
        open(qr, "rb"),
        caption=(
            f"💎 VIP ACCESS PAYMENT\n\n"
            f"Price: ₹{cfg['price_main']}\n\n"
            f"UPI: {cfg['upi_id']}"
        ),
        reply_markup=kb
    )

# ================== RUN ==================
print("🔥 BOT RUNNING STABLE...")
bot.infinity_polling(skip_pending=True)
