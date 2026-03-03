# ns.py - FINAL ULTIMATE FUNNEL BOT (ALL ADMIN FEATURES + ZERO ERRORS + STABLE)

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
    "start_channel": "@yourchannel",
    "start_post_id": 1,
    "start_caption": (
        "<b>Direct P#rn Video Channel 🌸\n\n"
        "For Desi Content Lovers 😋\n"
        "No Sn#p, Pure Desi Content 😙\n\n"
        "51000+ rare Desi le#ks ever.... 🎀\n\n"
        "Just pay and get entry...\n\n"
        "Direct video No Link - Ads Sh#t 🔥\n\n"
        "Price :- ₹99.00/-\n\n"
        "Validity :- lifetime</b>"
    ),
    "upi_id": "sohilkhan.21@fam",
    "demo_link": "https://t.me/",
    "howto_link": "https://t.me/",
    "private_message": "🎉 Payment Approved!\nHere is your Premium Access Link.",
    "price_main": 99,
    "price_offer": 59
}

# ================== 🛠 FILE SAFETY ==================

def ensure_files():
    if not os.path.exists(USERS_FILE):
        json.dump([], open(USERS_FILE, "w"), indent=4)
    else:
        try:
            data = json.load(open(USERS_FILE))
            if not isinstance(data, list):
                json.dump([], open(USERS_FILE, "w"), indent=4)
        except:
            json.dump([], open(USERS_FILE, "w"), indent=4)

    if not os.path.exists(PENDING_FILE):
        json.dump({}, open(PENDING_FILE, "w"), indent=4)

    if not os.path.exists(CONFIG_FILE):
        json.dump(DEFAULT_CONFIG, open(CONFIG_FILE, "w"), indent=4)

ensure_files()

# ================== 📥 LOAD SAFE ==================

def load_users():
    try:
        data = json.load(open(USERS_FILE))
        return data if isinstance(data, list) else []
    except:
        return []

def save_users(data):
    json.dump(data, open(USERS_FILE, "w"), indent=4)

def load_pending():
    try:
        data = json.load(open(PENDING_FILE))
        return data if isinstance(data, dict) else {}
    except:
        return {}

def save_pending(data):
    json.dump(data, open(PENDING_FILE, "w"), indent=4)

def load_config():
    try:
        cfg = json.load(open(CONFIG_FILE))
    except:
        cfg = DEFAULT_CONFIG

    updated = False
    for k in DEFAULT_CONFIG:
        if k not in cfg:
            cfg[k] = DEFAULT_CONFIG[k]
            updated = True

    if updated:
        json.dump(cfg, open(CONFIG_FILE, "w"), indent=4)

    return cfg

def save_config(cfg):
    json.dump(cfg, open(CONFIG_FILE, "w"), indent=4)

# ================== 👤 USER REGISTER ==================

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
                    f"👤 Name: {user.first_name}\n"
                    f"🆔 ID: {user.id}\n"
                    f"🔗 Username: @{user.username}\n"
                    f"📊 Total Users: {len(users)}"
                )
            except:
                pass

# ================== 🚀 START (FIXED) ==================

@bot.message_handler(commands=['start'])
def start(m):
    cfg = load_config()
    register_user(m.from_user)

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("💎 Get Premium", callback_data="buy"))
    kb.add(InlineKeyboardButton("🎥 Premium Demo", url=cfg["demo_link"]))
    kb.add(InlineKeyboardButton("✅ How to Get Premium", url=cfg["howto_link"]))

    try:
        sent_msg = bot.copy_message(
            chat_id=m.chat.id,
            from_chat_id=cfg["start_channel"],
            message_id=cfg["start_post_id"]
        )

        bot.edit_message_reply_markup(
            chat_id=m.chat.id,
            message_id=sent_msg.message_id,
            reply_markup=kb
        )

    except:
        bot.send_message(m.chat.id, cfg["start_caption"], reply_markup=kb)

# ================== 💳 QR GENERATOR ==================

def make_qr(upi, amt, uid):
    link = f"upi://pay?pa={upi}&pn=VIP&am={amt}&cu=INR"
    file = f"qr_{uid}.png"
    segno.make(link).save(file, scale=6)
    return file

# ================== 💎 BUY PANEL ==================

@bot.callback_query_handler(func=lambda c: c.data == "buy")
def buy(c):
    cfg = load_config()
    qr = make_qr(cfg["upi_id"], cfg["price_main"], c.from_user.id)

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📸 I HAVE PAID (Submit Screenshot)", callback_data="ss"))
    kb.add(InlineKeyboardButton("🔍 PROOFS", callback_data="proofs"))
    kb.add(InlineKeyboardButton("❌ CANCEL", callback_data="offer"))

    bot.send_photo(
        c.message.chat.id,
        open(qr, "rb"),
        caption=(
            f"💎 <b>VIP ACCESS PAYMENT</b>\n"
            f"🏷 <b>Price: ₹{cfg['price_main']} ONLY!</b>\n\n"
            f"⏳ <b>Offer Expires in: 02:00</b>\n\n"
            f"1️⃣ Scan QR above\n"
            f"2️⃣ Click 'I PAID' below\n\n"
            f"✅ <b>UPI ID:</b> <code>{cfg['upi_id']}</code>"
        ),
        reply_markup=kb
    )

# ================== 🎯 SECRET OFFER ==================

@bot.callback_query_handler(func=lambda c: c.data == "offer")
def offer(c):
    cfg = load_config()
    qr = make_qr(cfg["upi_id"], cfg["price_offer"], c.from_user.id)

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton("📸 I Paid Offer Submit", callback_data="ss"))
    kb.add(InlineKeyboardButton("😔 No thanks", callback_data="reject"))

    bot.send_photo(
        c.message.chat.id,
        open(qr, "rb"),
        caption=(
            f"🛑 <b>WAIT! DON'T GO YET!</b>\n\n"
            f"💎 Original Price: ₹{cfg['price_main']}\n"
            f"🎁 Your Offer Price: ₹{cfg['price_offer']} ONLY!\n\n"
            f"⚠️ This offer disappears in 2 minutes forever.\n\n"
            f"UPI: <code>{cfg['upi_id']}</code>"
        ),
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data == "reject")
def reject(c):
    bot.send_message(c.message.chat.id, "Offer rejected. Click /start again.")

@bot.callback_query_handler(func=lambda c: c.data == "proofs")
def proofs(c):
    bot.answer_callback_query(c.id, "1000+ Successful Payments ✔️", show_alert=True)

# ================== 📸 SCREENSHOT ==================

@bot.callback_query_handler(func=lambda c: c.data == "ss")
def ask_ss(c):
    p = load_pending()
    p[str(c.from_user.id)] = True
    save_pending(p)
    bot.send_message(c.message.chat.id, "Send payment screenshot.")

@bot.message_handler(content_types=['photo'])
def ss(m):
    p = load_pending()
    uid = str(m.from_user.id)
    if uid not in p:
        return

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ APPROVE", callback_data=f"ap_{uid}"),
        InlineKeyboardButton("❌ REJECT", callback_data=f"rj_{uid}")
    )

    for admin in ADMIN_IDS:
        bot.send_photo(admin, m.photo[-1].file_id,
                       caption=f"Payment SS\nUser: {uid}",
                       reply_markup=kb)

    bot.send_message(m.chat.id, "Waiting for admin approval...")

@bot.callback_query_handler(func=lambda c: c.data.startswith("ap_") or c.data.startswith("rj_"))
def decision(c):
    if c.from_user.id not in ADMIN_IDS:
        return

    uid = c.data.split("_")[1]
    cfg = load_config()
    p = load_pending()

    if uid in p:
        if c.data.startswith("ap_"):
            bot.send_message(int(uid), cfg["private_message"])
        else:
            bot.send_message(int(uid), "Payment Rejected.")

        del p[uid]
        save_pending(p)

# ================== 👑 ADMIN PANEL ==================

@bot.message_handler(commands=['admin'])
def admin(m):
    if m.from_user.id not in ADMIN_IDS:
        return

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("💳 Set UPI", callback_data="admin_upi")
    )
    kb.add(
        InlineKeyboardButton("🎥 Set Demo Link", callback_data="admin_demo"),
        InlineKeyboardButton("📘 Set HowTo Link", callback_data="admin_how")
    )
    kb.add(
        InlineKeyboardButton("🔐 Set Private Msg", callback_data="admin_pm"),
        InlineKeyboardButton("🖼 Start Image", callback_data="admin_img")
    )
    kb.add(
        InlineKeyboardButton("✏️ Start Message", callback_data="admin_msg"),
        InlineKeyboardButton("💰 Normal Price", callback_data="admin_price")
    )
    kb.add(
        InlineKeyboardButton("🎁 Offer Price", callback_data="admin_offer")
    )

    bot.send_message(m.chat.id, "👑 FULL ADMIN PANEL", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_"))
def admin_actions(c):
    if c.from_user.id not in ADMIN_IDS:
        return

    ADMIN_STATE[c.from_user.id] = c.data
    bot.send_message(c.message.chat.id, "Send new value:")

@bot.message_handler(func=lambda m: m.from_user.id in ADMIN_STATE)
def admin_input(m):
    state = ADMIN_STATE[m.from_user.id]
    cfg = load_config()

    if state == "admin_upi":
        cfg["upi_id"] = m.text

    elif state == "admin_demo":
        cfg["demo_link"] = m.text

    elif state == "admin_how":
        cfg["howto_link"] = m.text

    elif state == "admin_pm":
        cfg["private_message"] = m.text

    elif state == "admin_msg":
        cfg["start_caption"] = m.text

    elif state == "admin_price":
        cfg["price_main"] = int(m.text)

    elif state == "admin_offer":
        cfg["price_offer"] = int(m.text)

    elif state == "admin_img":
        try:
            ch, pid = m.text.split()
            cfg["start_channel"] = ch
            cfg["start_post_id"] = int(pid)
        except:
            bot.send_message(m.chat.id, "Format: @channel 1")
            return

    elif state == "admin_broadcast":
        users = load_users()
        sent = 0
        for u in users:
            try:
                bot.send_message(u, m.text)
                sent += 1
            except:
                pass

        bot.send_message(m.chat.id, f"Broadcast sent to {sent} users")
        del ADMIN_STATE[m.from_user.id]
        return

    save_config(cfg)
    del ADMIN_STATE[m.from_user.id]
    bot.send_message(m.chat.id, "Updated Successfully ✅")

print("🔥 FINAL ULTIMATE ADMIN FUNNEL BOT RUNNING (NO ERRORS)...")
bot.infinity_polling(skip_pending=True)
