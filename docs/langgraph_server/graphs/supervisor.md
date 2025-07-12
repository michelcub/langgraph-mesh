Module langgraph_server.graphs.supervisor
=========================================

Classes
-------

`SupervisorChatGroup(agents: list[langgraph.pregel.Pregel | langgraph_server.agents.client.RemoteAgent], *, model: langchain_core.runnables.base.Runnable[langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, typing.Any]], langchain_core.messages.base.BaseMessage | str], tools: list[typing.Union[langchain_core.tools.base.BaseTool, typing.Callable]] | langgraph.prebuilt.tool_node.ToolNode | None = None, prompt: langchain_core.messages.system.SystemMessage | str | Callable[[~StateSchema], langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]]] | langchain_core.runnables.base.Runnable[~StateSchema, langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, typing.Any]]] | None = None, response_format: dict | type[pydantic.main.BaseModel] | tuple[str, dict | type[pydantic.main.BaseModel]] | None = None, parallel_tool_calls: bool = False, state_schema: Type[~StateSchema] = None, config_schema: Type[Any] | None = None, output_mode: Literal['full_history', 'last_message'] = 'last_message', add_handoff_messages: bool = True, handoff_tool_prefix: str | None = None, add_handoff_back_messages: bool | None = None, supervisor_name: str = 'supervisor', include_agent_name: Literal['inline'] | None = None)`
:   Crea un grupo de chat supervisado con agentes especializados.
    
    Esta clase facilita la creación de un grafo que incluye un supervisor
    responsable de dirigir el flujo de conversación entre múltiples agentes.

    ### Static methods

    `generate_prompt(agents: list[langgraph.pregel.Pregel]) ‑> langchain_core.messages.system.SystemMessage | str | Callable[[~StateSchema], langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]]] | langchain_core.runnables.base.Runnable[~StateSchema, langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, typing.Any]]]`
    :   Genera un prompt base para el supervisor.

    `infer_tools(agents: list[langgraph.pregel.Pregel]) ‑> list[langchain_core.tools.base.BaseTool]`
    :   Extrae e infiere herramientas únicas de todos los agentes.