from typing import List, Dict, Any, Callable, Optional
import logging


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import jsonpickle
from starlette.responses import StreamingResponse

from langgraph_server.agents import Agent
from langgraph_server.types import AgentMetadata, InvokeParams, StreamParams
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RequestMessage(BaseModel):
    role: str
    content: str


class RequestServer(BaseModel):
    messages: List[RequestMessage]
    stream: Optional[bool] = False


class Server:
    def __init__(self, title: str = "LangGraph Dynamic Server"):
        self.app = FastAPI(title=title)

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # En producción, especifica dominios exactos
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.registered_paths: List[str] = []
        self.agents: Dict[str, Any] = {}

        # Mapeo de métodos de agente a configuraciones de endpoint

        # Endpoints globales
        self.app.get("/health")(self._health_check)

    def add_agent(
        self,
        agent: Any,
        path: str,
        name: str = None,
        description: str = None,
        skills: List[str] = None,
    ):
        """
        Registra un agente y crea endpoints automáticamente para todos sus métodos.

        Args:
            agent: El agente a registrar (Agent wrapper o CompiledStateGraph)
            path: Ruta base del agente (ej: "/math")
            name
            description
            skills
        """
        if skills is None:
            skills = []

        # Validar que la ruta no esté registrada
        if path in self.registered_paths:
            raise RuntimeError(f"Agent path '{path}' already registered")

        # Normalizar path
        if not path.startswith("/"):
            path = "/" + path

        self.registered_paths.append(path)

        # 🎯 DETECCIÓN AUTOMÁTICA DE METADATA DEL AGENT
        agent_metadata: AgentMetadata = {
            "path": path,
            "name": name,
            "description": description,
            "skills": skills,
            "agent": agent,
        }

        # Guardar agente con metadata (automática o manual)
        self.agents[path] = agent_metadata

        def info():
            return agent.info()

        # Crear endpoints para cada método disponible
        async def invoke(request: Request):
            raw_body = await request.body()
            payload = jsonpickle.decode(raw_body)
    
            print("kwargs received and decoded:", payload)
            
            response = agent.invoke(payload)
            print("response", response)            
            return jsonpickle.encode(response)

        async def ainvoke(request: InvokeParams):
            raw_body = await request.body()
            payload = jsonpickle.decode(raw_body)
    
            print("kwargs received and decoded:", payload)
            response = await agent.ainvoke(payload)
            print("response", response)
            return jsonpickle.encode(response)

        async def stream(request: StreamParams):
            raw_body = await request.body()
            payload = jsonpickle.decode(raw_body)
    
            print("kwargs received and decoded:", payload)
            return StreamingResponse(
                content=_event_generator(payload),
                media_type="application/json",
            )

        async def astream(request: StreamParams):
            raw_body = await request.body()
            payload = jsonpickle.decode(raw_body)
    
            print("kwargs received and decoded:", payload)
            return StreamingResponse(
                content=_async_event_generator(payload),
                media_type="application/json",
            )

        async def _async_event_generator(request):
            async for chunk in agent.astream(request):
                print("chunk", chunk)
                yield jsonpickle.encode(chunk.get("agent")) + "\n"

        async def _event_generator(request):
            for chunk in agent.stream(request):
                print("chunk", chunk)
                yield jsonpickle.encode(chunk.get("agent")) + "\n"

        self.app.add_api_route(f"{path}/info", info, methods=["GET"])
        self.app.add_api_route(f"{path}/invoke", invoke, methods=["POST"])
        self.app.add_api_route(f"{path}/ainvoke", ainvoke, methods=["POST"])
        self.app.add_api_route(f"{path}/stream", stream, methods=["POST"])
        self.app.add_api_route(f"{path}/astream", astream, methods=["POST"])

        logger.info(f"Description: {agent_metadata['description']}")

    async def _health_check(self):
        """Health check global del servidor"""
        return {
            "status": "healthy",
            "registered_agents": len(self.registered_paths),
            "agent_paths": self.registered_paths,
        }

    def run(self, host: str = "localhost", port: int = 8000, **kwargs):
        """Ejecuta el servidor con banner ASCII"""

        # 🎨 BANNER ASCII PERSONALIZADO
        self._print_startup_banner(host, port)

        # Mostrar información de agentes registrados
        if self.agents:
            print("📋 Registered Agents:")
            for path, metadata in self.agents.items():
                print(f"   • {path} → {metadata['name']}: {metadata['description']}")
            print()

        logger.info(f"Starting server with {len(self.agents)} agents")

        uvicorn.run(self.app, host=host, port=port, **kwargs)

    def _print_startup_banner(self, host: str, port: int):
        """Imprime el banner ASCII de inicio"""

        # Colores ANSI
        CYAN = "\033[96m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        RESET = "\033[0m"
        BOLD = "\033[1m"

        # Banner ASCII con diseño atractivo
        banner = f"""
{CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  {BOLD}{MAGENTA}██╗      █████╗ ███╗   ██╗ ██████╗  ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗{RESET}{CYAN}  ║
║  {BOLD}{MAGENTA}██║     ██╔══██╗████╗  ██║██╔════╝ ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║{RESET}{CYAN}  ║
║  {BOLD}{MAGENTA}██║     ███████║██╔██╗ ██║██║  ███╗██║  ███╗██████╔╝███████║██████╔╝███████║{RESET}{CYAN}  ║
║  {BOLD}{MAGENTA}██║     ██╔══██║██║╚██╗██║██║   ██║██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║{RESET}{CYAN}  ║
║  {BOLD}{MAGENTA}███████╗██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║{RESET}{CYAN}  ║
║  {BOLD}{MAGENTA}╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝{RESET}{CYAN}  ║
║                                                                      ║
║                    {BOLD}{YELLOW}🚀 S E R V E R   S T A R T I N G 🚀{RESET}{CYAN}                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
"""

        # Información del servidor
        server_info = f"""
{GREEN}┌─────────────────────────────────────────────────────────────┐
│  {BOLD}🌐 Server Information{RESET}{GREEN}                                     │
├─────────────────────────────────────────────────────────────┤
│  📡 Host: {BOLD}{YELLOW}{host}{RESET}{GREEN}                                           │
│  🔌 Port: {BOLD}{YELLOW}{port}{RESET}{GREEN}                                              │
│  🔗 URL:  {BOLD}{BLUE}http://{host}:{port}{RESET}{GREEN}                           │
│  📚 Docs: {BOLD}{BLUE}http://{host}:{port}/docs{RESET}{GREEN}                      │
│  ❤️  Health: {BOLD}{BLUE}http://{host}:{port}/health{RESET}{GREEN}                   │
│  🤖 Agents: {BOLD}{YELLOW}{len(self.agents)} registered{RESET}{GREEN}                              │
└─────────────────────────────────────────────────────────────┘{RESET}
"""

        # Imprimir todo
        print(banner)
        print(server_info)

        # Endpoints disponibles si hay agentes
        if self.agents:
            endpoints_info = f"""
{BLUE}┌─────────────────────────────────────────────────────────────┐
│  {BOLD}🔧 Available Endpoints{RESET}{BLUE}                                   │
├─────────────────────────────────────────────────────────────┤"""

            for path, metadata in self.agents.items():
                agent_name = metadata["name"]
                endpoints_info += f"""
│  {BOLD}{CYAN}{path}{RESET}{BLUE} → {agent_name}                                    │
│    📤 POST {BOLD}{path}/invoke{RESET}{BLUE}                                │
│    ℹ️  GET  {BOLD}{path}/info{RESET}{BLUE}                                  │
│    ❤️  GET  {BOLD}{path}/health{RESET}{BLUE}                                │"""

            endpoints_info += f"""
└─────────────────────────────────────────────────────────────┘{RESET}
"""
            print(endpoints_info)

        # Mensaje final
        print(
            f"{BOLD}{GREEN}🎯 LangGraph Server is ready! Press Ctrl+C to stop.{RESET}"
        )
        print()
