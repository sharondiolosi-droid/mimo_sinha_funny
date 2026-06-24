import random
import string
from datetime import datetime

def generate_transaction_id():
    """Gera um ID de transação único"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def format_currency(amount):
    """Formata valor em moeda brasileira"""
    return f"R$ {amount:.2f}"

def get_current_date():
    """Retorna a data atual"""
    return datetime.now().date()

def calculate_discount(price, discount_percent):
    """Calcula o preço com desconto"""
    return price * (1 - discount_percent / 100)