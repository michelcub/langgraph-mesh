Module langgraph_server.agents.agent
====================================

Classes
-------

`Agent(tools: List[langchain_core.tools.base.BaseTool], store: langgraph.store.base.BaseStore = None, memory: bool | langgraph.checkpoint.base.BaseCheckpointSaver | None = None, name: str = None, model: langchain_core.runnables.base.Runnable[langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, typing.Any]], langchain_core.messages.base.BaseMessage | str] = None, prompt: langchain_core.messages.system.SystemMessage | str | Callable[[~StateSchema], langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]]] | langchain_core.runnables.base.Runnable[~StateSchema, langchain_core.prompt_values.PromptValue | str | Sequence[langchain_core.messages.base.BaseMessage | list[str] | tuple[str, str] | str | dict[str, typing.Any]]] = None, output_schema: dict | type[pydantic.main.BaseModel] = None, state_schema: Type[~StateSchema] = None, description: str | None = None, skills: List[str] | None = None)`
:   Wrapper para crear un agente React.
    
    Este wrapper simplifica la creación de agentes React al combinar la función `create_react_agent`
    con metadatos adicionales como descripción y habilidades.