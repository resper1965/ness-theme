'use client'

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useStore } from '@/store'
import { useQueryState } from 'nuqs'
import { User, Users2, Settings, Play, Pause, Trash2, Edit, Plus } from 'lucide-react'
import { toast } from 'sonner'

export function EntityManager() {
  const { mode, setMode, agents, teams, setAgents, setTeams } = useStore()
  const [agentId, setAgentId] = useQueryState('agent')
  const [teamId, setTeamId] = useQueryState('team')
  const [selectedEntity, setSelectedEntity] = useState<string | null>(null)

  const currentEntities = mode === 'team' ? teams : agents
  const currentValue = mode === 'team' ? teamId : agentId

  const handleModeChange = (newMode: 'agent' | 'team') => {
    setMode(newMode)
    setAgentId(null)
    setTeamId(null)
    setSelectedEntity(null)
  }

  const handleEntitySelect = (entityId: string) => {
    setSelectedEntity(entityId)
    
    if (mode === 'team') {
      setTeamId(entityId)
      setAgentId(null)
    } else {
      setAgentId(entityId)
      setTeamId(null)
    }
  }

  const handleStartChat = () => {
    if (selectedEntity) {
      // Redirecionar para o chat com a entidade selecionada
      window.location.href = `/?${mode}=${selectedEntity}`
    }
  }

  const handleCreateNew = () => {
    if (mode === 'agent') {
      // Abrir modal de criação de agente
      console.log('Criar novo agente')
    } else {
      // Abrir modal de criação de time
      console.log('Criar novo time')
    }
  }

  const handleEditEntity = (entityId: string) => {
    console.log('Editar entidade:', entityId)
  }

  const handleDeleteEntity = (entityId: string) => {
    if (confirm(`Tem certeza que deseja excluir este ${mode === 'agent' ? 'agente' : 'time'}?`)) {
      console.log('Excluir entidade:', entityId)
      toast.success(`${mode === 'agent' ? 'Agente' : 'Time'} excluído com sucesso`)
    }
  }

  return (
    <div className="space-y-6">
      {/* Seletor de Modo */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Configuração de Entidades
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-4">
            <label className="text-sm font-medium">Modo de Operação:</label>
            <Select value={mode} onValueChange={handleModeChange}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="agent">
                  <div className="flex items-center gap-2">
                    <User className="h-4 w-4" />
                    Agente Individual
                  </div>
                </SelectItem>
                <SelectItem value="team">
                  <div className="flex items-center gap-2">
                    <Users2 className="h-4 w-4" />
                    Time/Workflow
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          {currentEntities.length > 0 && (
            <div className="flex items-center gap-4">
              <label className="text-sm font-medium">
                {mode === 'team' ? 'Time' : 'Agente'} Ativo:
              </label>
              <Select value={currentValue || ''} onValueChange={handleEntitySelect}>
                <SelectTrigger className="w-64">
                  <SelectValue placeholder={`Selecione um ${mode === 'team' ? 'time' : 'agente'}`} />
                </SelectTrigger>
                <SelectContent>
                  {currentEntities.map((entity) => (
                    <SelectItem key={entity.id} value={entity.id}>
                      <div className="flex items-center gap-2">
                        {mode === 'team' ? <Users2 className="h-4 w-4" /> : <User className="h-4 w-4" />}
                        {entity.name || entity.id}
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Lista de Entidades */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              {mode === 'team' ? <Users2 className="h-5 w-5" /> : <User className="h-5 w-5" />}
              {mode === 'team' ? 'Times Disponíveis' : 'Agentes Disponíveis'}
            </CardTitle>
            <Button onClick={handleCreateNew} size="sm">
              <Plus className="h-4 w-4 mr-2" />
              Novo {mode === 'team' ? 'Time' : 'Agente'}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {currentEntities.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <div className="flex flex-col items-center gap-2">
                {mode === 'team' ? <Users2 className="h-8 w-8" /> : <User className="h-8 w-8" />}
                <p>Nenhum {mode === 'team' ? 'time' : 'agente'} encontrado</p>
                <Button onClick={handleCreateNew} variant="outline" size="sm">
                  Criar Primeiro {mode === 'team' ? 'Time' : 'Agente'}
                </Button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {currentEntities.map((entity) => (
                <Card 
                  key={entity.id} 
                  className={`cursor-pointer transition-all hover:shadow-md ${
                    selectedEntity === entity.id ? 'ring-2 ring-brand-blue' : ''
                  }`}
                  onClick={() => handleEntitySelect(entity.id)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          {mode === 'team' ? <Users2 className="h-4 w-4" /> : <User className="h-4 w-4" />}
                          <h4 className="font-medium text-sm">{entity.name || entity.id}</h4>
                        </div>
                        <p className="text-xs text-muted-foreground mb-2">
                          {(entity as any).description || 'Sem descrição'}
                        </p>
                        <div className="flex items-center gap-2">
                          <Badge variant="secondary" className="text-xs">
                            {entity.model?.provider || 'Sem modelo'}
                          </Badge>
                        </div>
                      </div>
                      <div className="flex items-center gap-1">
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleEditEntity(entity.id)
                          }}
                          className="h-6 w-6 p-0"
                        >
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleDeleteEntity(entity.id)
                          }}
                          className="h-6 w-6 p-0 text-destructive hover:text-destructive"
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Ações */}
      {selectedEntity && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Ações</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <Button onClick={handleStartChat} className="flex items-center gap-2">
                <Play className="h-4 w-4" />
                Iniciar Chat
              </Button>
              <Button variant="outline" onClick={() => setSelectedEntity(null)}>
                Cancelar Seleção
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
