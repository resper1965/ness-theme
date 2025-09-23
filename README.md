# Gabi - Chat Multi-Agentes

Um chat inteligente baseado no padrão BMAD com tecnologia Agno SDK, implementado seguindo o documento oficial do Agno.

## 📁 Estrutura do Projeto

```
Gabi/
├── backend/                      # Backend Python com Agno SDK
├── bmad/                        # Padrão BMAD implementado
├── src/                         # Frontend Next.js
├── config/                      # Arquivos de configuração
│   ├── components.json          # Configuração do shadcn/ui
│   ├── eslint.config.mjs        # Configuração do ESLint
│   ├── next.config.ts           # Configuração do Next.js
│   ├── postcss.config.mjs       # Configuração do PostCSS
│   ├── prettier.config.cjs      # Configuração do Prettier
│   ├── tailwind.config.ts       # Configuração do Tailwind
│   ├── tsconfig.json            # Configuração do TypeScript
│   └── env.example              # Exemplo de variáveis de ambiente
├── docs/                        # Documentação
│   ├── README.md                # Documentação principal
│   ├── BRAND_GUIDELINES.md      # Diretrizes de marca
│   └── AGNO_SDK_INTEGRATION_GUIDE.md # Guia de integração Agno SDK
├── assets/                      # Assets públicos
│   ├── favicon.ico              # Favicon
│   ├── gabi.png                 # Logo Gabi
│   └── gabia.png                # Logo Gabi alternativo
├── docker-compose.yml           # Orquestração Docker
├── Dockerfile                   # Container do frontend
├── package.json                 # Dependências do frontend
└── pnpm-lock.yaml              # Lock file do pnpm
```

## 🚀 Início Rápido

### 1. Configuração
```bash
# Copiar configurações de exemplo
cp config/env.example .env

# Editar variáveis de ambiente
nano .env
```

### 2. Instalação
```bash
# Instalar dependências do frontend
pnpm install

# Instalar dependências do backend
cd backend
pip install -r requirements.txt
```

### 3. Execução
```bash
# Executar com Docker
docker-compose up -d

# Ou executar localmente
pnpm dev          # Frontend
cd backend && uvicorn app.main:app --reload  # Backend
```

## 📚 Documentação

- **[Índice da Documentação](docs/INDEX.md)** - Navegação completa da documentação
- **[Documentação Principal](docs/README.md)** - Guia completo do projeto
- **[Brand Guidelines](docs/BRAND_GUIDELINES.md)** - Diretrizes de marca
- **[Agno SDK Integration Guide](docs/AGNO_SDK_INTEGRATION_GUIDE.md)** - Guia de integração

## 🔗 Links Úteis

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).