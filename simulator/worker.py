from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.behaviours.protocols import FipaRequestProtocol

from random import randint

import macros

class RegisterInStore(FipaSubscribeProtocol):

    def __init__(self, agent, message):
        super(RegisterInStore, self).__init__(agent, message, is_initiator=True)

    def handle_agree(self, message):
        display_message(self.agent.aid.localname, "Registered")

    def handle_inform(self, message):
        # display_message(self.agent.aid.localname, message.content)
        self.status = 0

class StartEndShift(FipaRequestProtocol):
    def __init__(self, agent):
        super(StartEndShift, self).__init__(agent=agent, message=None, is_initiator=False)

    def handle_request(self, message):
        if message.ontology == macros.SHIFT_ONTOLOGY:
            super(StartEndShift, self).handle_request(message)

            if self.agent.working == 0:
                self.agent.working = 1
                display_message(self.agent.aid.localname, 'Shift started')
            else:
                self.agent.working = 0
                display_message(self.agent.aid.localname, 'Shift ended')


class ReceiveTask(FipaRequestProtocol):

    def __init__(self, agent):
        super(ReceiveTask, self).__init__(agent=agent,
                                           message=None,
                                           is_initiator=False)

    def handle_request(self, message):
        if message.ontology == macros.TASK_ONTOLOGY:
            super(ReceiveTask, self).handle_request(message)

            display_message(self.agent.aid.localname, 'Received task ' + message.content)

            local_task_efficiency = self.agent.production_efficiency
            # local_task_efficiency = self.agent.get_task_efficiency()

            # Change worker parameters (happiness, energy, etc)
            

            reply = message.create_reply()
            reply.set_performative(ACLMessage.INFORM)
            
            # INFORM with worker task efficiency
            reply.set_content(local_task_efficiency)
            self.agent.send(reply)
        

class Worker(Agent):

    def __init__(self, aid, store_aid):
        super(Worker, self).__init__(aid=aid)
        self.production_efficiency = round(randint(20, 100) * 0.01, 2)

        self.happiness = 0.8
        self.energy = 1.0
        self.money = 200

        self.working = 0

        self.store_aid = store_aid

        self.effort_points = 0
        self.reward_points = 0

        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.set_content("Registering")
        msg.add_receiver(self.store_aid)

        self.call_later(8.0, self.launch_subscriber_protocol, msg)

        self.star_work = StartEndShift(self)
        self.behaviours.append(self.star_work)

        self.receive_task = ReceiveTask(self)
        self.behaviours.append(self.receive_task)


    def launch_subscriber_protocol(self, message):
        self.register = RegisterInStore(self, message)
        self.behaviours.append(self.register)
        self.register.on_start()

    def on_start(self):
        super(Worker, self).on_start()

        display_message(self.aid.localname, 'p_e: ' + str(self.production_efficiency) + ' m: ' + str(self.money))


    # Returns the task effiency which is production_efficiency * happiness * (energy)^2, energy affects the efficiency more
    def get_task_efficiency(self):
        return self.production_efficiency * self.happiness * self.energy * self.energy
