# ============================================
# PATCH PARA PYTHON 3.14+ (removeu o imghdr)
# ============================================
import sys
import types

if sys.version_info >= (3, 14):
    imghdr = types.ModuleType('imghdr')
    def what(file, h=None):
        return None
    imghdr.what = what
    sys.modules['imghdr'] = imghdr

# ============================================
# IMPORTS
# ============================================
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import sqlite3
from datetime import datetime, timedelta
import random
import string

# ============================================
# CONFIGURAÇÕES
# ============================================
BOT_TOKEN = "8840039207:AAEuUFTayyACnskLZGmqxjgXdNjDE2snSPA"
ADMIN_ID = 8881712229
PIX_KEY = "suporte@annynhafunny.com"

# ============================================
# BANCO DE DADOS
# ============================================
def init_db():
    conn = sqlite3.connect('mimo_sinha.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            subscription TEXT,
            subscription_end DATE,
            created_at DATE,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            transaction_id TEXT,
            amount REAL,
            method TEXT,
            status TEXT,
            created_at DATE
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('mimo_sinha.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, datetime.now().date()))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('mimo_sinha.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result

def update_subscription(user_id, plan, days=30):
    conn = sqlite3.connect('mimo_sinha.db')
    c = conn.cursor()
    end_date = datetime.now().date() + timedelta(days=days)
    c.execute('''
        UPDATE users SET subscription = ?, subscription_end = ?
        WHERE user_id = ?
    ''', (plan, end_date, user_id))
    conn.commit()
    conn.close()

def check_subscription(user_id):
    conn = sqlite3.connect('mimo_sinha.db')
    c = conn.cursor()
    c.execute('SELECT subscription_end FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    if result and result[0]:
        end_date = datetime.strptime(result[0], '%Y-%m-%d').date()
        return end_date > datetime.now().date()
    return False

def save_payment(user_id, transaction_id, amount, method, status):
    conn = sqlite3.connect('mimo_sinha.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO payments (user_id, transaction_id, amount, method, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, transaction_id, amount, method, status, datetime.now().date()))
    conn.commit()
    conn.close()

def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# ============================================
# TECLADOS
# ============================================
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📋 Assinar", callback_data="subscribe")],
        [InlineKeyboardButton("🎯 Promoções", callback_data="promotions")],
        [InlineKeyboardButton("📂 Categorias", callback_data="categories")],
        [InlineKeyboardButton("👩 Modelos", callback_data="models")],
        [InlineKeyboardButton("👤 Minha Conta", callback_data="my_account")],
        [InlineKeyboardButton("💳 Meus Pagamentos", callback_data="my_payments")],
        [InlineKeyboardButton("📦 Meus Produtos", callback_data="my_products")],
        [InlineKeyboardButton("🎫 Cupons", callback_data="coupons")],
        [InlineKeyboardButton("👥 Indique Amigos", callback_data="referral")],
        [InlineKeyboardButton("🆘 Suporte", callback_data="support")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("⚙️ Configurações", callback_data="settings")],
        [InlineKeyboardButton("🆕 Conteúdo Recente", callback_data="recent_content")],
        [InlineKeyboardButton("👑 PAINEL ADMIN", callback_data="admin_panel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="back_main")]])

# ============================================
# MENSAGEM DE BOAS-VINDAS
# ============================================
WELCOME_MESSAGE = """
🌺 **MIMOSA HOT — CONTEÚDO EXCLUSIVO**

Olá, {name}! 👋

Bem-vindo ao paraíso proibido!

Escolha uma opção abaixo:
"""

# ============================================
# HANDLERS
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name, user.last_name)
    await update.message.reply_text(
        WELCOME_MESSAGE.format(name=user.first_name),
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "back_main":
        await query.edit_message_text(
            WELCOME_MESSAGE.format(name=query.from_user.first_name),
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            f"📌 Você selecionou: {data}\n\nEm desenvolvimento...",
            reply_markup=back_button(),
            parse_mode='Markdown'
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.lower() == "voltar":
        await update.message.reply_text(
            WELCOME_MESSAGE.format(name=update.effective_user.first_name),
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )

# ============================================
# MAIN
# ============================================
def main():
    init_db()
    print("🤖 Bot iniciado!")
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🔄 Aguardando mensagens...")
    application.run_polling()

if __name__ == "__main__":
    main()