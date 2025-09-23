"""
Serviço de workflows/teams - Implementação baseada no documento oficial do Agno
Compatível com Agno UI seguindo padrão BMAD
"""

import logging
import uuid
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.config.settings import get_settings
from app.models.agent import Agent, AgentType
from app.schemas.agent import AgentCreate, AgentResponse

logger = logging.getLogger(__name__)

class WorkflowService:
    """Serviço para gerenciamento de workflows/teams baseado no documento do Agno"""
    
    def __init__(self):
        self.settings = get_settings()
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.workflow_templates: Dict[str, Dict[str, Any]] = {
            "research_workflow": {
                "name": "Workflow de Pesquisa",
                "description": "Workflow para pesquisa e análise de dados",
                "agents": [
                    {
                        "name": "Pesquisador Principal",
                        "type": "agent",
                        "model": "gpt-4",
                        "description": "Agente responsável pela pesquisa principal"
                    },
                    {
                        "name": "Analista de Dados",
                        "type": "agent", 
                        "model": "gpt-4",
                        "description": "Agente especializado em análise de dados"
                    },
                    {
                        "name": "Orquestrador de Pesquisa",
                        "type": "orchestrator",
                        "model": "gpt-4",
                        "description": "Coordena o processo de pesquisa"
                    }
                ]
            },
            "writing_workflow": {
                "name": "Workflow de Escrita",
                "description": "Workflow para criação de conteúdo",
                "agents": [
                    {
                        "name": "Escritor Principal",
                        "type": "agent",
                        "model": "gpt-4",
                        "description": "Agente responsável pela escrita principal"
                    },
                    {
                        "name": "Revisor de Conteúdo",
                        "type": "agent",
                        "model": "gpt-4", 
                        "description": "Agente especializado em revisão"
                    },
                    {
                        "name": "Orquestrador de Escrita",
                        "type": "orchestrator",
                        "model": "gpt-4",
                        "description": "Coordena o processo de escrita"
                    }
                ]
            },
            "analysis_workflow": {
                "name": "Workflow de Análise",
                "description": "Workflow para análise e relatórios",
                "agents": [
                    {
                        "name": "Analista Principal",
                        "type": "agent",
                        "model": "gpt-4",
                        "description": "Agente responsável pela análise principal"
                    },
                    {
                        "name": "Gerador de Relatórios",
                        "type": "agent",
                        "model": "gpt-4",
                        "description": "Agente especializado em relatórios"
                    },
                    {
                        "name": "Orquestrador de Análise",
                        "type": "orchestrator",
                        "model": "gpt-4",
                        "description": "Coordena o processo de análise"
                    }
                ]
            }
        }
    
    async def create_workflow_from_template(self, template_name: str, session_id: str, custom_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Cria workflow a partir de template baseado no documento do Agno"""
        try:
            if template_name not in self.workflow_templates:
                raise ValueError(f"Template '{template_name}' não encontrado")
            
            template = self.workflow_templates[template_name]
            workflow_id = f"workflow-{uuid.uuid4().hex[:8]}"
            
            # Aplicar configurações customizadas se fornecidas
            if custom_config:
                template = {**template, **custom_config}
            
            workflow = {
                "id": workflow_id,
                "name": template["name"],
                "description": template["description"],
                "template_name": template_name,
                "session_id": session_id,
                "agents": template["agents"],
                "status": "active",
                "created_at": int(datetime.now().timestamp()),
                "updated_at": int(datetime.now().timestamp())
            }
            
            self.active_workflows[workflow_id] = workflow
            
            logger.info(f"✅ Workflow criado: {workflow_id} do template {template_name}")
            
            return workflow
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar workflow: {e}")
            raise
    
    async def create_custom_workflow(self, session_id: str, task_description: str, agent_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cria workflow customizado baseado na descrição da tarefa"""
        try:
            workflow_id = f"workflow-{uuid.uuid4().hex[:8]}"
            
            # Analisar descrição da tarefa para determinar agentes necessários
            suggested_agents = self._analyze_task_for_agents(task_description)
            
            # Combinar agentes sugeridos com configurações fornecidas
            final_agents = suggested_agents + agent_configs
            
            workflow = {
                "id": workflow_id,
                "name": f"Workflow para: {task_description[:50]}...",
                "description": f"Workflow customizado para: {task_description}",
                "template_name": "custom",
                "session_id": session_id,
                "task_description": task_description,
                "agents": final_agents,
                "status": "active",
                "created_at": int(datetime.now().timestamp()),
                "updated_at": int(datetime.now().timestamp())
            }
            
            self.active_workflows[workflow_id] = workflow
            
            logger.info(f"✅ Workflow customizado criado: {workflow_id}")
            
            return workflow
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar workflow customizado: {e}")
            raise
    
    def _analyze_task_for_agents(self, task_description: str) -> List[Dict[str, Any]]:
        """Analisa descrição da tarefa para sugerir agentes necessários"""
        agents = []
        task_lower = task_description.lower()
        
        # Análise baseada em palavras-chave
        if any(word in task_lower for word in ["pesquisar", "pesquisa", "buscar", "encontrar"]):
            agents.append({
                "name": "Pesquisador",
                "type": "agent",
                "model": "gpt-4",
                "description": "Agente especializado em pesquisa"
            })
        
        if any(word in task_lower for word in ["escrever", "criar", "redigir", "documento"]):
            agents.append({
                "name": "Escritor",
                "type": "agent", 
                "model": "gpt-4",
                "description": "Agente especializado em escrita"
            })
        
        if any(word in task_lower for word in ["analisar", "análise", "avaliar", "examinar"]):
            agents.append({
                "name": "Analista",
                "type": "agent",
                "model": "gpt-4",
                "description": "Agente especializado em análise"
            })
        
        # Sempre adicionar orquestrador
        agents.append({
            "name": "Orquestrador",
            "type": "orchestrator",
            "model": "gpt-4",
            "description": "Coordena a execução da tarefa"
        })
        
        return agents
    
    async def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Retorna workflow específico"""
        return self.active_workflows.get(workflow_id)
    
    async def get_workflows_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Retorna workflows de uma sessão"""
        workflows = []
        for workflow in self.active_workflows.values():
            if workflow["session_id"] == session_id:
                workflows.append(workflow)
        return workflows
    
    async def get_available_templates(self) -> List[Dict[str, Any]]:
        """Retorna templates disponíveis"""
        templates = []
        for template_name, template in self.workflow_templates.items():
            templates.append({
                "name": template_name,
                "display_name": template["name"],
                "description": template["description"],
                "agents_count": len(template["agents"])
            })
        return templates
    
    async def execute_workflow(self, workflow_id: str, session_id: str, message: str) -> Dict[str, Any]:
        """Executa workflow - compatível com Agno UI"""
        try:
            workflow = await self.get_workflow(workflow_id)
            if not workflow:
                raise ValueError("Workflow não encontrado")
            
            if workflow["session_id"] != session_id:
                raise ValueError("Workflow não pertence à sessão especificada")
            
            # Simular execução do workflow
            run_id = f"run-{uuid.uuid4().hex[:8]}"
            
            response = {
                "run_id": run_id,
                "workflow_id": workflow_id,
                "session_id": session_id,
                "status": "RUNNING",
                "message": f"Executando workflow {workflow['name']}: {message}",
                "agents_involved": [agent["name"] for agent in workflow["agents"]],
                "created_at": int(datetime.now().timestamp())
            }
            
            logger.info(f"✅ Workflow {workflow_id} executado")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao executar workflow: {e}")
            raise
    
    async def delete_workflow(self, workflow_id: str) -> bool:
        """Remove workflow"""
        try:
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
                logger.info(f"✅ Workflow removido: {workflow_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao remover workflow: {e}")
            raise
    
    def get_teams(self) -> List[Dict[str, Any]]:
        """Retorna lista de teams (workflows) - compatível com Agno UI"""
        teams = []
        for workflow in self.active_workflows.values():
            teams.append({
                "id": workflow["id"],
                "name": workflow["name"],
                "description": workflow["description"],
                "session_id": workflow["session_id"],
                "status": workflow["status"],
                "agents_count": len(workflow["agents"]),
                "created_at": workflow["created_at"]
            })
        return teams
