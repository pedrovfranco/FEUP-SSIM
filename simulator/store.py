from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.behaviours.protocols import TimedBehaviour
from pade.behaviours.protocols import FipaRequestProtocol

import datetime
import random

import utils
import macros
import epgp_table

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
        elif self.agent.date.hour == 8:
            self.startEndShift(self.agent.morning_shift)
        elif self.agent.date.hour == 16:
            self.startEndShift(self.agent.morning_shift)
            self.startEndShift(self.agent.afternoon_shift)
        elif self.agent.date.hour == 0:
            self.startEndShift(self.agent.afternoon_shift)
            self.closeStore()
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        message.set_content(self.agent.date)
        self.notify(message)

        # Start distributing tasks
        display_message(self.agent.aid.localname, "Starting distributing tasks")
        current_shift = self.agent.get_current_shift()
       
        if current_shift != None:
            display_message(self.agent.aid.localname, current_shift)
        
            for worker_name in current_shift:
                message = ACLMessage(ACLMessage.REQUEST)
                message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
                message.set_ontology(macros.TASK_ONTOLOGY)
                message.add_receiver(worker_name)
                message.set_content(str(self.agent.date))
                self.agent.send(message)


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

    def closeStore(self):
        self.agent.morning_shift = list()
        self.agent.afternoon_shift = list()

    def startEndShift(self, names):

        for name in names:
            receiver_aid = None
            for worker in self.agent.workers_aid:
                if worker.localname == name:
                    receiver_aid = worker
                    break
            message = ACLMessage(ACLMessage.REQUEST)
            message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
            message.set_ontology(macros.SHIFT_ONTOLOGY)
            message.add_receiver(receiver_aid)
            message.set_content('Change work')
            self.agent.send(message)



class DisplayStoreInfo(TimedBehaviour):
    def __init__(self, agent, time):
        super(DisplayStoreInfo, self).__init__(agent, time)


    def on_time(self):
        super(DisplayStoreInfo, self).on_time()
        display_message(self.agent.aid.localname, "Number_of_workers: " + str(self.agent.number_of_workers) + "\n"
                                                + "Workers_aid: " + utils.AIDToString(self.agent.workers_aid) + "\n"
                                                + "Morning_shift: " + utils.listToString(self.agent.morning_shift) + "\n"
                                                + "Afternoon_shift: " + utils.listToString(self.agent.afternoon_shift) + "\n"
                                                + "Date: " + str(self.agent.date) + "\n")


class DistributeTasks(FipaRequestProtocol):

    def __init__(self, agent):
        super(DistributeTasks, self).__init__(agent=agent,
                                           message=None,
                                           is_initiator=True)


    def handle_inform(self, message):
        if message.ontology == macros.TASK_ONTOLOGY:

            self.agent.epgp.add_ep(self.message.sender.localname, macros.MAX_TASK_EP * float(message.content))

            # display_message(self.agent.aid.localname, message.content)
            # display_message(self.agent.aid.localname, self.agent.epgp.table)



class Store(Agent):

    def __init__(self, aid):
        super(Store, self).__init__(aid=aid)
        self.number_of_workers = 0
        self.workers_aid = list()
        self.morning_shift= list()
        self.afternoon_shift= list()
        self.schedule =  list()
        self.epgp = epgp_table.Epgp_table()

        self.date = datetime.datetime(2020, 1, 1)

        self.register = RegisterWorkers(self)
        self.behaviours.append(self.register)

        self.debug_info = DisplayStoreInfo(self, 1.0)
        self.behaviours.append(self.debug_info)

        self.call_later(10.0, self.launch_pass_time)

        self.distribute_tasks = DistributeTasks(self)
        self.behaviours.append(self.distribute_tasks)
        

    def launch_pass_time(self):
        self.pass_time = PassTime(self, 1.0, self.register.notify)
        self.behaviours.append(self.pass_time)
        self.pass_time.on_start()

    def on_start(self):
        super(Store, self).on_start()
        display_message(self.aid.localname, 'store initalized')
    

    def get_current_shift(self):
        
        if self.date.hour >= 8 and self.date.hour < 16:
            return self.morning_shift
    
        elif self.date.hour >= 16:
            return self.afternoon_shift

        else:
            return []

    
