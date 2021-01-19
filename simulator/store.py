from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.behaviours.protocols import TimedBehaviour

import datetime

import utils

class RegisterWorkers(FipaSubscribeProtocol):

    def __init__(self, agent):
        super(RegisterWorkers, self).__init__(agent, message=None, is_initiator=False)

    def handle_subscribe(self, message):
        self.register(message.sender)

        self.agent.workers_aid.append(message.sender)
        self.agent.number_of_workers += 1

        reply = message.create_reply()
        reply.set_performative(ACLMessage.AGREE)
        reply.set_content(self.agent.number_of_workers)
        self.agent.send(reply)

    def handle_cancel(self, message):
        self.deregister(self, message.sender)

        self.agent.workers_aid.remove(message.content)
        self.agent.number_of_workers -= 1

        display_message(self.agent.aid.localname, message.content)

    def notify(self, message):
        super(RegisterWorkers, self).notify(message)


class PassTime(TimedBehaviour):
    def __init__(self, agent, time, notify):
        super(PassTime, self).__init__(agent, time)
        self.notify = notify

    def on_time(self):
        super(PassTime, self).on_time()
        self.agent.date = self.agent.date + datetime.timedelta(hours=1)
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        message.set_content(self.agent.date)
        self.notify(message)

class DisplayStoreInfo(TimedBehaviour):
    def __init__(self, agent, time):
        super(DisplayStoreInfo, self).__init__(agent, time)


    def on_time(self):
        super(DisplayStoreInfo, self).on_time()
        display_message(self.agent.aid.localname, "Number_of_workers: " + str(self.agent.number_of_workers) + "\n"
                                                + "Workers_aid: " + utils.AIDToString(self.agent.workers_aid) + "\n"
                                                + "Morning_shift: " + utils.AIDToString(self.agent.morning_shift) + "\n"
                                                + "Afternoon_shift: " + utils.AIDToString(self.agent.afternoon_shift) + "\n"
                                                + "Date: " + str(self.agent.date) + "\n")


class Store(Agent):

    def __init__(self, aid):
        super(Store, self).__init__(aid=aid)
        self.number_of_workers = 0
        self.workers_aid = list()
        self.morning_shift= list()
        self.afternoon_shift= list()

        self.date = datetime.datetime(2020, 1, 1)

        self.register = RegisterWorkers(self)
        self.pass_time = PassTime(self, 1.0, self.register.notify)


        self.behaviours.append(self.pass_time)
        self.behaviours.append(self.register)

        self.debug_info = DisplayStoreInfo(self, 1.0)
        self.behaviours.append(self.debug_info)

    def on_start(self):
        super(Store, self).on_start()
        display_message(self.aid.localname, 'store initalized')
