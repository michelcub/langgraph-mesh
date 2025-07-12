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
    """
    Wrapper para crear un agente React.

    Este wrapper simplifica la creación de agentes React al combinar la función `create_react_agent`
    con metadatos adicionales como descripción y habilidades.
    """

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
        """
        Crea una instancia de un agente React.

        Args:
            tools (List[BaseTool]): Lista de herramientas que el agente puede usar.
            store (BaseStore, optional): Almacén para el estado del agente. Defaults to None.
            memory (Checkpointer, optional): Checkpointer para la memoria del agente. Defaults to None.
            name (str, optional): Nombre del agente. Defaults to None.
            model (LanguageModelLike, optional): Modelo de lenguaje a usar. Defaults to None.
            prompt (Prompt, optional): Prompt para el agente. Defaults to None.
            output_schema (StructuredResponseSchema, optional): Esquema de salida estructurado. Defaults to None.
            state_schema (StateSchemaType, optional): Esquema de estado. Defaults to None.
            description (str, optional): Descripción del agente. Defaults to None.
            skills (List[str], optional): Lista de habilidades del agente. Defaults to None.

        Returns:
            Any: Una instancia compilada del agente React.
        """
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
                    {"name": t.name, "description": t.description}
                    for t in tools
                ],
            }

        # Adjuntamos la función como un método a la instancia del agente
        setattr(instance, "info", info)

        # --- FIN DE LA MODIFICACIÓN ---

        return instance
