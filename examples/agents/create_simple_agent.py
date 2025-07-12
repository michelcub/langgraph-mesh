import sys
import os
from pyexpat.errors import messages

from click import prompt
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from langgraph_server.agents import Agent

from langchain_core.callbacks.base import BaseCallbackHandler

class MyLoggingCallback(BaseCallbackHandler):
    def on_chain_start(self, serialized, inputs, **kwargs):
        print("🔄 Inicio del paso:", serialized)
        print("📥 Input:", inputs)

    def on_chain_end(self, outputs, **kwargs):
        print("✅ Fin del paso. Output:", outputs)
        print("kwargs", kwargs)
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("🧠 LLM llamado con prompts:", prompts)

    def on_llm_end(self, response, **kwargs):
        print("🧠 LLM respondió:", response)

    def on_tool_start(self, serialized, input_str, **kwargs):
        print("🔧 Herramienta llamada:", serialized.get("name", "unknown"))
        print("📥 Input a la herramienta:", input_str)

    def on_tool_end(self, output, **kwargs):
        print("🔧 Resultado de la herramienta:", output)


llm = ChatOpenAI(
    model= "deepseek-r1-0528-qwen3-8b-mlx",
    base_url="http://localhost:1234/v1",
    api_key="sk-fsZnJlTw6u1RllkI3MCIhQ",
)

prompt = "Eres una agente de prueba siempre que te pregunten algo tienes que comenzar diciendo que eres una agente de prueba"

simple_agent = Agent(
    name='simple_agent',
    model=llm,
    tools=[],
    prompt=prompt
)

data = {
    "messages": [
        HumanMessage(content="Hola")
    ]
}

response = simple_agent.invoke(data, config={
        "callbacks": [MyLoggingCallback()]
    })

