# Kogui — README

## Visão Geral
Aplicação para listar Pokémons consumindo a PokéAPI via backend centralizado. Usuários podem marcar Pokémons como favoritos e montar uma equipe de batalha com até seis integrantes. Projeto pensado para frontend em Angular e backend em Python (Flask ou Django), com persistência local em SQLite.

## Funcionalidades Principais
- Listagem de Pokémons em cards interativos.
- Marcar/desmarcar favoritos.
- Selecionar até seis Pokémons para o Grupo de Batalha.
- Visualização dos estados (favorito / em grupo) na listagem.
- Autenticação via token JWT.
- Integração com PokéAPI feita exclusivamente pelo backend.

## Tecnologias
- Frontend: Angular
- Backend: Python (Flask ou Django)
- Banco de dados: SQLite
- ORM: SQLAlchemy (Flask) ou Django ORM
- Autenticação: JWT
- API externa: PokéAPI (https://pokeapi.co/)

## Modelagem (resumo)
Entidades principais:
- Usuario
    - IDUsuario (PK), Nome, Login, Email, Senha (hash), DataNascimento, DataUltimoAcesso
- Pokémon
    - IDPokémon (PK), Nome, Descrição, Tipo1ID (FK → TipoPokémon), Tipo2ID (FK, opcional), Geração, Número
- TipoPokémon
    - IDTipoPokémon (PK), Descrição, Fraquezas
- PokémonUsuario (associação com atributos)
    - IDPokémonUsuario (PK), IDUsuario (FK), IDPokémon (FK), Nome (opcional), Descrição (opcional), Itens (lista/JSON), DataFavorito, IsFavorito (boolean), EmGrupoDeBatalha (boolean), PosicaoNoGrupo (opcional)

Relações:
- Usuario 1:N PokémonUsuario
- Pokémon 1:N PokémonUsuario
- TipoPokémon 1:N Pokémon (via Tipo1ID / Tipo2ID)

Observação: PokémonUsuario modela a relação entre usuários e pokémons, permitindo atributos adicionais (favorito, posição no grupo, itens etc.). Para suportar equipes avançadas, pode-se adicionar entidade GrupoDeBatalha e referenciar PokémonUsuario.

## Requisitos Mínimos (obrigatórios)
1. Seguir a modelagem proposta.
2. Frontend em Angular.
3. Backend em Python (Flask ou Django).
4. Integração com PokéAPI centralizada no backend.
5. Banco local SQLite usando SQLAlchemy ou Django ORM.
6. Autenticação via JWT.
7. Documentar a API e rotas principais.

## Requisitos Opcionais (diferenciais)
- Dockerfile / docker-compose para a API.
- Painel para reset de senha.
- Painel de gestão de usuários.

## Recomendações de implementação
- Centralizar chamadas à PokéAPI no backend para controle de cache e consistência.
- Armazenar referências essenciais (ID, nomes) localmente e enriquecer com dados da PokéAPI quando necessário.
- Tratar limite de seis membros na camada de domínio (backend) e na UI (frontend).
- Hashear senhas (bcrypt/Argon2) e configurar expiração/refresh de tokens JWT.
- Usar migrations (Flask-Migrate ou Django migrations) para gerir o schema do SQLite.

## Exemplo de endpoints (sugestão)
- POST /auth/login — autenticação (retorna JWT)
- POST /auth/register — criar usuário
- GET /pokemons — listagem (paginação / filtros)
- GET /pokemons/:id — detalhes
- POST /users/:id/pokemons — adicionar Pokémon ao usuário (favorito / itens)
- PATCH /users/:id/pokemons/:relId — marcar favorito / definir em grupo
- GET /users/:id/team — obter equipe de batalha do usuário

## Como começar (exemplo rápido)
1. Clonar repositório.
2. Criar virtualenv e instalar dependências (backend).
3. Configurar variáveis de ambiente (ex.: SECRET_KEY, DATABASE_URL, JWT_SECRET).
4. Executar migrations e iniciar servidor (Flask/Django).
5. Iniciar frontend Angular, apontando API para backend.

## Referências
- PokéAPI: https://pokeapi.co/docs/v2

Licença: adicionar conforme projeto (ex.: MIT).

# Guia Completo para Construção do App Kogui

Vou te guiar passo a passo na construção deste projeto, desde a escolha da plataforma até o deployment final.

## 🎯 Escolha da Plataforma de Desenvolvimento

### Opções Recomendadas:

**1. VS Code Local (Recomendado para iniciantes/intermediários)**
- ✅ Melhor performance
- ✅ Controle total do ambiente
- ✅ Funciona offline após setup
- ✅ Integração perfeita com Git

**2. GitHub Codespaces (Recomendado para este projeto)**
- ✅ Ambiente pré-configurado
- ✅ Acesso de qualquer lugar
- ✅ Já vem com Python, Node.js, Git
- ✅ 60 horas gratuitas/mês
- ⚠️ Requer internet estável

**3. GitPod**
- Similar ao Codespaces
- 50 horas gratuitas/mês

**Minha Recomendação:** Use **GitHub Codespaces** para este projeto pela praticidade, ou **VS Code Local** se tiver uma máquina boa.

---

## 📋 ROTEIRO COMPLETO DE DESENVOLVIMENTO

### **FASE 1: Preparação do Ambiente (Dia 1)**

#### Passo 1.1: Configurar Repositório GitHub
```bash
# Criar repositório no GitHub:
# - Nome: kogui-pokemon-app
# - Descrição: "App de gestão de Pokémons com Angular + Flask"
# - Adicionar .gitignore (Python, Node)
# - Adicionar README
```

#### Passo 1.2: Iniciar Codespace
1. Acesse seu repositório no GitHub
2. Clique em "Code" → "Codespaces" → "Create codespace on main"
3. Aguarde o ambiente carregar

#### Passo 1.3: Estruturar o Projeto
```bash
# No terminal do Codespace:
mkdir kogui-pokemon-app
cd kogui-pokemon-app

# Criar estrutura de pastas
mkdir backend frontend docs

# Estrutura final:
# kogui-pokemon-app/
# ├── backend/          # API Flask
# ├── frontend/         # Angular
# ├── docs/             # Documentação
# ├── docker-compose.yml
# └── README.md
```

---

### **FASE 2: Desenvolvimento do Backend (Dias 2-5)**

#### Passo 2.1: Configurar Backend Flask
```bash
cd backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Criar requirements.txt
cat > requirements.txt << EOF
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-JWT-Extended==4.6.0
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
bcrypt==4.1.2
EOF

# Instalar dependências
pip install -r requirements.txt
```

#### Passo 2.2: Criar Estrutura do Backend
```bash
# Dentro de backend/
mkdir app
cd app

# Criar estrutura modular
mkdir models routes services utils
touch __init__.py config.py

# Estrutura:
# backend/
# ├── app/
# │   ├── __init__.py
# │   ├── config.py
# │   ├── models/
# │   │   ├── __init__.py
# │   │   ├── usuario.py
# │   │   ├── pokemon.py
# │   │   ├── tipo_pokemon.py
# │   │   └── pokemon_usuario.py
# │   ├── routes/
# │   │   ├── __init__.py
# │   │   ├── auth.py
# │   │   ├── pokemon.py
# │   │   └── user.py
# │   ├── services/
# │   │   ├── __init__.py
# │   │   ├── pokeapi_service.py
# │   │   └── auth_service.py
# │   └── utils/
# │       ├── __init__.py
# │       └── decorators.py
# ├── migrations/
# ├── tests/
# ├── run.py
# ├── requirements.txt
# └── .env
```

#### Passo 2.3: Implementar Modelos (models/)

**Ordem de implementação:**
1. `tipo_pokemon.py` (sem dependências)
2. `pokemon.py` (depende de TipoPokemon)
3. `usuario.py` (independente)
4. `pokemon_usuario.py` (depende de Usuario e Pokemon)

#### Passo 2.4: Implementar Serviços

**services/pokeapi_service.py:**
- Função para buscar lista de Pokémons
- Função para buscar detalhes de um Pokémon
- Sistema de cache para evitar chamadas repetidas

**services/auth_service.py:**
- Geração de tokens JWT
- Validação de tokens
- Hash de senhas

#### Passo 2.5: Criar Rotas (routes/)

**Ordem de implementação:**
1. `auth.py` - Login e registro
2. `pokemon.py` - CRUD de Pokémons
3. `user.py` - Gerenciamento de usuários e equipes

#### Passo 2.6: Configurar Migrations
```bash
# No diretório backend/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### Passo 2.7: Testar Backend
```bash
# Criar arquivo run.py
python run.py

# Testar endpoints com curl ou Postman:
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","login":"teste","email":"teste@email.com","senha":"123456"}'
```

---

### **FASE 3: Desenvolvimento do Frontend (Dias 6-9)**

#### Passo 3.1: Criar Projeto Angular
```bash
cd ../frontend

# Instalar Angular CLI (se necessário)
npm install -g @angular/cli

# Criar projeto
ng new kogui-frontend --routing --style=scss
cd kogui-frontend

# Instalar dependências adicionais
npm install @angular/material @angular/cdk
npm install jwt-decode
```

#### Passo 3.2: Estruturar o Frontend
```bash
# Criar módulos e componentes
ng generate module core
ng generate module shared
ng generate module features

# Componentes principais
ng generate component features/pokemon-list
ng generate component features/pokemon-card
ng generate component features/pokemon-detail
ng generate component features/battle-team
ng generate component features/login
ng generate component features/register

# Services
ng generate service core/services/pokemon
ng generate service core/services/auth
ng generate service core/services/user

# Guards
ng generate guard core/guards/auth

# Interceptors
ng generate interceptor core/interceptors/auth
```

#### Passo 3.3: Implementar Serviços

**Ordem de implementação:**
1. `auth.service.ts` - Autenticação e gerenciamento de token
2. `pokemon.service.ts` - Comunicação com API de Pokémons
3. `user.service.ts` - Gerenciamento de favoritos e equipe

#### Passo 3.4: Implementar Componentes

**Ordem de desenvolvimento:**
1. Login/Register (autenticação básica)
2. Pokemon List (listagem principal)
3. Pokemon Card (card individual)
4. Pokemon Detail (detalhes completos)
5. Battle Team (visualização da equipe)

#### Passo 3.5: Configurar Rotas
```typescript
// app-routing.module.ts
const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { 
    path: '', 
    canActivate: [AuthGuard],
    children: [
      { path: 'pokemons', component: PokemonListComponent },
      { path: 'pokemons/:id', component: PokemonDetailComponent },
      { path: 'team', component: BattleTeamComponent },
      { path: '', redirectTo: '/pokemons', pathMatch: 'full' }
    ]
  }
];
```

---

### **FASE 4: Integração e Testes (Dias 10-11)**

#### Passo 4.1: Conectar Frontend ao Backend
```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000'
};
```

#### Passo 4.2: Testar Fluxos Completos
1. Registro de usuário
2. Login e recebimento de token
3. Listagem de Pokémons
4. Adicionar aos favoritos
5. Montar equipe de batalha
6. Visualizar detalhes

#### Passo 4.3: Testes Unitários (Opcional mas recomendado)
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend/kogui-frontend
ng test
```

---

### **FASE 5: Docker e Deploy (Dia 12)**

#### Passo 5.1: Criar Dockerfiles

**backend/Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

**frontend/Dockerfile:**
```dockerfile
FROM node:18 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist/kogui-frontend /usr/share/nginx/html
EXPOSE 80
```

#### Passo 5.2: Criar docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "4200:80"
    depends_on:
      - backend
```

#### Passo 5.3: Testar com Docker
```bash
docker-compose up --build
```

---

## 🎨 ORDEM DE PRIORIDADE DE FEATURES

### MVP (Mínimo Viável) - Semana 1
1. ✅ Autenticação (login/registro)
2. ✅ Listagem de Pokémons
3. ✅ Adicionar/remover favoritos
4. ✅ Montar equipe básica (até 6)

### Features Intermediárias - Semana 2
5. ✅ Detalhes do Pokémon
6. ✅ Filtros e busca
7. ✅ Paginação
8. ✅ Persistência de itens

### Features Avançadas - Semana 3
9. ✅ Reset de senha
10. ✅ Painel admin
11. ✅ Docker
12. ✅ Documentação da API

---

## 📚 CHECKLIST DE DESENVOLVIMENTO

### Backend
- [ ] Configurar ambiente virtual
- [ ] Criar modelos de dados
- [ ] Implementar autenticação JWT
- [ ] Criar endpoints da API
- [ ] Integrar com PokéAPI
- [ ] Configurar CORS
- [ ] Implementar migrations
- [ ] Adicionar validações
- [ ] Criar documentação da API
- [ ] Testes unitários

### Frontend
- [ ] Criar projeto Angular
- [ ] Configurar Material Design
- [ ] Implementar serviços HTTP
- [ ] Criar componentes principais
- [ ] Implementar guards e interceptors
- [ ] Adicionar formulários reativos
- [ ] Estilizar com SCSS
- [ ] Responsividade mobile
- [ ] Tratamento de erros
- [ ] Loading states

### DevOps
- [ ] Criar Dockerfiles
- [ ] Configurar docker-compose
- [ ] Variáveis de ambiente
- [ ] Scripts de deploy
- [ ] CI/CD (opcional)

---

## 🛠️ COMANDOS ÚTEIS

### Backend
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Rodar servidor
python run.py

# Criar migration
flask db migrate -m "descrição"

# Aplicar migration
flask db upgrade

# Criar usuário admin (script customizado)
python scripts/create_admin.py
```

### Frontend
```bash
# Instalar dependências
npm install

# Servidor de desenvolvimento
ng serve

# Build de produção
ng build --prod

# Testes
ng test

# Gerar componente
ng g c nome-componente
```

---

## 📖 RECURSOS DE APRENDIZADO

1. **Flask:** https://flask.palletsprojects.com/
2. **Angular:** https://angular.io/docs
3. **SQLAlchemy:** https://docs.sqlalchemy.org/
4. **JWT:** https://jwt.io/introduction
5. **PokéAPI:** https://pokeapi.co/docs/v2

---

## ⚡ DICAS PRO

1. **Commit frequente:** Faça commits pequenos e descritivos
2. **Branch strategy:** Use branches para features (`feature/nome-feature`)
3. **Code review:** Revise seu próprio código antes de mergear
4. **Documentação:** Documente enquanto desenvolve, não depois
5. **Testes:** Escreva testes para funcionalidades críticas
6. **Performance:** Use cache para chamadas à PokéAPI
7. **Segurança:** Nunca commite senhas ou tokens no Git

---

## 🚀 PRÓXIMOS PASSOS

1. Escolha entre VS Code Local ou GitHub Codespaces
2. Clone/crie o repositório
3. Comece pela FASE 1
4. Siga o roteiro sequencialmente
5. Teste cada fase antes de avançar

Quer que eu detalhe alguma fase específica ou precisa de ajuda para começar?

Perfeito 🚀. Juntei o que está no **Kogui.txt** e no **README.md** e montei um **guia detalhado e completo** com as etapas para você desenvolver o app, incluindo qual ambiente usar (VS Code, Codespaces, etc.).

---

# 📌 Etapas para Desenvolver o Kogui App

## 1. Preparação do Ambiente

### Escolha da plataforma:

* **Visual Studio Code (VS Code)** ✅ (recomendado):

  * Melhor suporte para Angular + Python.
  * Extensões de linting, debugging, SQLite, Docker etc.
* **GitHub Codespaces** 🌐:

  * Bom se quiser tudo pronto na nuvem, mas depende de internet estável e pode ter custo.
* **IntelliJ/PyCharm**:

  * Excelente para Python (Flask/Django), mas pior suporte para Angular.
    👉 Melhor custo-benefício: **VS Code local + Docker (opcional)**.

### Instalações necessárias:

* **Node.js (LTS)** → para rodar Angular.
* **Angular CLI** (`npm install -g @angular/cli`).
* **Python 3.10+**.
* **SQLite** (já vem embutido em Python, mas instale cliente CLI).
* **Flask + SQLAlchemy + Flask-JWT-Extended** ou **Django + Django REST Framework + djangorestframework-simplejwt**.
* **Postman/Insomnia** → testar APIs.

---

## 2. Organização do Projeto

Estrutura sugerida:

```
kogui/
 ├── backend/       # Flask ou Django
 │   ├── app/       
 │   ├── models/
 │   ├── routes/
 │   ├── migrations/
 │   ├── tests/
 │   └── requirements.txt
 ├── frontend/      # Angular
 │   ├── src/
 │   ├── app/
 │   ├── environments/
 │   └── package.json
 ├── docker-compose.yml   (opcional)
 └── README.md
```

---

## 3. Backend (Python)

### 3.1 Estrutura de Dados

Seguir a modelagem:

* **Usuario**: credenciais e dados pessoais.
* **Pokémon**: dados básicos e tipos.
* **TipoPokémon**: tabela de referência (fogo, água, etc.).
* **PokémonUsuario**: relação entre usuário e Pokémon (favorito, em equipe etc.).

### 3.2 Passos

1. Criar ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Instalar dependências (exemplo Flask):

   ```bash
   pip install flask flask_sqlalchemy flask_migrate flask-jwt-extended requests bcrypt
   ```

3. Configurar banco SQLite no `config.py`.

4. Criar modelos (SQLAlchemy ou Django ORM).

5. Configurar autenticação JWT.

6. Criar serviços para consumir **PokéAPI**:

   * `/pokemons` → listar com paginação e cache local.
   * `/pokemons/:id` → detalhes.

7. Endpoints principais:

   * `POST /auth/register`
   * `POST /auth/login`
   * `GET /pokemons`
   * `POST /users/:id/pokemons`
   * `PATCH /users/:id/pokemons/:relId`
   * `GET /users/:id/team`

8. Criar migrations e popular tabela `TipoPokémon`.

9. Testar com Postman.

---

## 4. Frontend (Angular)

### 4.1 Criar projeto

```bash
ng new kogui-frontend --routing --style=scss
cd kogui-frontend
```

### 4.2 Módulos principais

* **AuthModule**: login, registro, guarda de rotas.
* **PokemonsModule**: listagem, detalhe, favoritos.
* **TeamModule**: equipe de batalha (máx. 6).
* **SharedModule**: componentes reutilizáveis (cards, headers etc.).

### 4.3 Consumo da API

* Criar `api.service.ts` centralizado.
* Usar `HttpClientModule` para requests.
* Guardar JWT no `localStorage`.

### 4.4 UI/UX

* Cards interativos para Pokémons.
* Ícone/flag para favorito.
* Seletor para equipe (bloqueio em 6).
* Menu para login/logout.

---

## 5. Integração Backend ↔ Frontend

* Criar arquivo `environment.ts` com URL da API.
* Configurar CORS no backend.
* Testar fluxo completo:

  1. Registrar usuário.
  2. Fazer login (JWT).
  3. Listar Pokémons (backend chama PokéAPI).
  4. Favoritar e montar equipe.

---

## 6. Extras (Opcionais)

* Criar `Dockerfile` para backend e frontend.
* Configurar `docker-compose.yml` para rodar ambos.
* Criar rota de reset de senha.
* Painel de gestão de usuários.

---

## 7. Ferramentas de Apoio

* **SQLite Browser**: visualizar dados.
* **pytest**: testes no backend.
* **Angular Material**: UI moderna.
* **Swagger (Flask-Swagger ou drf-yasg no Django)**: documentar API.

---

## 8. Deploy (futuro)

* Backend: Render, Railway ou Heroku (Flask/Django).
* Frontend: Vercel ou Netlify (Angular).
* Banco: SQLite pode ser mantido local ou migrado para PostgreSQL em produção.

---

✅ **Resumo da recomendação de ambiente**:

* Use **VS Code local** → melhor integração com Angular + Python.
* Use **Docker** só se quiser padronizar ambiente ou facilitar deploy.
* Use **GitHub Codespaces** se não quiser configurar nada local (mas pode ficar mais caro e lento).

---

Quer que eu monte um **cronograma prático de desenvolvimento (semana 1, semana 2, etc.)** para você seguir como plano de execução desse app?
