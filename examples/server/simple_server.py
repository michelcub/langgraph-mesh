import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from examples.server.agent import simple_agent

from langgraph_server.agents import Server


server=Server()

server.add_agent(
    agent=simple_agent,
    path='simple_agent',
    name='simple_agent',
    description='Simple Agent for examples',
    skills=['simple', 'agent']
)

server.run()