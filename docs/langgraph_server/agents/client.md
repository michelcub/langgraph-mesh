Module langgraph_server.agents.client
=====================================

Classes
-------

`RemoteAgent(path: str)`
:   Cliente para interactuar con un agente remoto.
    
    Esta clase permite invocar, transmitir y obtener información de un agente
    que se ejecuta en un servidor remoto.
    
    Inicializa el cliente del agente remoto.
    
    Args:
        path (str): La URL base del servidor del agente remoto.

    ### Methods

    `ainvoke(self, input: ~InputT, config: langchain_core.runnables.config.RunnableConfig | None = None, *, stream_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] = 'values', print_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] | Sequence[Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']] = (), output_keys: str | Sequence[str] | None = None, interrupt_before: Literal['*'] | Sequence[str] | None = None, interrupt_after: Literal['*'] | Sequence[str] | None = None, **kwargs: Any) ‑> dict[str, typing.Any] | typing.Any`
    :   Invoca el agente remoto de forma asíncrona.
        
        Args:
            input (InputT): La entrada para el agente.
            config (RunnableConfig | None = None, optional): Configuración para la ejecución. Defaults to None.
            stream_mode (StreamMode = "values", optional): Modo de transmisión. Defaults to "values".
            print_mode (StreamMode | Sequence[StreamMode] = (), optional): Modo de impresión. Defaults to ().
            output_keys (str | Sequence[str] | None = None, optional): Claves de salida. Defaults to None.
            interrupt_before (All | Sequence[str] | None = None, optional): Interrupciones antes de la ejecución. Defaults to None.
            interrupt_after (All | Sequence[str] | None = None, optional): Interrupciones después de la ejecución. Defaults to None.
            **kwargs (Any): Argumentos adicionales.
        
        Returns:
            dict[str, Any] | Any: La respuesta del agente.

    `astream(self, input: ~InputT, config: langchain_core.runnables.config.RunnableConfig | None = None, *, stream_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] | Sequence[Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']] | None = None, print_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] | Sequence[Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']] = (), output_keys: str | Sequence[str] | None = None, interrupt_before: Literal['*'] | Sequence[str] | None = None, interrupt_after: Literal['*'] | Sequence[str] | None = None, checkpoint_during: bool | None = None, debug: bool | None = None, subgraphs: bool = False) ‑> AsyncIterator[dict[str, Any] | Any]`
    :   Transmite la salida del agente remoto de forma asíncrona.
        
        Args:
            input (InputT): La entrada para el agente.
            config (RunnableConfig | None = None, optional): Configuración para la ejecución. Defaults to None.
            stream_mode (StreamMode | Sequence[StreamMode] | None = None, optional): Modo de transmisión. Defaults to None.
            print_mode (StreamMode | Sequence[StreamMode] = (), optional): Modo de impresión. Defaults to ().
            output_keys (str | Sequence[str] | None = None, optional): Claves de salida. Defaults to None.
            interrupt_before (All | Sequence[str] | None = None, optional): Interrupciones antes de la ejecución. Defaults to None.
            interrupt_after (All | Sequence[str] | None = None, optional): Interrupciones después de la ejecución. Defaults to None.
            checkpoint_during (bool | None = None, optional): Checkpoint durante la ejecución. Defaults to None.
            debug (bool | None = None, optional): Modo de depuración. Defaults to None.
            subgraphs (bool = False, optional): Incluir subgrafos. Defaults to False.
        
        Yields:
            AsyncIterator[dict[str, Any] | Any]: Los chunks de la respuesta del agente.

    `info(self)`
    :   Obtiene información sobre el agente remoto.
        
        Returns:
            dict: Un diccionario con la información del agente.

    `invoke(self, input: ~InputT, config: langchain_core.runnables.config.RunnableConfig | None = None, *, stream_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] = 'values', print_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] | Sequence[Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']] = (), output_keys: str | Sequence[str] | None = None, interrupt_before: Literal['*'] | Sequence[str] | None = None, interrupt_after: Literal['*'] | Sequence[str] | None = None, **kwargs: Any) ‑> dict[str, typing.Any] | typing.Any`
    :   Invoca el agente remoto de forma síncrona.
        
        Args:
            input (InputT): La entrada para el agente.
            config (RunnableConfig | None, optional): Configuración para la ejecución. Defaults to None.
            stream_mode (StreamMode, optional): Modo de transmisión. Defaults to "values".
            print_mode (StreamMode | Sequence[StreamMode], optional): Modo de impresión. Defaults to ().
            output_keys (str | Sequence[str] | None, optional): Claves de salida. Defaults to None.
            interrupt_before (All | Sequence[str] | None = None, optional): Interrupciones antes de la ejecución. Defaults to None.
            interrupt_after (All | Sequence[str] | None = None, optional): Interrupciones después de la ejecución. Defaults to None.
            **kwargs (Any): Argumentos adicionales.
        
        Returns:
            dict[str, Any] | Any: La respuesta del agente.

    `stream(self, input: ~InputT, config: langchain_core.runnables.config.RunnableConfig | None = None, *, stream_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] | Sequence[Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']] | None = None, print_mode: Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom'] | Sequence[Literal['values', 'updates', 'checkpoints', 'tasks', 'debug', 'messages', 'custom']] = (), output_keys: str | Sequence[str] | None = None, interrupt_before: Literal['*'] | Sequence[str] | None = None, interrupt_after: Literal['*'] | Sequence[str] | None = None, checkpoint_during: bool | None = None, debug: bool | None = None, subgraphs: bool = False) ‑> Iterator[dict[str, Any] | Any]`
    :   Transmite la salida del agente remoto de forma síncrona.
        
        Args:
            input (InputT): La entrada para el agente.
            config (RunnableConfig | None = None, optional): Configuración para la ejecución. Defaults to None.
            stream_mode (StreamMode | Sequence[StreamMode] | None = None, optional): Modo de transmisión. Defaults to None.
            print_mode (StreamMode | Sequence[StreamMode] = (), optional): Modo de impresión. Defaults to ().
            output_keys (str | Sequence[str] | None = None, optional): Claves de salida. Defaults to None.
            interrupt_before (All | Sequence[str] | None = None, optional): Interrupciones antes de la ejecución. Defaults to None.
            interrupt_after (All | Sequence[str] | None = None, optional): Interrupciones después de la ejecución. Defaults to None.
            checkpoint_during (bool | None = None, optional): Checkpoint durante la ejecución. Defaults to None.
            debug (bool | None = None, optional): Modo de depuración. Defaults to None.
            subgraphs (bool = False, optional): Incluir subgrafos. Defaults to False.
        
        Yields:
            Iterator[dict[str, Any] | Any]: Los chunks de la respuesta del agente.