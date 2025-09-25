# Sistema de Design - Gabi

## 🎨 Princípios de Design

### 1. **Consistência Visual**
- **Layout Padrão**: Sidebar + Área principal em todas as páginas
- **Navegação Unificada**: Mesmo padrão de breadcrumb e botões
- **Espaçamento**: Grid system de 8px (0.5rem, 1rem, 1.5rem, 2rem, 3rem, 4rem, 6rem, 8rem)

### 2. **Hierarquia de Informação**
- **Títulos**: H1 (3xl), H2 (2xl), H3 (xl), H4 (lg)
- **Texto**: Base (base), Pequeno (sm), Muito pequeno (xs)
- **Peso**: Normal (400), Médio (500), Semibold (600), Bold (700)

### 3. **Paleta de Cores**
```css
/* Cores Principais */
--primary: 198 100% 45%     /* #00ADE8 - Azul Gabi */
--secondary: 240 4.8% 95.9% /* Cinza claro */
--accent: 240 4.8% 95.9%   /* Cinza de destaque */

/* Cores de Fundo */
--background: 0 0% 100%     /* Branco */
--card: 0 0% 100%          /* Branco para cards */
--sidebar: 240 5.9% 90%    /* Cinza sidebar */

/* Cores de Texto */
--foreground: 240 10% 3.9%  /* Preto */
--muted-foreground: 240 3.8% 46.1% /* Cinza médio */

/* Estados */
--destructive: 0 84.2% 60.2% /* Vermelho erro */
--success: 142 76% 36%      /* Verde sucesso */
--warning: 38 92% 50%       /* Amarelo aviso */
```

### 4. **Componentes Base**

#### **Layout Principal**
```tsx
<div className="flex h-screen bg-background">
  <ModernSidebar />
  <div className="flex-1 overflow-hidden flex flex-col">
    <Header />
    <main className="flex-1 overflow-y-auto">
      <Content />
    </main>
  </div>
</div>
```

#### **Header Padrão**
```tsx
<div className="border-b border-border bg-background/80 backdrop-blur-sm">
  <div className="flex items-center justify-between px-6 py-4">
    <Navigation />
    <Breadcrumb />
  </div>
</div>
```

#### **Cards Padrão**
```tsx
<Card className="p-6">
  <CardHeader className="pb-4">
    <CardTitle className="text-xl font-semibold">Título</CardTitle>
  </CardHeader>
  <CardContent>
    <Content />
  </CardContent>
</Card>
```

### 5. **Padrões de Navegação**

#### **Sidebar (Todas as páginas)**
- Logo Gabi.OS no topo
- Botão "Novo Chat" sempre visível
- Seções: Modo, Agentes, Configurações
- Botão Sair no final

#### **Breadcrumb (Páginas internas)**
```
Início / Configurações / Agentes
```

#### **Tabs (Páginas de configuração)**
- Grid responsivo: 2 colunas mobile, 6 desktop
- Ícones + texto
- Estado ativo destacado

### 6. **Responsividade**

#### **Breakpoints**
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px  
- **Desktop**: > 1024px

#### **Grid System**
- **Mobile**: 1 coluna
- **Tablet**: 2 colunas
- **Desktop**: 3+ colunas

### 7. **Acessibilidade**

#### **Contraste**
- **AA**: Mínimo 4.5:1 para texto normal
- **AAA**: Mínimo 7:1 para texto pequeno

#### **Navegação por Teclado**
- Tab order lógico
- Focus visible em todos os elementos interativos
- Skip links para conteúdo principal

#### **Screen Readers**
- Labels descritivos
- ARIA roles apropriados
- Texto alternativo para imagens

## 🚀 Implementação

### Fase 1: Fundação (Semana 1)
- [ ] Padronizar layout principal
- [ ] Unificar sistema de cores
- [ ] Criar componentes base

### Fase 2: Componentes (Semana 2)  
- [ ] Biblioteca de componentes
- [ ] Padrões de navegação
- [ ] Sistema de grid

### Fase 3: Páginas (Semana 3)
- [ ] Home harmonizada
- [ ] Configurações padronizada
- [ ] Outras páginas

### Fase 4: Polimento (Semana 4)
- [ ] Responsividade
- [ ] Acessibilidade
- [ ] Performance
- [ ] Testes de usuário
