from telegram import Update
from telegram.ext import ContextTypes
from config import PLANS, PACKAGES, TRIALS, PIX_KEY
from keyboards import plan_buttons, package_buttons, trial_buttons, confirm_payment_buttons, back_button

async def show_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra planos de assinatura"""
    text = """
📋 **ASSINAR — ESCOLHA SEU PLANO**

**FAN** — R$ 29,90/mês
- Conteúdo exclusivo semanal
- Acesso ao Canal FAN

**VIP** — R$ 79,90/mês
- Conteúdo premium 3x semana
- 2 modelos + Canal VIP

**PRIVÊ** — R$ 299,90/mês
- Interação direta + Lives exclusivas
- 3 modelos + Grupo PRIVÊ

**DIAMOND** — R$ 499,90/mês
- Experiência VIP total
- Todas as modelos + 1:1

**VITALÍCIO** — R$ 1.999,90
- Acesso ilimitado para sempre!

---

**Pacotes Especiais:**
- DUO: R$ 119,90
- TRIO: R$ 179,90
- QUINTETO: R$ 299,90
- PRIVÊ COMPLETO: R$ 1.199,90
"""
    return text, plan_buttons()

async def show_plan_details(update: Update, context: ContextTypes.DEFAULT_TYPE, plan_key: str):
    """Mostra detalhes de um plano específico"""
    plan = PLANS.get(plan_key)
    if not plan:
        return "Plano não encontrado.", back_button()
    
    features = "\n".join([f"✅ {f}" for f in plan['features']])
    text = f"""
⭐ **{plan['name'].upper()}** — R$ {plan['price']:.2f}/{plan['period']}

**Benefícios:**
{features}

💳 **Pagamento via PIX**
Chave: {PIX_KEY}

⚠️ Após o pagamento, clique em "Confirmar Pagamento" e aguarde a liberação.
"""
    return text, confirm_payment_buttons(plan_key)

async def show_packages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra pacotes especiais"""
    text = """
📦 **Pacotes Especiais**

**DUO** — R$ 119,90
2 modelos VIP

**TRIO** — R$ 179,90
3 modelos VIP

**QUINTETO** — R$ 299,90
5 modelos VIP

**PRIVÊ COMPLETO** — R$ 1.199,90
Tudo incluído!
"""
    return text, package_buttons()

async def show_package_details(update: Update, context: ContextTypes.DEFAULT_TYPE, package_key: str):
    """Mostra detalhes de um pacote específico"""
    package = PACKAGES.get(package_key)
    if not package:
        return "Pacote não encontrado.", back_button()
    
    text = f"""
📦 **{package['name'].upper()}** — R$ {package['price']:.2f}

{package['description']}

💳 **Pagamento via PIX**
Chave: {PIX_KEY}

⚠️ Após o pagamento, clique em "Confirmar Pagamento".
"""
    return text, confirm_payment_buttons(package_key)

async def show_trials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra planos trial"""
    text = """
🔄 **Planos Trial**

**Plano 3 Dias** - Grátis
**Plano 7 Dias** - Grátis

Aproveite para conhecer nosso conteúdo!
"""
    return text, trial_buttons()

async def show_trial_details(update: Update, context: ContextTypes.DEFAULT_TYPE, trial_key: str):
    """Mostra detalhes de um plano trial"""
    trial = TRIALS.get(trial_key)
    if not trial:
        return "Trial não encontrado.", back_button()
    
    text = f"""
🔄 **{trial['name']}** — Grátis!

Acesso por {trial['days']} dias ao conteúdo exclusivo.

💳 **100% gratuito!**

Clique em "Confirmar" para ativar seu trial.
"""
    return text, confirm_payment_buttons(trial_key)