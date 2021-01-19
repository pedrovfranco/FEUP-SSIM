from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.behaviours.protocols import TimedBehaviour

from datetime import datetime
from sys import argv
from time import sleep

import worker
import store


if __name__ == '__main__':

    agents_per_process = 6
    c = 0
    agents = list()

    port = int(argv[1]) + c
    agent_name = 'worker_{}@localhost:{}'.format(port, port)
    agente_store = store.Store(AID(name=agent_name))
    agents.append(agente_store)
    c += 1000

    for i in range(agents_per_process):
        port = int(argv[1]) + c
        agent_name = 'worker_{}@localhost:{}'.format(port, port)
        agente_worker = worker.Worker(AID(name=agent_name), agente_store.aid)
        agents.append(agente_worker)
        c += 1000


    start_loop(agents)