import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from langchain_core.messages import HumanMessage
from langchain_core.callbacks.base import BaseCallbackHandler

from langgraph_server.graphs.supervisor import (
    SupervisorChatGroup,
)  # tu clase mejorada
from langgraph_supervisor.agent_name import AgentNameMode





from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langgraph_server.agents import Agent, RemoteAgent  # Usa tu clase modificada

llm = ChatOpenAI(
    model="deepseek-r1-0528-qwen3-8b-mlx",
    base_url="http://localhost:1234/v1",
    api_key="sk-fsZnJlTw6u1RllkI3MCIhQ",
)

agente_soporte = RemoteAgent("http://localhost:8000/soporte")
agente_hr = RemoteAgent("http://localhost:8000/rrhh")

# Creamos supervisor
supervisor = SupervisorChatGroup(
    agents=[agente_soporte, agente_hr],
    model=llm,
)

# Simulación de consulta del usuario
consulta = HumanMessage(content="¿Cuantos dias de vacaciones me quedan, mi usuario k29@company.com?")

# Invocación del supervisor
response = supervisor.invoke(
    {"messages": [consulta]}
    #{"messages": [consulta]}, config={"callbacks": [MyLoggingCallback()]}
)

# Mostrar respuesta final
print("\n🧾 RESPUESTA FINAL DEL SUPERVISOR:")
print(response["messages"][-1].content)
