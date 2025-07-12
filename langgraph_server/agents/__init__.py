"""
Componentes para agentes: locales y remotos
"""

# Componente local (wrapper)
from .agent import Agent

# Componentes remotos (networking)
from .server import Server  # ← Server exportado aquí
from .client import RemoteAgent


__all__ = [
    # 🏠 LOCAL (wrapper para uso local)
    "Agent",
    # 🖥️ SERVER (para alojar agentes)
    "Server",  # ← Alias principal
    # 🌐 CLIENT (para conectar a agentes remotos)
    "RemoteAgent",
]
