from typing import List, Any, Dict

from langgraph.prebuilt.chat_agent_executor import (
    StructuredResponseSchema,
    Prompt,
    StateSchemaType,
)
from langgraph.store.base import BaseStore
from langgraph.types import Checkpointer

from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langchain_core.language_models import LanguageModelLike


class Agent:

    def __new__(
        self,
        tools: List[BaseTool],
        store: BaseStore = None,
        memory: Checkpointer = None,
        name: str = None,
        model: LanguageModelLike = None,
        prompt: Prompt = None,
        output_schema: StructuredResponseSchema = None,
        state_schema: StateSchemaType = None,
        description: str | None = None,
        skills: List[str] | None = None,
    ):
        instance = create_react_agent(
            name=name,
            model=model,
            tools=tools,
            store=store,
            checkpointer=memory,
            prompt=prompt,
            state_schema=state_schema,
            response_format=output_schema,
        )

        # --- INICIO DE LA MODIFICACIÓN ---

        # Adjuntamos los metadatos directamente a la instancia
        setattr(instance, "description", description)
        setattr(instance, "skills", skills)
        # El nombre ya está en el grafo, pero lo guardamos para un acceso fácil
        setattr(instance, "name", name)

        # Creamos una función que recolectará la información
        def info() -> Dict[str, Any]:
            """Devuelve un diccionario con los metadatos del agente."""
            return {
                "name": getattr(instance, "name", None),
                "description": getattr(instance, "description", None),
                "skills": getattr(instance, "skills", []),
                "tools": [
                    {"name": tool.name, "description": tool.description}
                    for tool in getattr(instance, "tools", [])
                ],
            }

        # Adjuntamos la función como un método a la instancia del agente
        setattr(instance, "info", info)

        # --- FIN DE LA MODIFICACIÓN ---

        return instance
