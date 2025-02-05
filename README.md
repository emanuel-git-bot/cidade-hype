# Sistema de Administração - Cidade Hype

Sistema de administração e APIs para o jogo Cidade Hype, desenvolvido com Django e Django REST Framework.

## Funcionalidades

### 1. Loja (Store)
- Gerenciamento de categorias e itens
- Sistema de pedidos
- APIs para listagem e compra de itens

### 2. Eventos (Events)
- Gerenciamento de eventos da cidade
- Suporte a múltiplas imagens por evento
- APIs para listagem e detalhes de eventos

### 3. Atualizações (Updates)
- Gerenciamento de atualizações do jogo
- Sistema de "Em Breve" (conteúdos futuros)
- Suporte a múltiplas imagens
- APIs para listagem e detalhes

### 4. Bugs
- Sistema de reporte de bugs
- Gerenciamento de status (pendente/resolvido)
- Suporte a capturas de tela
- APIs para usuários e administradores

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd [NOME_DO_DIRETÓRIO]
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
cd backend
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

## Uso

1. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

2. Acesse:
- Painel administrativo: http://localhost:8000/admin/
- APIs: http://localhost:8000/api/

## Endpoints da API

### Store
- `GET /api/categories/`: Lista todas as categorias
- `GET /api/items/`: Lista todos os itens ativos
- `GET /api/items/?category=1`: Lista itens de uma categoria específica
- `POST /api/orders/`: Cria um novo pedido

### Events
- `GET /api/events/`: Lista todos os eventos
- `GET /api/events/{id}/`: Detalhes de um evento
- `POST /api/events/{id}/add_image/`: Adiciona imagem a um evento
- `POST /api/events/{id}/remove_image/`: Remove imagem de um evento
- `POST /api/events/{id}/reorder_images/`: Reordena imagens de um evento

### Updates
- `GET /api/updates/`: Lista todas as atualizações
- `GET /api/coming-soon/`: Lista todos os conteúdos futuros
- Endpoints similares aos eventos para gerenciamento de imagens

### Bugs
- `GET /api/bugs/`: Lista bugs (filtrados por status para usuários normais)
- `POST /api/bugs/`: Reporta um novo bug
- `POST /api/bugs/{id}/resolve/`: Marca um bug como resolvido (apenas admin)

## Segurança

- Autenticação via sessão para o painel administrativo
- APIs protegidas com autenticação quando necessário
- Uploads de arquivos limitados a 5MB
- Proteções contra XSS e CSRF ativadas
- CORS configurado para desenvolvimento local

## Produção

Para ambiente de produção:

1. Configure variáveis de ambiente sensíveis
2. Ative HTTPS
3. Configure um servidor web (nginx/apache)
4. Use gunicorn como servidor WSGI
5. Configure um banco de dados mais robusto (PostgreSQL recomendado)

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 