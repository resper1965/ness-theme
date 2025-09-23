"""
Exceções customizadas do Agno SDK para Gabi
"""

class AgnoError(Exception):
    """Exceção base do Agno"""
    pass

class ModelProviderError(AgnoError):
    """Erro do provedor de modelo"""
    pass

class StopAgentRun(AgnoError):
    """Parar execução do agente"""
    pass

class KnowledgeSourceError(AgnoError):
    """Erro na fonte de conhecimento"""
    pass

class SessionError(AgnoError):
    """Erro na sessão"""
    pass

class AgentCreationError(AgnoError):
    """Erro na criação do agente"""
    pass

class DatabaseError(AgnoError):
    """Erro no banco de dados"""
    pass
