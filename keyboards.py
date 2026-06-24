from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CATEGORIES, PLANS, PACKAGES, TRIALS

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

def plan_buttons():
    keyboard = [
        [InlineKeyboardButton(f"📱 FAN — R$ {PLANS['fan']['price']:.2f}/mês", callback_data="plan_fan")],
        [InlineKeyboardButton(f"⭐ VIP — R$ {PLANS['vip']['price']:.2f}/mês", callback_data="plan_vip")],
        [InlineKeyboardButton(f"🔒 PRIVÊ — R$ {PLANS['prive']['price']:.2f}/mês", callback_data="plan_prive")],
        [InlineKeyboardButton(f"💎 DIAMOND — R$ {PLANS['diamond']['price']:.2f}/mês", callback_data="plan_diamond")],
        [InlineKeyboardButton(f"∞ VITALÍCIO — R$ {PLANS['vitalicio']['price']:.2f}", callback_data="plan_vitalicio")],
        [InlineKeyboardButton("📦 Pacotes Especiais", callback_data="packages")],
        [InlineKeyboardButton("🔄 Planos Trial", callback_data="trials")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def package_buttons():
    keyboard = [
        [InlineKeyboardButton(f"DUO — R$ {PACKAGES['duo']['price']:.2f}", callback_data="package_duo")],
        [InlineKeyboardButton(f"TRIO — R$ {PACKAGES['trio']['price']:.2f}", callback_data="package_trio")],
        [InlineKeyboardButton(f"QUINTETO — R$ {PACKAGES['quinteto']['price']:.2f}", callback_data="package_quinteto")],
        [InlineKeyboardButton(f"PRIVÊ COMPLETO — R$ {PACKAGES['prive_completo']['price']:.2f}", callback_data="package_prive_completo")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_subscribe")]
    ]
    return InlineKeyboardMarkup(keyboard)

def trial_buttons():
    keyboard = [
        [InlineKeyboardButton(f"🔄 {TRIALS['3_dias']['name']}", callback_data="trial_3_dias")],
        [InlineKeyboardButton(f"🔄 {TRIALS['7_dias']['name']}", callback_data="trial_7_dias")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_subscribe")]
    ]
    return InlineKeyboardMarkup(keyboard)

def category_buttons():
    keyboard = []
    for cat in CATEGORIES:
        keyboard.append([InlineKeyboardButton(f"📁 {cat}", callback_data=f"category_{cat}")])
    keyboard.append([InlineKeyboardButton("🔙 Voltar", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)

def confirm_payment_buttons(plan):
    keyboard = [
        [InlineKeyboardButton("✅ Confirmar Pagamento", callback_data=f"confirm_{plan}")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_subscribe")]
    ]
    return InlineKeyboardMarkup(keyboard)

def settings_buttons():
    keyboard = [
        [InlineKeyboardButton("🌐 Idioma", callback_data="settings_language")],
        [InlineKeyboardButton("🔔 Notificações", callback_data="settings_notifications")],
        [InlineKeyboardButton("🔒 Privacidade", callback_data="settings_privacy")],
        [InlineKeyboardButton("🗑️ Excluir Minha Conta", callback_data="settings_delete")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_buttons():
    keyboard = [
        [InlineKeyboardButton("📊 Dashboard", callback_data="admin_dashboard")],
        [InlineKeyboardButton("👥 Usuários", callback_data="admin_users")],
        [InlineKeyboardButton("📋 Assinaturas", callback_data="admin_subscriptions")],
        [InlineKeyboardButton("📦 Pedidos", callback_data="admin_orders")],
        [InlineKeyboardButton("⏳ Pendentes", callback_data="admin_pending")],
        [InlineKeyboardButton("🎫 Cupons", callback_data="admin_coupons")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        [InlineKeyboardButton("📈 Analytics", callback_data="admin_analytics")],
        [InlineKeyboardButton("📝 Logs", callback_data="admin_logs")],
        [InlineKeyboardButton("🎯 Promoções", callback_data="admin_promotions")],
        [InlineKeyboardButton("👩 Modelos", callback_data="admin_models")],
        [InlineKeyboardButton("💾 Backup", callback_data="admin_backup")],
        [InlineKeyboardButton("⚙️ Config", callback_data="admin_config")],
        [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data="back_main")]])

def support_buttons():
    keyboard = [
        [InlineKeyboardButton("📱 WhatsApp", url="https://wa.me/5511940462611")],
        [InlineKeyboardButton("📧 Email", callback_data="sharondiolosi@gmail.com")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)