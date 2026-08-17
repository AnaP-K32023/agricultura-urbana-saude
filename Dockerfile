FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc g++ build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Força a instalação de versões prontas do numpy e pandas, evitando compilação
RUN pip install --no-cache-dir --only-binary=:all: numpy pandas
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "hortas_dash:app"]