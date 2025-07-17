FROM python:3.12-alpine

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
# Esta etapa é separada para aproveitar o cache do Docker. As dependências só
# serão reinstaladas se o arquivo requirements.txt mudar.
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação usando Uvicorn
# O host 0.0.0.0 torna a aplicação acessível de fora do container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]