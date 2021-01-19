from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaSubscribeProtocol

from random import randint

class RegisterInStore(FipaSubscribeProtocol):

    def __init__(self, agent, message):
        super(RegisterInStore, self).__init__(agent, message, is_initiator=True)

    def handle_agree(self, message):
        display_message(self.agent.aid.localname, "Registered")

    def handle_inform(self, message):
        # display_message(self.agent.aid.localname, message.content)
        self.status = 0

class Worker(Agent):

    def __init__(self, aid, store_aid):
        super(Worker, self).__init__(aid=aid)
        self.production_efficiency = round(randint(20, 100) * 0.01, 2)
        self.happiness = 80
        self.energy = 100
        self.money = 200
        self.shift = 0
        self.store_aid = store_aid

        msg = ACLMessage(ACLMessage.SUBSCRIBE)
        msg.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        msg.set_content("Registering")
        msg.add_receiver(self.store_aid)

        self.call_later(8.0, self.launch_subscriber_protocol, msg)

    def launch_subscriber_protocol(self, message):
        self.resgister = RegisterInStore(self, message)
        self.behaviours.append(self.resgister)
        self.resgister.on_start()

    def on_start(self):
        super(Worker, self).on_start()

        display_message(self.aid.localname, 'p_e: ' + str(self.production_efficiency) + ' m: ' + str(self.money))

