"use client";

import React, { useState, useEffect } from 'react';
import { 
  Plus, 
  Settings, 
  LogOut, 
  Menu, 
  X, 
  ChevronLeft, 
  ChevronRight,
  MessageSquare,
  Users,
  Zap,
  Search,
  HelpCircle,
  Sun,
  Moon,
  Server,
  Edit,
  Check,
  RefreshCw,
  User,
  Users2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/ui/theme-toggle';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useStore } from '@/store';
import { useQueryState } from 'nuqs';
import { isValidUrl } from '@/lib/utils';
import { toast } from 'sonner';
import useChatActions from '@/hooks/useChatActions';

interface NavigationItem {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  href: string;
  badge?: string;
}

interface ModernSidebarProps {
  className?: string;
  onNewChat?: () => void;
  onSettings?: () => void;
  onLogout?: () => void;
}

// Navigation items for Gabi - Removido para dar espaço aos chats
const navigationItems: NavigationItem[] = [];

export function ModernSidebar({ 
  className = "", 
  onNewChat,
  onSettings,
  onLogout 
}: ModernSidebarProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeItem, setActiveItem] = useState("chat");

  // Auto-open sidebar on desktop
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setIsOpen(true);
      } else {
        setIsOpen(false);
      }
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleSidebar = () => setIsOpen(!isOpen);
  const toggleCollapse = () => setIsCollapsed(!isCollapsed);

  const handleItemClick = (itemId: string) => {
    setActiveItem(itemId);
    if (window.innerWidth < 768) {
      setIsOpen(false);
    }
  };

  return (
    <>
      {/* Mobile hamburger button */}
      <button
        onClick={toggleSidebar}
        className="fixed top-6 left-6 z-50 p-3 rounded-lg bg-sidebar shadow-md border border-cyan-800 md:hidden hover:bg-sidebar-accent transition-all duration-200"
        aria-label="Toggle sidebar"
      >
        {isOpen ? 
          <X className="h-5 w-5 text-sidebar-foreground" /> : 
          <Menu className="h-5 w-5 text-sidebar-foreground" />
        }
      </button>

      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/40 backdrop-blur-sm z-30 md:hidden transition-opacity duration-300" 
          onClick={toggleSidebar} 
        />
      )}

      {/* Sidebar */}
      <div
        className={`
          fixed top-0 left-0 h-full bg-neutral-50 border-r border-neutral-border z-40 transition-all duration-300 ease-in-out flex flex-col shadow-soft
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
          ${isCollapsed ? "w-20" : "w-72"}
          md:translate-x-0 md:static md:z-auto
          ${className}
        `}
      >
        {/* Header with logo and collapse button */}
        <div className="flex items-center justify-between p-6 bg-neutral-50 border-b border-neutral-border">
          {!isCollapsed ? (
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-brand-blue rounded-lg flex items-center justify-center shadow-sm">
                <span className="text-white font-bold text-lg">G</span>
              </div>
              <div className="flex flex-col">
                <span className="font-semibold text-default-font text-lg">
                  Gabi<span className="text-brand-blue">.</span>
                </span>
                <span className="text-xs text-subtext-color">Chat Multi-Agentes</span>
              </div>
            </div>
          ) : (
            <div className="w-10 h-10 bg-brand-blue rounded-lg flex items-center justify-center mx-auto shadow-sm">
              <span className="text-white font-bold text-lg">G</span>
            </div>
          )}

          {/* Desktop collapse button */}
          <button
            onClick={toggleCollapse}
            className="flex p-2 rounded-md hover:bg-sidebar-accent transition-all duration-200 hover:shadow-soft"
            aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {isCollapsed ? (
              <ChevronRight className="h-4 w-4 text-sidebar-foreground" />
            ) : (
              <ChevronLeft className="h-4 w-4 text-sidebar-foreground" />
            )}
          </button>
        </div>

        {/* New Chat Button */}
        <div className="p-4">
          <Button
            onClick={onNewChat}
            className="w-full bg-brand-blue hover:bg-brand-blue/90 text-white font-medium"
          >
            <Plus className="h-4 w-4 mr-2" />
            {!isCollapsed && "Novo Chat"}
          </Button>
        </div>


        {/* Gabi.OS Endpoint Section */}
        {!isCollapsed && <GabiOSSection />}

        {/* Mode Selector */}
        {!isCollapsed && <ModeSection />}

        {/* Entity Selector */}
        {!isCollapsed && <EntitySection />}

        {/* Chat Area - Espaço para chats dos usuários */}
        <div className="flex-1 px-3 py-2 overflow-y-auto">
          {/* Aqui será implementada a área de chats dos usuários */}
          <div className="text-center text-muted-foreground text-sm py-8">
            {!isCollapsed ? "Área de Chats" : ""}
          </div>
        </div>

        {/* Bottom section with theme toggle, settings and logout */}
        <div className="mt-auto">
          {/* Theme Toggle */}
          <div className="px-4 py-2">
            <div className={`flex items-center ${isCollapsed ? "justify-center" : "space-x-3"}`}>
              <ThemeToggle />
              {!isCollapsed && (
                <span className="text-sm text-sidebar-foreground">Tema</span>
              )}
            </div>
          </div>

                {/* Settings Button */}
                <div className="px-4 py-2">
                  <button
                    onClick={() => window.location.href = '/configuracoes'}
                    className={`
                      w-full flex items-center rounded-md text-left transition-all duration-200 group
                      text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground
                      ${isCollapsed ? "justify-center p-2" : "space-x-3 px-3 py-2"}
                    `}
                    title={isCollapsed ? "Configurações" : undefined}
                  >
                    <div className="flex items-center justify-center min-w-[24px]">
                      <Settings className="h-5 w-5 flex-shrink-0 text-sidebar-foreground group-hover:text-sidebar-accent-foreground" />
                    </div>
                    
                    {!isCollapsed && (
                      <span className="text-sm">Configurações</span>
                    )}
                    
                    {/* Tooltip for collapsed state */}
                    {isCollapsed && (
                      <div className="absolute left-full ml-2 px-2 py-1 bg-sidebar-foreground text-sidebar text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                        Configurações
                        <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 w-1.5 h-1.5 bg-sidebar-foreground rotate-45" />
                      </div>
                    )}
                  </button>
                </div>

          {/* Logout Button */}
          <div className="px-4 py-2">
            <button
              onClick={onLogout}
              className={`
                w-full flex items-center rounded-md text-left transition-all duration-200 group
                text-cyan-300 hover:bg-cyan-800/20 hover:text-cyan-200
                ${isCollapsed ? "justify-center p-2" : "space-x-3 px-3 py-2"}
              `}
              title={isCollapsed ? "Sair" : undefined}
            >
              <div className="flex items-center justify-center min-w-[24px]">
                <LogOut className="h-5 w-5 flex-shrink-0 text-cyan-300 group-hover:text-cyan-200" />
              </div>
              
              {!isCollapsed && (
                <span className="text-sm">Sair</span>
              )}
              
              {/* Tooltip for collapsed state */}
              {isCollapsed && (
                <div className="absolute left-full ml-2 px-2 py-1 bg-sidebar-foreground text-sidebar text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                  Sair
                  <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 w-1.5 h-1.5 bg-sidebar-foreground rotate-45" />
                </div>
              )}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

// Gabi.OS Endpoint Section
function GabiOSSection() {
  const {
    selectedEndpoint,
    isEndpointActive,
    setSelectedEndpoint,
    setAgents,
    setSessionsData,
    setMessages
  } = useStore();
  const { initialize } = useChatActions();
  const [isEditing, setIsEditing] = useState(false);
  const [endpointValue, setEndpointValue] = useState('');
  const [isRotating, setIsRotating] = useState(false);
  const [, setAgentId] = useQueryState('agent');
  const [, setSessionId] = useQueryState('session');

  useEffect(() => {
    setEndpointValue(selectedEndpoint);
  }, [selectedEndpoint]);

  const handleSave = async () => {
    if (!isValidUrl(endpointValue)) {
      toast.error('Please enter a valid URL');
      return;
    }
    const cleanEndpoint = endpointValue.replace(/\/$/, '').trim();
    setSelectedEndpoint(cleanEndpoint);
    setAgentId(null);
    setSessionId(null);
    setIsEditing(false);
    setAgents([]);
    setSessionsData([]);
    setMessages([]);
  };

  const handleCancel = () => {
    setEndpointValue(selectedEndpoint);
    setIsEditing(false);
  };

  const handleRefresh = async () => {
    setIsRotating(true);
    await initialize();
    setTimeout(() => setIsRotating(false), 500);
  };

  return (
    <div className="px-4 py-2">
      <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground mb-2">
        <Server className="h-4 w-4" />
        Gabi<span className="text-brand-blue">.</span>OS
      </div>
      {isEditing ? (
        <div className="flex w-full items-center gap-1">
          <input
            type="text"
            value={endpointValue}
            onChange={(e) => setEndpointValue(e.target.value)}
            className="flex h-8 w-full items-center text-ellipsis rounded-md border border-cyan-800 bg-background px-3 text-sm font-medium text-foreground"
            placeholder="Enter endpoint URL"
            autoFocus
          />
          <Button
            variant="ghost"
            size="icon"
            onClick={handleSave}
            className="h-8 w-8 hover:bg-sidebar-accent"
          >
            <Check className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={handleCancel}
            className="h-8 w-8 hover:bg-sidebar-accent"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <div className="flex w-full items-center gap-1">
          <div className="flex h-8 w-full items-center justify-between rounded-md border border-cyan-800 bg-background px-3 text-sm">
            <span className="truncate text-sidebar-foreground">
              {selectedEndpoint || 'NENHUM ENDPOINT ADICIONADO'}
            </span>
            <div className="flex gap-1">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsEditing(true)}
                className="h-6 w-6 hover:bg-sidebar-accent"
              >
                <Edit className="h-3 w-3" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={handleRefresh}
                disabled={isRotating}
                className="h-6 w-6 hover:bg-sidebar-accent"
              >
                <RefreshCw className={`h-3 w-3 ${isRotating ? 'animate-spin' : ''}`} />
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Mode Selector Section
function ModeSection() {
  const { mode, setMode, setMessages, setSelectedModel } = useStore();
  const { clearChat } = useChatActions();
  const [, setAgentId] = useQueryState('agent');
  const [, setTeamId] = useQueryState('team');
  const [, setSessionId] = useQueryState('session');

  const handleModeChange = (newMode: 'agent' | 'team') => {
    if (newMode === mode) return;

    setMode(newMode);
    setAgentId(null);
    setTeamId(null);
    setSelectedModel('');
    setMessages([]);
    setSessionId(null);
    clearChat();
  };

  return (
    <div className="px-4 py-2">
      <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground mb-2">
        <Zap className="h-4 w-4" />
        Modo
      </div>
      <Select
        defaultValue={mode}
        value={mode}
        onValueChange={(value) => handleModeChange(value as 'agent' | 'team')}
      >
        <SelectTrigger className="h-8 w-full rounded-md border border-cyan-800 bg-background text-xs font-medium text-sidebar-foreground">
          <SelectValue />
        </SelectTrigger>
        <SelectContent className="border-cyan-800 bg-sidebar text-sidebar-foreground shadow-lg">
          <SelectItem value="agent" className="cursor-pointer text-sidebar-foreground">
            <div className="text-xs font-medium uppercase">Agent</div>
          </SelectItem>
          <SelectItem value="team" className="cursor-pointer text-sidebar-foreground">
            <div className="text-xs font-medium uppercase">Team</div>
          </SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}

// Entity Selector Section
function EntitySection() {
  const { mode, agents, teams, setMessages, setSelectedModel } = useStore();
  const { focusChatInput } = useChatActions();
  const [agentId, setAgentId] = useQueryState('agent', {
    parse: (value) => value || undefined,
    history: 'push'
  });
  const [teamId, setTeamId] = useQueryState('team', {
    parse: (value) => value || undefined,
    history: 'push'
  });
  const [, setSessionId] = useQueryState('session');

  const currentEntities = mode === 'team' ? teams : agents;
  const currentValue = mode === 'team' ? teamId : agentId;
  const placeholder = mode === 'team' ? 'Select Team' : 'Select Agent';

  const handleOnValueChange = (value: string) => {
    const newValue = value === currentValue ? null : value;
    const selectedEntity = currentEntities.find((item) => item.id === newValue);

    setSelectedModel(selectedEntity?.model?.provider || '');

    if (mode === 'team') {
      setTeamId(newValue);
      setAgentId(null);
    } else {
      setAgentId(newValue);
      setTeamId(null);
    }

    setMessages([]);
    setSessionId(null);

    if (selectedEntity?.model?.provider) {
      focusChatInput();
    }
  };

  if (currentEntities.length === 0) {
    return (
      <div className="px-4 py-2">
        <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground mb-2">
          {mode === 'team' ? <Users2 className="h-4 w-4" /> : <User className="h-4 w-4" />}
          {mode === 'team' ? 'Equipes' : 'Agentes'}
        </div>
        <Select disabled>
          <SelectTrigger className="h-8 w-full rounded-md border border-cyan-800 bg-background text-xs font-medium text-muted-foreground opacity-50">
            <SelectValue placeholder={`No ${mode}s Available`} />
          </SelectTrigger>
        </Select>
      </div>
    );
  }

  return (
    <div className="px-4 py-2">
      <div className="flex items-center gap-2 text-sm font-medium text-sidebar-foreground mb-2">
        {mode === 'team' ? <Users2 className="h-4 w-4" /> : <User className="h-4 w-4" />}
        {mode === 'team' ? 'Equipes' : 'Agentes'}
      </div>
      <Select
        value={currentValue || ''}
        onValueChange={(value) => handleOnValueChange(value)}
      >
        <SelectTrigger className="h-8 w-full rounded-md border border-cyan-800 bg-background text-xs font-medium text-sidebar-foreground">
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent className="border-cyan-800 bg-sidebar text-sidebar-foreground shadow-lg">
          {currentEntities.map((entity, index) => (
            <SelectItem
              className="cursor-pointer text-sidebar-foreground"
              key={`${entity.id}-${index}`}
              value={entity.id}
            >
              <div className="flex items-center gap-3 text-xs font-medium">
              <Users className="h-4 w-4" />
                {entity.name || entity.id}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
