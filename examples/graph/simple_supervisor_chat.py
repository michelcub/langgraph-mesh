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
from langgraph_server.agents import Agent  # Usa tu clase modificada

llm = ChatOpenAI(
    model="deepseek-r1-0528-qwen3-8b-mlx",
    base_url="http://localhost:1234/v1",
    api_key="sk-fsZnJlTw6u1RllkI3MCIhQ",
)

agente_soporte = Agent(
    name="soporte",
    description="Responde dudas sobre productos, incidencias y asistencia técnica.",
    skills=[
        "resolución de problemas",
        "conocimiento de producto",
        "asistencia técnica",
    ],
    tools=[],  # podrías añadir herramientas tipo "buscarFAQ"
    model=llm,
    prompt="Eres un agente de soporte técnico. Ayudas con dudas, errores y guías de uso.",
)

prompt = (
    "Eres un agente especializado en Recursos Humanos. "
    "Respondes de forma clara y directa a preguntas sobre vacaciones, sueldos, bajas y beneficios. "
    "Simula tener acceso a los datos del usuario y proporciona respuestas plausibles. "
    "Por ejemplo, si te preguntan cuántos días de vacaciones les quedan, responde como si tuvieras esa información. "
    "No digas que vas a transferir la solicitud. Sé resolutivo."
)

agente_hr = Agent(
    name="recursos_humanos",
    description=(
        "Eres un agente especializado en Recursos Humanos. "
        "Respondes de forma clara y directa a preguntas sobre vacaciones, sueldos, bajas y beneficios. "
        "Simula tener acceso a los datos del usuario y proporciona respuestas plausibles. "
        "Por ejemplo, si te preguntan cuántos días de vacaciones les quedan, responde como si tuvieras esa información. "
        "No digas que vas a transferir la solicitud. Sé resolutivo."
    ),
    skills=["normativa laboral", "vacaciones", "beneficios"],
    tools=[],  # podrías añadir herramienta tipo "consultarNomina"
    model=llm,
    prompt="Eres un agente de recursos humanos. Ayudas con temas laborales internos y beneficios.",
)


# Creamos supervisor
supervisor = SupervisorChatGroup(
    agents=[agente_soporte, agente_hr],
    model=llm,
)

# Simulación de consulta del usuario
consulta = HumanMessage(content="¿Cuántos días de vacaciones me quedan este año?")

# Invocación del supervisor
response = supervisor.invoke(
    {"messages": [consulta]}
)

# Mostrar respuesta final
print("\n🧾 RESPUESTA FINAL DEL SUPERVISOR:")
print(response["messages"][-1].content)
