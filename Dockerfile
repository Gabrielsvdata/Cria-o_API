# Usa imagem base com Python
FROM python:3.11-slim

# Instala bibliotecas do sistema necessárias para o mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia as dependências primeiro (aproveita cache)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Define a variável de ambiente para o Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expõe a porta usada pela aplicação Flask
EXPOSE 5000

# Comando que inicia a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
