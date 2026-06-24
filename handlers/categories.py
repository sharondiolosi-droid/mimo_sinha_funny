from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import category_buttons, back_button

db = Database()

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra lista de categorias"""
    text = """
📂 **CATEGORIAS DE CONTEÚDO**

🔥 Explore nosso acervo exclusivo:
*Clique em uma categoria para ver os planos*
"""
    return text, category_buttons()

async def show_category_content(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Mostra conteúdo de uma categoria específica"""
    content = db.get_content(category)
    
    if not content:
        text = f"""
📁 **{category}**

❌ Nenhum conteúdo disponível nesta categoria ainda.

Novidades em breve! 🔥
"""
    else:
        text = f"📁 **{category}**\n\n"
        for item in content:
            text += f"📌 {item[2]}\n"
            text += f"{item[3]}\n\n"
    
    return text, back_button()