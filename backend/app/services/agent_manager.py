"""
Gerenciador de agentes dinâmicos
Implementa criação e orquestração de agentes baseado no padrão BMAD
"""

import logging
from typing import List, Dict, Optional, Any
from app.models.agent import Agent, AgentType, KnowledgeSource
from app.models.session import Session
from app.schemas.agent import AgentCreate, AgentResponse
from app.config.settings import get_settings

logger = logging.getLogger(__name__)

class AgentManager:
    """Gerenciador de agentes dinâmicos"""
    
    def __init__(self):
        self.settings = get_settings()
        self.agent_templates = self._load_agent_templates()
    
    def _load_agent_templates(self) -> Dict[str, Dict[str, Any]]:
        """Carrega templates de agentes pré-definidos"""
        return {
            "research_agent": {
                "name": "Agente de Pesquisa",
                "description": "Especializado em pesquisa e análise de informações",
                "model": "gpt-4",
                "capabilities": ["web_search", "document_analysis", "data_processing"],
                "knowledge_sources": ["web", "documents"]
            },
            "writing_agent": {
                "name": "Agente de Escrita",
                "description": "Especializado em criação de conteúdo e redação",
                "model": "gpt-4",
                "capabilities": ["content_creation", "editing", "formatting"],
                "knowledge_sources": ["documents", "templates"]
            },
            "analysis_agent": {
                "name": "Agente de Análise",
                "description": "Especializado em análise de dados e insights",
                "model": "gpt-4",
                "capabilities": ["data_analysis", "pattern_recognition", "insights"],
                "knowledge_sources": ["databases", "reports"]
            },
            "orchestrator": {
                "name": "Orquestrador",
                "description": "Coordena e orquestra outros agentes",
                "model": "gpt-4",
                "capabilities": ["coordination", "task_distribution", "result_synthesis"],
                "knowledge_sources": ["all"]
            }
        }
    
    def create_agent_from_template(self, template_name: str, session_id: str, custom_config: Optional[Dict[str, Any]] = None) -> AgentCreate:
        """Cria um agente baseado em template"""
        if template_name not in self.agent_templates:
            raise ValueError(f"Template '{template_name}' não encontrado")
        
        template = self.agent_templates[template_name]
        config = custom_config or {}
        
        # Gerar ID único
        import uuid
        agent_id = str(uuid.uuid4())
        
        # Configurar fontes de conhecimento
        knowledge_sources = []
        for source_type in template.get("knowledge_sources", []):
            knowledge_sources.append(KnowledgeSource(
                id=str(uuid.uuid4()),
                name=f"Fonte {source_type}",
                type=source_type,
                config={"enabled": True}
            ))
        
        return AgentCreate(
            id=agent_id,
            name=config.get("name", template["name"]),
            description=config.get("description", template["description"]),
            type=AgentType.ORCHESTRATOR if template_name == "orchestrator" else AgentType.AGENT,
            model=config.get("model", template["model"]),
            knowledge_sources=knowledge_sources
        )
    
    def validate_session_limits(self, session: Session, agent_type: AgentType) -> bool:
        """Valida limites de agentes na sessão"""
        if agent_type == AgentType.ORCHESTRATOR:
            return session.orchestrator_count < session.max_orchestrator
        else:
            return session.agents_count < session.max_agents
    
    def get_available_templates(self) -> List[str]:
        """Retorna templates disponíveis"""
        return list(self.agent_templates.keys())
    
    def get_agent_capabilities(self, agent_type: str) -> List[str]:
        """Retorna capacidades de um tipo de agente"""
        if agent_type in self.agent_templates:
            return self.agent_templates[agent_type].get("capabilities", [])
        return []
    
    def suggest_agent_combination(self, task_description: str) -> List[str]:
        """Sugere combinação de agentes baseada na descrição da tarefa"""
        suggestions = []
        
        # Análise simples baseada em palavras-chave
        task_lower = task_description.lower()
        
        if any(word in task_lower for word in ["pesquisar", "buscar", "encontrar", "investigar"]):
            suggestions.append("research_agent")
        
        if any(word in task_lower for word in ["escrever", "criar", "redigir", "documento"]):
            suggestions.append("writing_agent")
        
        if any(word in task_lower for word in ["analisar", "dados", "insights", "padrões"]):
            suggestions.append("analysis_agent")
        
        # Sempre incluir orquestrador
        suggestions.append("orchestrator")
        
        return list(set(suggestions))  # Remove duplicatas
    
    def create_agent_workflow(self, session_id: str, task_description: str) -> List[AgentCreate]:
        """Cria workflow de agentes baseado na tarefa"""
        suggested_templates = self.suggest_agent_combination(task_description)
        agents = []
        
        for template_name in suggested_templates:
            try:
                agent = self.create_agent_from_template(template_name, session_id)
                agents.append(agent)
            except Exception as e:
                logger.error(f"Erro ao criar agente {template_name}: {e}")
        
        return agents
    
    def optimize_agent_configuration(self, agents: List[Agent], task_description: str) -> List[Agent]:
        """Otimiza configuração de agentes baseada na tarefa"""
        # Implementar lógica de otimização
        # Por exemplo: ajustar modelos, fontes de conhecimento, etc.
        return agents
    
    def get_agent_performance_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Retorna métricas de performance de um agente"""
        # Implementar coleta de métricas
        return {
            "agent_id": agent_id,
            "messages_processed": 0,
            "response_time_avg": 0.0,
            "success_rate": 0.0,
            "knowledge_sources_used": []
        }
