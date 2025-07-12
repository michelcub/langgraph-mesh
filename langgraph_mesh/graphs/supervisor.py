from typing import Type, Any, Optional, Union, Callable

from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt.chat_agent_executor import (
    StateSchemaType,
    StructuredResponseSchema,
    Prompt,
)
from langgraph.pregel import Pregel
from langgraph_supervisor.agent_name import AgentNameMode
from langgraph_supervisor.supervisor import OutputMode, create_supervisor

from langgraph_server.agents import RemoteAgent


class SupervisorChatGroup:
    def __new__(
        self,
        agents: list[Pregel | RemoteAgent],
        *,
        model: LanguageModelLike,
        tools: list[BaseTool | Callable] | ToolNode | None = None,
        prompt: Prompt | None = None,
        response_format: Optional[
            Union[
                StructuredResponseSchema,
                tuple[str, StructuredResponseSchema],
            ]
        ] = None,
        parallel_tool_calls: bool = False,
        state_schema: StateSchemaType = None,
        config_schema: Type[Any] | None = None,
        output_mode: OutputMode = "last_message",
        add_handoff_messages: bool = True,
        handoff_tool_prefix: Optional[str] = None,
        add_handoff_back_messages: Optional[bool] = None,
        supervisor_name: str = "supervisor",
        include_agent_name: AgentNameMode | None = None,
    ):
        # Paso 1: Generar prompt base
        base_prompt = SupervisorChatGroup.generate_prompt(agents)

        # Paso 2: Combinar con prompt extra si existe
        if prompt is not None:
            final_prompt = Prompt.from_text(
                f"{base_prompt.text}\n\n---\n\n{prompt.text}"
            )
        else:
            final_prompt = base_prompt

        # Paso 3: Inferir herramientas si no se pasan
        if tools is None:
            tools = SupervisorChatGroup.infer_tools(agents)

        # Paso 4: Crear supervisor
        instance = create_supervisor(
            agents=agents,
            model=model,
            tools=tools,
            prompt=final_prompt,
            response_format=response_format,
            parallel_tool_calls=parallel_tool_calls,
            state_schema=state_schema,
            config_schema=config_schema,
            output_mode=output_mode,
            add_handoff_messages=add_handoff_messages,
            handoff_tool_prefix=handoff_tool_prefix,
            add_handoff_back_messages=add_handoff_back_messages,
            supervisor_name=supervisor_name,
            include_agent_name=include_agent_name,
        )
        return instance.compile()

    @staticmethod
    def generate_prompt(agents: list[Pregel]) -> Prompt:
        descriptions = []
        for agent in agents:
            if hasattr(agent, "info") and callable(agent.info):
                agent_info = agent.info()
                name = agent_info.get("name", "Desconocido")
                desc = agent_info.get("description", "Sin descripción.")
                skills = ", ".join(agent_info.get("skills", [])) or "No especificadas"
                tools = (
                    "\n".join(
                        [
                            f"- {t['name']}: {t['description']}"
                            for t in agent_info.get("tools", [])
                        ]
                    )
                    or "No tiene herramientas"
                )
                agent_block = (
                    f"### Agente: {name}\n"
                    f"Descripción: {desc}\n"
                    f"Habilidades: {skills}\n"
                    f"Herramientas:\n{tools}"
                )
                descriptions.append(agent_block)
            else:
                descriptions.append("Agente sin información.")

        prompt_text = (
            "Eres un supervisor responsable de dirigir los siguientes agentes especializados.\n"
            "Cada agente tiene habilidades y herramientas distintas. Según la tarea, "
            "elige el agente más adecuado para ejecutarla.\n\n"
            + "\n\n".join(descriptions)
            + "\n\nUsa esta información para tomar decisiones informadas."
        )

        return prompt_text

    @staticmethod
    def infer_tools(agents: list[Pregel]) -> list[BaseTool]:
        """Extrae e infiere herramientas únicas de todos los agentes."""
        seen = set()
        inferred_tools = []

        for agent in agents:
            agent_tools = getattr(agent, "tools", [])
            for tool in agent_tools:
                if tool.name not in seen:
                    seen.add(tool.name)
                    inferred_tools.append(tool)

        return inferred_tools
