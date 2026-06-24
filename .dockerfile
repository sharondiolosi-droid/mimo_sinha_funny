FROM python:3.11-slim

WORKDIR /app

# Copia e instala dependências primeiro (melhor para cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Comando para iniciar o bot
CMD ["python", "bot.py"]