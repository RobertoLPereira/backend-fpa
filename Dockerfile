# 1. Usa uma imagem oficial leve do Python baseada em Alpine/Debian Slim
FROM python:3.12-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Evita que o Python escreva arquivos .pyc no disco e bufferiza os logs do terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 4. Instala dependências do sistema operacional necessárias para o SQLite e compilações de pacotes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia primeiro apenas o arquivo de dependências para aproveitar o cache do Docker
COPY requirements.txt .

# 6. Instala as bibliotecas do Python (FastAPI, Uvicorn, Pydantic, etc.)
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 7. Copia todo o código-fonte da pasta src para dentro do container
COPY ./src ./src

# 8. Copia o arquivo do banco de dados para a raiz do container
COPY fpa.db .

# 9. Cria a pasta de backups dentro do container e concede permissões de escrita
RUN mkdir -p backups

# 10. Expõe a porta padrão que o FastAPI usará na nuvem
EXPOSE 8000

# 11. Comando definitivo para iniciar o Uvicorn em produção (sem o parâmetro --reload)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
