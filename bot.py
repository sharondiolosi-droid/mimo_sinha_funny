import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN, ADMIN_ID
from database import Database
from keyboards import main_menu, back_button
from handlers import show_admin_panel, handle_admin_action
from handlers.user import show_account, show_payments
from handlers.categories import show_categories, show_category_content
from handlers.plans import (
    show_subscription, show_plan_details, show_packages, 
    show_package_details, show_trials, show_trial_details
)
from handlers.payment import process_payment

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

# Welcome message
WELCOME_MESSAGE = """
🌺 **MIMOSA HOT — CONTEÚDO EXCLUSIVO**

Olá, {name}! 👋

Bem-vindo ao paraíso proibido! Aqui você encontra:

- Universitárias
- Omegle +18
- Cornos
- Lésbicas
- Amadores
- Fetiches
- Milfs
- Boquetes
- Novinhas +18
- OnlyFans

...e muito mais! 👏

---

**PIX** | **100% Seguro** | **Entrega Imediata**

---

Escolha uma opção abaixo:
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    if user.id == ADMIN_ID:
        db.cursor.execute('UPDATE users SET is_admin = 1 WHERE user_id = ?', (user.id,))
        db.conn.commit()
    
    await update.message.reply_text(
        WELCOME_MESSAGE.format(name=user.first_name),
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    # Main menu options
    if data == "back_main":
        await query.edit_message_text(
            WELCOME_MESSAGE.format(name=query.from_user.first_name),
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        return
    
    if data == "back_subscribe":
        text, markup = await show_subscription(update, context)
        await query.edit_message_text(text, reply_markup=markup, parse_mode='Markdown')
        return
    
    # Subscription
    if data == "subscribe":
        text, markup = await show_subscription(update, context)
    elif data.startswith("plan_"):
        plan_key = data.replace("plan_", "")
        text, markup = await show_plan_details(update, context, plan_key)
    elif data == "packages":
        text, markup = await show_packages(update, context)
    elif data.startswith("package_"):
        package_key = data.replace("package_", "")
        text, markup = await show_package_details(update, context, package_key)
    elif data == "trials":
        text, markup = await show_trials(update, context)
    elif data.startswith("trial_"):
        trial_key = data.replace("trial_", "")
        text, markup = await show_trial_details(update, context, trial_key)
    elif data.startswith("confirm_"):
        plan_key = data.replace("confirm_", "")
        text, markup = await process_payment(update, context, plan_key, user_id)
    
    # Categories
    elif data == "categories":
        text, markup = await show_categories(update, context)
    elif data.startswith("category_"):
        category = data.replace("category_", "")
        text, markup = await show_category_content(update, context, category)
    
    # Account
    elif data == "my_account":
        text, markup = await show_account(update, context, user_id)
    elif data == "my_payments":
        text, markup = await show_payments(update, context, user_id)
    elif data == "my_products":
        text = """
📦 **MEUS PRODUTOS**

Você não possui produtos adquiridos ainda.

Assine um plano para acessar nosso conteúdo exclusivo!
"""
        markup = back_button()
    elif data == "coupons":
        text = """
🎫 **CUPONS**

Digite seu código de cupom para ganhar descontos!

*Em breve mais promoções!*
"""
        markup = back_button()
    elif data == "referral":
        text = f"""
👥 **INDIQUE AMIGOS**

Indique seus amigos e ganhe benefícios exclusivos!

🔗 Seu link: https://t.me/mimo_sinha_bot?start={user_id}

💰 Para cada amigo que assinar, você ganha 10% de crédito!
"""
        markup = back_button()
    elif data == "support":
        text = """
🆘 **SUPORTE**

📱 WhatsApp: +5511940462611
📧 Email: suporte@annynhafunny.com

💬 Atendimento humanizado!

Horário de atendimento:
Seg-Sex: 9h às 18h
Sáb: 10h às 15h
"""
        from keyboards import support_buttons
        markup = support_buttons()
    elif data == "faq":
        text = """
❓ **FAQ - Perguntas Frequentes**

**1. Como funciona?**
Escolha seu plano, faça o pagamento via PIX e receba acesso imediato.

**2. O conteúdo é liberado na hora?**
Sim! Após confirmação do pagamento, seu acesso é liberado automaticamente.

**3. Posso cancelar?**
Sim, você pode cancelar sua assinatura a qualquer momento.

**4. Como renovar?**
Sua assinatura é renovada automaticamente mensalmente.

**5. Os dados são seguros?**
Sim, utilizamos criptografia e não compartilhamos seus dados.

**6. Como funciona o trial?**
Teste grátis por 3 ou 7 dias com acesso limitado.
"""
        markup = back_button()
    elif data == "settings":
        text = """
⚙️ **CONFIGURAÇÕES**

Personalize sua experiência:
"""
        from keyboards import settings_buttons
        markup = settings_buttons()
    elif data.startswith("settings_"):
        if data == "settings_language":
            text = "🌐 **IDIOMA**\n\nSelecione seu idioma:\n🇧🇷 Português\n🇺🇸 English"
        elif data == "settings_notifications":
            text = "🔔 **NOTIFICAÇÕES**\n\nAtivar/Desativar notificações."
        elif data == "settings_privacy":
            text = "🔒 **PRIVACIDADE**\n\nGerencie suas configurações de privacidade."
        elif data == "settings_delete":
            text = "🗑️ **EXCLUIR MINHA CONTA**\n\nTem certeza? Esta ação é irreversível!"
        else:
            text = "⚙️ Configurações"
        markup = back_button()
    elif data == "recent_content":
        content = db.get_content()
        if not content:
            text = "🆕 **CONTEÚDO RECENTE**\n\nNenhum conteúdo disponível ainda."
        else:
            text = "🆕 **CONTEÚDO RECENTE**\n\n"
            for item in content[:5]:
                text += f"📌 {item[2]}\n"
                text += f"📂 {item[1]}\n"
                text += f"📅 {item[5]}\n\n"
        markup = back_button()
    elif data == "promotions":
        db.cursor.execute('SELECT * FROM promotions WHERE is_active = 1 AND valid_until >= date("now")')
        promotions = db.cursor.fetchall()
        
        if not promotions:
            text = "🎯 **PROMOÇÕES**\n\nNenhuma promoção ativa no momento.\nFique ligado para novidades!"
        else:
            text = "🎯 **PROMOÇÕES ATIVAS**\n\n"
            for promo in promotions:
                text += f"🔥 {promo[1]}\n"
                text += f"📝 {promo[2]}\n"
                text += f"🎫 Código: {promo[4]}\n"
                text += f"💰 Desconto: {promo[3]}%\n"
                text += f"📅 Válido até: {promo[5]}\n\n"
        markup = back_button()
    elif data == "email_support":
        text = f"""
📧 **Email de Suporte**

Envie seu email para: suporte@annynhafunny.com

Responderemos em até 24h!
"""
        markup = back_button()
    
    # Admin
    elif data == "admin_panel":
        if user_id == ADMIN_ID:
            text, markup = await show_admin_panel(update, context)
        else:
            text = "❌ Você não tem permissão para acessar esta área."
            markup = back_button()
    elif data.startswith("admin_"):
        if user_id == ADMIN_ID:
            text, markup = await handle_admin_action(update, context, data)
        else:
            text = "❌ Você não tem permissão para acessar esta área."
            markup = back_button()
    else:
        text = "Opção não reconhecida."
        markup = back_button()
    
    await query.edit_message_text(text, reply_markup=markup, parse_mode='Markdown')

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.lower() == "voltar":
        await update.message.reply_text(
            WELCOME_MESSAGE.format(name=update.effective_user.first_name),
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    print("🤖 Bot Mimo Sinha iniciado!")
    print("📱 Conectado ao bot @mimo_sinha_bot")
    print("🔄 Aguardando mensagens...")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()