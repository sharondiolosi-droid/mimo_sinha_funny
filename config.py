import os

# Use variáveis de ambiente no Railway
BOT_TOKEN = os.environ.get("BOT_TOKEN", "SEU_TOKEN_AQUI")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 8881712229))
PIX_KEY = os.environ.get("PIX_KEY", "(11)9.4046-2611")

# ... (suas categorias, planos, pacotes, trials permanecem iguais

# config.py - Configurações do bot
BOT_TOKEN = "8840039207:AAEuUFTayyACnskLZGmqxjgXdNjDE2snSPA"
ADMIN_ID = 8881712229

# Payment settings
PIX_KEY = "suporte@annynhafunny.com"

# Categories
CATEGORIES = [
    "Universitárias",
    "Cornos",
    "Amadores",
    "Milfs",
    "Novinhas +18",
    "Instagram +18",
    "Câmeras Ocultas",
    "Coroas",
    "Casadas",
    "Lives +18",
    "Família Sacana",
    "Omegle +18",
    "Lésbicas",
    "Fetiches",
    "Boquetes",
    "OnlyFans",
    "Vazadas",
    "Asiáticas",
    "Surubas",
    "Anal"
]

# Plans with prices
PLANS = {
    "fan": {"name": "FAN", "price": 29.90, "period": "mês", "features": ["Conteúdo exclusivo semanal", "Acesso ao Canal FAN"]},
    "vip": {"name": "VIP", "price": 79.90, "period": "mês", "features": ["Conteúdo premium 3x semana", "2 modelos + Canal VIP"]},
    "prive": {"name": "PRIVÊ", "price": 299.90, "period": "mês", "features": ["Interação direta + Lives exclusivas", "3 modelos + Grupo PRIVÊ"]},
    "diamond": {"name": "DIAMOND", "price": 499.90, "period": "mês", "features": ["Experiência VIP total", "Todas as modelos + 1:1"]},
    "vitalicio": {"name": "VITALÍCIO", "price": 1999.90, "period": "", "features": ["Acesso ilimitado para sempre!"]}
}

# Special packages
PACKAGES = {
    "duo": {"name": "DUO", "price": 119.90, "description": "2 modelos VIP"},
    "trio": {"name": "TRIO", "price": 179.90, "description": "3 modelos VIP"},
    "quinteto": {"name": "QUINTETO", "price": 299.90, "description": "5 modelos VIP"},
    "prive_completo": {"name": "PRIVÊ COMPLETO", "price": 1199.90, "description": "Tudo incluído"}
}

# Trial periods
TRIALS = {
    "3_dias": {"name": "Plano 3 Dias", "days": 3},
    "7_dias": {"name": "Plano 7 Dias", "days": 7}
}