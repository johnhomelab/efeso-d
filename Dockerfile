# 1. Base da imagem: Python leve e rápido
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# 2. Instala dependências do sistema para o Postgres
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# 3. Define a pasta de trabalho
WORKDIR /app

# 4. Instala as bibliotecas do Django
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o seu código para dentro da imagem
COPY . .
EXPOSE 8000
# 6. Comando para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
