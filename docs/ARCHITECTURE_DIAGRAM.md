# Diagrama de Arquitetura - Gabi System

## 🏗️ Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        GABI SYSTEM                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   FRONTEND      │    │    BACKEND      │    │   DATABASE  │ │
│  │   Next.js       │◄──►│   FastAPI       │◄──►│ PostgreSQL  │ │
│  │   Port 3000     │    │   Port 7777     │    │ Port 5432   │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
│           │                       │                             │
│           │                       │                             │
│           ▼                       ▼                             │
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │     REDIS       │    │   AGNO SDK      │                    │
│  │     Cache       │    │   Integration   │                    │
│  │   Port 6379     │    │   (Optional)    │                    │
│  └─────────────────┘    └─────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de Dados

```
┌─────────────┐    HTTP     ┌─────────────┐    API     ┌─────────────┐
│   USUÁRIO   │ ──────────► │  FRONTEND   │ ─────────► │  BACKEND    │
│             │            │  (Next.js)  │            │ (FastAPI)   │
└─────────────┘            └─────────────┘            └─────────────┘
                                    │                         │
                                    │                         │
                                    ▼                         ▼
                           ┌─────────────┐            ┌─────────────┐
                           │   REDIS     │            │ POSTGRESQL  │
                           │   CACHE     │            │  DATABASE   │
                           └─────────────┘            └─────────────┘
```

## 📱 Estrutura de Telas

```
┌─────────────────────────────────────────────────────────────────┐
│                        GABI INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────────────────────────────────┐  │
│  │   SIDEBAR   │  │              MAIN CONTENT                │  │
│  │             │  │                                         │  │
│  │ • Chat      │  │  ┌─────────────────────────────────┐   │  │
│  │ • Chats     │  │  │         CHAT INTERFACE          │   │  │
│  │ • Gabi.OS   │  │  │                                 │   │  │
│  │ • Config    │  │  │  ┌─────────────────────────┐   │   │  │
│  │             │  │  │  │    MESSAGE AREA         │   │   │  │
│  │             │  │  │  │                         │   │   │  │
│  │             │  │  │  └─────────────────────────┘   │   │  │
│  │             │  │  │                                 │   │  │
│  │             │  │  │  ┌─────────────────────────┐   │   │  │
│  │             │  │  │  │    INPUT FIELD          │   │   │  │
│  │             │  │  │  └─────────────────────────┘   │   │  │
│  │             │  │  └─────────────────────────────────┘   │  │
│  └─────────────┘  └─────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔌 API Endpoints

```
┌─────────────────────────────────────────────────────────────────┐
│                        API STRUCTURE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐ │
│  │   CHAT API      │    │  AGENTS API     │    │ AGNO API    │ │
│  │                 │    │                 │    │             │ │
│  │ POST /chat/     │    │ GET /agents     │    │ GET /agno/  │ │
│  │ send-message    │    │ POST /agents    │    │ status      │ │
│  │                 │    │ PUT /agents/{id}│    │             │ │
│  │ POST /chat/     │    │ DELETE /agents/ │    │ POST /     │ │
│  │ start-session   │    │ {id}            │    │ dynamic/   │ │
│  │                 │    │                 │    │ agents     │ │
│  │ GET /chat/      │    │                 │    │             │ │
│  │ session-status  │    │                 │    │             │ │
│  └─────────────────┘    └─────────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🐳 Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DOCKER CONTAINERS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ GABI-CHAT   │  │  GABI-OS    │  │GABI-POSTGRES│  │GABI-REDIS│ │
│  │             │  │             │  │             │  │         │ │
│  │ Next.js     │  │ FastAPI     │  │ PostgreSQL  │  │ Redis   │ │
│  │ Port 3000   │  │ Port 7777   │  │ Port 5432   │  │Port 6379│ │
│  │             │  │             │  │             │  │         │ │
│  │ Frontend    │  │ Backend     │  │ Database    │  │ Cache   │ │
│  │ Interface   │  │ API Server  │  │ Storage     │  │ Session │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Sequence

```
1. USER INPUT
   │
   ▼
2. FRONTEND VALIDATION
   │
   ▼
3. HTTP REQUEST TO BACKEND
   │
   ▼
4. BACKEND PROCESSING
   │
   ▼
5. AGNO SDK INTEGRATION (if available)
   │
   ▼
6. DATABASE QUERY/UPDATE
   │
   ▼
7. REDIS CACHE UPDATE
   │
   ▼
8. RESPONSE TO FRONTEND
   │
   ▼
9. UI UPDATE
   │
   ▼
10. USER SEES RESULT
```

## 🎯 Component Hierarchy

```
Gabi App
├── Layout
│   ├── Sidebar
│   │   ├── Navigation
│   │   └── User Actions
│   └── Main Content
│       ├── Chat Page (/)
│       │   ├── Message List
│       │   ├── Input Field
│       │   └── Send Button
│       ├── Chats Page (/chats)
│       │   ├── Chat History
│       │   └── Chat Actions
│       ├── Gabi.OS Page (/gabi-os)
│       │   ├── URL Input
│       │   ├── Connection Test
│       │   └── Status Display
│       └── Config Page (/configuracoes)
│           ├── Agent Management
│           ├── System Settings
│           └── Advanced Options
```

## 🔧 Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FRONTEND:              BACKEND:              INFRASTRUCTURE: │
│  ┌─────────────┐        ┌─────────────┐        ┌─────────────┐ │
│  │ Next.js 15  │        │ FastAPI     │        │ Docker      │ │
│  │ React 18    │        │ Python 3.11 │        │ Compose     │ │
│  │ TypeScript  │        │ Pydantic    │        │ PostgreSQL  │ │
│  │ TailwindCSS │        │ SQLAlchemy  │        │ Redis       │ │
│  │ shadcn/ui   │        │ Agno SDK    │        │ WSL2        │ │
│  └─────────────┘        └─────────────┘        └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Performance Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE TARGETS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • Page Load Time:     < 50ms                                  │
│  • Chat Response:      < 20ms                                  │
│  • API Response:       < 100ms                                │
│  • Database Query:     < 50ms                                  │
│  • Memory Usage:       < 2GB                                   │
│  • CPU Usage:          < 50%                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Sistema Gabi - Arquitetura Documentada**  
*Powered by ness.*
