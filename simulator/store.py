from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.behaviours.protocols import TimedBehaviour

import datetime
import random

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

        self.create_shifts_hour = 5
        self.create_shifts_day = 1

    def on_time(self):
        super(PassTime, self).on_time()
        self.agent.date = self.agent.date + datetime.timedelta(hours=1)

        if self.agent.date.hour == self.create_shifts_hour and self.agent.date.day == self.create_shifts_day:
            self.createShifts()

        if self.agent.date.hour == 6:
            self.setShifts(self.agent.date.day)
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        message.set_content(self.agent.date)
        self.notify(message)

    def createShifts(self):
        number_of_days = utils.daysOfMonth(self.agent.date.month)
        workers = utils.getWorkers(self.agent.workers_aid)
        self.agent.schedule = [[] for i in range(number_of_days)]

        day_off_tracker = list()
        for day in range(number_of_days):

            # in pos 0 is day off, 1 is morning, 2 is afternoon
            day_shift = [[] for i in range(3)]
            if len(day_off_tracker) == len(workers):
                day_off_tracker = list()

            random.shuffle(workers)

            for worker in workers:
                if (worker not in day_off_tracker) and (len(day_shift[0]) < self.agent.number_of_workers//3):
                    day_shift[0].append(worker)
                    day_off_tracker.append(worker)
                    continue
                elif (worker not in day_shift[0]) and (len(day_shift[1]) < self.agent.number_of_workers//3):
                    day_shift[1].append(worker)
                    continue
                elif (worker not in day_shift[1]) and (len(day_shift[2]) < self.agent.number_of_workers//3):
                    day_shift[2].append(worker)
                    continue
                else:
                    day_shift[random.randint(1,2)].append(worker)


            self.agent.schedule[day] = day_shift

    def setShifts(self, day):
        self.agent.morning_shift = self.agent.schedule[day][1]
        self.agent.afternoon_shift = self.agent.schedule[day][2]


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
        self.schedule =  list()

        self.date = datetime.datetime(2020, 1, 1)

        self.register = RegisterWorkers(self)

        self.behaviours.append(self.register)

        self.debug_info = DisplayStoreInfo(self, 1.0)
        self.behaviours.append(self.debug_info)

        self.call_later(10.0, self.launch_pass_time)

    def launch_pass_time(self):
        self.pass_time = PassTime(self, 1.0, self.register.notify)
        self.behaviours.append(self.pass_time)
        self.pass_time.on_start()

    def on_start(self):
        super(Store, self).on_start()
        display_message(self.aid.localname, 'store initalized')
