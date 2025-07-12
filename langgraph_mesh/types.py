from typing import TypedDict, List
from langgraph_server.agents import Agent
from typing import Sequence, Union, Any, Optional
from pydantic import BaseModel
from langgraph.typing import InputT
class AgentMetadata(TypedDict):
    agent: Agent | None
    name: str | None
    description: str | None
    skills: List[str]
    path: str | None



# Para invoke y ainvoke
class InvokeParams(BaseModel):
    input: Any
    config: Optional[Any] = None  # RunnableConfig | None

    stream_mode: Union[str, Sequence[str]] = "values"
    print_mode: Union[Sequence[str], str] = ()
    output_keys: Optional[Union[str, Sequence[str]]] = None

    interrupt_before: Optional[Union[str, Sequence[str]]] = None  # Usando str para All por simplicidad
    interrupt_after: Optional[Union[str, Sequence[str]]] = None

    class Config:
        arbitrary_types_allowed = True

# Para stream y astream
class StreamParams(BaseModel):
    input: Any
    config: Optional[Any] = None  # RunnableConfig | None

    stream_mode: Optional[Union[str, Sequence[str]]] = None
    print_mode: Union[Sequence[str], str] = ()
    output_keys: Optional[Union[str, Sequence[str]]] = None

    interrupt_before: Optional[Union[str, Sequence[str]]] = None
    interrupt_after: Optional[Union[str, Sequence[str]]] = None

    checkpoint_during: Optional[bool] = None
    debug: Optional[bool] = None
    subgraphs: bool = False

    class Config:
        arbitrary_types_allowed = True


