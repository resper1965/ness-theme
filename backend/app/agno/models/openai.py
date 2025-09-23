"""
Modelo OpenAI
"""

import openai
from typing import Dict, Any, Optional
from .base import Model, ModelResponse


class OpenAIModel(Model):
    """Modelo OpenAI"""
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        super().__init__(
            name=model_name,
            provider="openai",
            config={
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        )
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_response(
        self, 
        context: Dict[str, Any],
        **kwargs
    ) -> str:
        """Gera resposta usando OpenAI"""
        try:
            # Preparar mensagens
            messages = self._prepare_messages(context)
            
            # Configurações do modelo
            model_config = {
                "model": self.name,
                "messages": messages,
                "temperature": self.config.get("temperature", 0.7),
                **kwargs
            }
            
            if self.config.get("max_tokens"):
                model_config["max_tokens"] = self.config["max_tokens"]
            
            # Fazer chamada para OpenAI
            response = await self.client.chat.completions.create(**model_config)
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta OpenAI: {str(e)}")
    
    async def generate_response_with_metadata(
        self, 
        context: Dict[str, Any],
        **kwargs
    ) -> ModelResponse:
        """Gera resposta com metadados"""
        try:
            # Preparar mensagens
            messages = self._prepare_messages(context)
            
            # Configurações do modelo
            model_config = {
                "model": self.name,
                "messages": messages,
                "temperature": self.config.get("temperature", 0.7),
                **kwargs
            }
            
            if self.config.get("max_tokens"):
                model_config["max_tokens"] = self.config["max_tokens"]
            
            # Fazer chamada para OpenAI
            response = await self.client.chat.completions.create(**model_config)
            
            return ModelResponse(
                content=response.choices[0].message.content,
                metadata={
                    "model": self.name,
                    "provider": self.provider,
                    "finish_reason": response.choices[0].finish_reason
                },
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                model=self.name
            )
            
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta OpenAI: {str(e)}")
    
    def _prepare_messages(self, context: Dict[str, Any]) -> list:
        """Prepara mensagens para o modelo"""
        messages = []
        
        # Adicionar histórico da conversa
        if "conversation_history" in context:
            messages.extend(context["conversation_history"])
        
        # Adicionar conhecimento relevante
        if "knowledge" in context and context["knowledge"]:
            knowledge_text = self._format_knowledge(context["knowledge"])
            messages.append({
                "role": "system",
                "content": f"Conhecimento relevante:\n{knowledge_text}"
            })
        
        # Adicionar configuração do agente
        if "agent_config" in context:
            agent_config = context["agent_config"]
            system_prompt = f"""
            Você é um agente chamado {agent_config.get('name', 'Assistente')}.
            Descrição: {agent_config.get('description', '')}
            
            Instruções:
            - Seja útil e preciso
            - Use o conhecimento fornecido quando relevante
            - Cite fontes quando apropriado
            """
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Adicionar mensagem do usuário
        if "message" in context:
            messages.append({
                "role": "user",
                "content": context["message"]
            })
        
        return messages
    
    def _format_knowledge(self, knowledge: list) -> str:
        """Formata conhecimento para o modelo"""
        if not knowledge:
            return ""
        
        formatted = []
        for i, kb in enumerate(knowledge, 1):
            content = kb.get("content", "")
            source = kb.get("source", f"Fonte {i}")
            formatted.append(f"{i}. {content}\n   Fonte: {source}")
        
        return "\n\n".join(formatted)
