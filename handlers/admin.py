from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import admin_buttons, back_button

db = Database()

async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o painel administrativo"""
    # Get stats
    db.cursor.execute('SELECT COUNT(*) FROM users')
    total_users = db.cursor.fetchone()[0]
    
    db.cursor.execute('SELECT COUNT(*) FROM subscriptions WHERE status = "active"')
    active_subs = db.cursor.fetchone()[0]
    
    db.cursor.execute('SELECT SUM(amount) FROM payments WHERE status = "completed"')
    total_revenue = db.cursor.fetchone()[0] or 0
    
    text = f"""
👑 **PAINEL ADMINISTRATIVO**

Bem-vindo, Admin!

📊 **Dashboard**

👥 Total de Usuários: {total_users}
📋 Assinaturas Ativas: {active_subs}
💰 Receita Total: R$ {total_revenue:.2f}

---

Selecione uma opção abaixo:
"""
    return text, admin_buttons()

async def handle_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str):
    """Gerencia ações administrativas"""
    actions = {
        "admin_dashboard": "📊 **DASHBOARD**\n\nEstatísticas detalhadas do sistema.",
        "admin_users": "👥 **USUÁRIOS**\n\nLista de usuários cadastrados.",
        "admin_subscriptions": "📋 **ASSINATURAS**\n\nGerenciar assinaturas ativas.",
        "admin_orders": "📦 **PEDIDOS**\n\nGerenciar pedidos realizados.",
        "admin_pending": "⏳ **PENDENTES**\n\nPagamentos aguardando confirmação.",
        "admin_coupons": "🎫 **CUPONS**\n\nGerenciar cupons de desconto.",
        "admin_broadcast": "📢 **BROADCAST**\n\nEnviar mensagem para todos os usuários.",
        "admin_analytics": "📈 **ANALYTICS**\n\nEstatísticas e análises do sistema.",
        "admin_logs": "📝 **LOGS**\n\nRegistro de atividades do sistema.",
        "admin_promotions": "🎯 **PROMOÇÕES**\n\nGerenciar promoções ativas.",
        "admin_models": "👩 **MODELOS**\n\nGerenciar modelos cadastradas.",
        "admin_backup": "💾 **BACKUP**\n\nRealizar backup do sistema.",
        "admin_config": "⚙️ **CONFIG**\n\nConfigurações do sistema."
    }
    
    text = actions.get(action, "Área administrativa")
    return text, back_button()