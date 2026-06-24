from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from config import PLANS, PACKAGES, TRIALS, PIX_KEY
from keyboards import back_button
from utils.helpers import generate_transaction_id
from datetime import datetime

db = Database()

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, plan_key: str, user_id: int):
    """Processa o pagamento de um plano"""
    transaction_id = generate_transaction_id()
    
    # Get plan/package/trial details
    if plan_key in PLANS:
        amount = PLANS[plan_key]['price']
        name = PLANS[plan_key]['name']
    elif plan_key in PACKAGES:
        amount = PACKAGES[plan_key]['price']
        name = PACKAGES[plan_key]['name']
    elif plan_key in TRIALS:
        amount = 0
        name = TRIALS[plan_key]['name']
    else:
        amount = 0
        name = "Desconhecido"
    
    # Save payment record
    db.cursor.execute('''
        INSERT INTO payments (user_id, transaction_id, amount, method, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, transaction_id, amount, "PIX", "pending", datetime.now().date()))
    db.conn.commit()
    
    if amount == 0:
        # Free trial - activate immediately
        if plan_key in TRIALS:
            days = TRIALS[plan_key]['days']
            db.update_subscription(user_id, f"trial_{plan_key}", days)
            db.cursor.execute('''
                UPDATE payments SET status = "completed"
                WHERE transaction_id = ?
            ''', (transaction_id,))
            db.conn.commit()
            
            text = f"""
✅ **TRIAL ATIVADO COM SUCESSO!**

🎉 Seu {name} foi ativado!
📅 Acesso por {days} dias.

Aproveite todo o conteúdo exclusivo! 🔥
"""
            return text, back_button()
    else:
        # Show PIX payment details
        text = f"""
💳 **PAGAMENTO PENDENTE**

📝 Transação: {transaction_id}
💰 Valor: R$ {amount:.2f}
📦 Plano: {name}

**Pagamento via PIX**
Chave: {PIX_KEY}

⚠️ Após realizar o pagamento, envie o comprovante para:
📱 WhatsApp: +5511940462611
📧 Email: sharondiolosi@gmail.com

Seu acesso será liberado em até 30 minutos após a confirmação.
"""
        return text, back_button()
    
    return "Erro ao processar pagamento.", back_button()