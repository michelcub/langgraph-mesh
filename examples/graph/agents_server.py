import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from langgraph_server.agents import Server

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from langgraph_server.agents import Agent  # Usa tu clase modificada
from langchain_core.tools import tool

@tool
def saldo_vacaciones() -> str:
    """
    Consulta a base de datos para obtener el saldo de vacaciones.
    """
    return "Tienes 10 días de vacaciones restantes."


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
    """
    Eres un agente especializado en Recursos Humanos. 
    Respondes de forma clara y directa a preguntas sobre vacaciones, sueldos, bajas y beneficios. 
    
    Tools disponibles:
    - saldo_vacaciones: Consulta el saldo de vacaciones del usuario.
    
    Para preguntas de saldo de vacaciones usa la herramienta `saldo_vacaciones`, una veces que la hayas invocado, no es necesario volver a usarla.
    Retorna la respuesta directamente al usuario, no digas que vas a transferir la solicitud. Sé resolutivo.
    
    Siempre responde de forma clara y directa, simulando tener acceso a los datos del usuario pero responde siempre.
    
    """
)

agente_hr = Agent(
    name="recursos_humanos",
    description=(
        "Agente especializado en Recursos Humanos. "
    ),
    skills=["normativa laboral", "vacaciones", "beneficios"],
    tools=[saldo_vacaciones],  # podrías añadir herramienta tipo "consultarNomina"
    model=llm,
    prompt=prompt,
)



server = Server()

server.add_agent(
    agent=agente_hr,
    path="/rrhh",
    name="Recursos Humanos",
    description="Agente de Recursos Humanos",
    skills=["recursos humanos", "empleados"],
)

server.add_agent(
    agent=agente_soporte,
    path="/soporte",
    name="Soporte Técnico",
    description="Agente de soporte técnico",
    skills=["soporte", "tecnico"],
)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8000)
