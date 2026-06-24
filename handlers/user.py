from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import main_menu, back_button

db = Database()

async def show_account(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Mostra informações da conta do usuário"""
    user = db.get_user(user_id)
    if not user:
        text = "❌ Usuário não encontrado."
    else:
        text = f"""
👤 **MINHA CONTA**

📝 Nome: {user[2] or user[1] or 'N/A'}
🆔 ID: {user[0]}
📅 Criado em: {user[5]}

🔒 **Assinatura:**
Plano: {user[3] or 'Nenhum'}
Válido até: {user[4] or 'N/A'}
Status: {'✅ Ativo' if db.check_subscription(user[0]) else '❌ Inativo'}
"""
    return text, back_button()

async def show_payments(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Mostra histórico de pagamentos do usuário"""
    db.cursor.execute('SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    payments = db.cursor.fetchall()
    
    if not payments:
        text = "💳 **MEUS PAGAMENTOS**\n\nNenhum pagamento registrado ainda."
    else:
        text = "💳 **MEUS PAGAMENTOS**\n\n"
        for payment in payments:
            text += f"🆔 {payment[2]}\n"
            text += f"💰 R$ {payment[3]:.2f}\n"
            text += f"📅 {payment[5]}\n"
            text += f"Status: {payment[4]}\n\n"
    
    return text, back_button()