import os
import sys

# Adicionar o diretório backend ao path do Python
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(backend_path)

# Importar a aplicação WSGI do Django
from backend.wsgi import application 