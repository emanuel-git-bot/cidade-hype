#!/usr/bin/env bash
# exit on error
set -o errexit

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Entrar no diretório do backend
cd backend

# Instalar dependências específicas do backend (se houver)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Criar diretório para arquivos estáticos
mkdir -p static

# Coletar arquivos estáticos e aplicar migrações
python manage.py collectstatic --no-input
python manage.py migrate 