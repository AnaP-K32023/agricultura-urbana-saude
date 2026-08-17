FROM python:3.11-slim

# Instala as ferramentas de compilação C (indispensáveis para o pandas)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho
WORKDIR /app

# Instala dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do seu app
COPY . .

# Comando para iniciar o app (seu arquivo principal se chama hortas_dash.py, então é isso)
CMD ["gunicorn", "hortas_dash:app"]