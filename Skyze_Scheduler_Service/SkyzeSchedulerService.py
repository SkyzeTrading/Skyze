# 3rd Party Libraries
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from random import randint

# Skyze Imports
from Skyze_Standard_Library.SkyzeServiceAbstract import *
# Messages
from Skyze_Messaging_Service.Messages.MessageMarketDataUpdaterRun import MessageMarketDataUpdaterRun
from Skyze_Messaging_Service.Messages.MessageMarketDataUpdaterRunAll import MessageMarketDataUpdaterRunAll
from Skyze_Messaging_Service.Messages.MessageScreenerRun import MessageScreenerRun
from Skyze_Messaging_Service.Messages.MessageSchedulerRun import MessageSchedulerRun
from Skyze_Messaging_Service.Messages.MessageSchedulerTest import MessageSchedulerTest


class SkyzeSchedulerService(SkyzeServiceAbstract):
    """Skyze inter-service message logger"""

    def __init__(self, message_bus):
        """Constructor"""
        #self.__message_bus = None
        path_to_service = "Skyze_Scheduler_Service"
        super().__init__(message_bus=message_bus, log_path=path_to_service)

    def __sendMessage(self, message):
        self._message_bus.publishMessage(message)

    def test(self):
        start_time = datetime.now()
        print('=== Skyze Scheduler TEST RUN ========== ' +
              str(start_time) + ' ========== ')
        print()

        sched = BlockingScheduler()

        message_list = [
            MessageMarketDataUpdaterRun("Poloniex", "BTCUSD", "1_Hour"),
            MessageMarketDataUpdaterRunAll("Cryptopia"),
            MessageScreenerRun("Mike's Screener")
        ]

        for i in range(1, 10):
            msg_number = randint(0, 2)
            msg = message_list[msg_number]
            self._sendMessage(msg)
        print(f"Test Messages published")

    def send_random_message(self):

        message_list = [
            MessageMarketDataUpdaterRun("Poloniex", "BTCUSD", "1_Hour"),
            MessageMarketDataUpdaterRunAll("Cryptopia"),
            MessageScreenerRun("Mike's Screener")
        ]

        print(f"Sending random message - {datetime.now()} - {msg.getJSON()}")
        msg_number = randint(0, 2)
        msg = message_list[msg_number]
        self._sendMessage(msg)

    def start(self):
        start_time = datetime.now()
        print('=== Skyze Scheduler ========== ' +
              str(start_time) + ' ========== ')
        print()

        sched = BlockingScheduler()

        job = sched.add_job(self.send_random_message, 'interval', minutes=1)

        @sched.scheduled_job('cron', day_of_week='mon-sun', hour='0-23')
        def cryptopia_hourly_update():
            message = 'Scheduler:: Triggering:: cryptopia_hourly_update'
            print(message)
            send_message(message)

        """Fold this back into start function when ready"""
        @sched.scheduled_job('cron', day_of_week='mon-sun', hour=14, minute=30)
        def cmc_daily_update():
            message = 'Scheduler:: Triggering:: CMC all markets Daily Update at 2:30pm.'
            print(message)
            send_message(message)

        @sched.scheduled_job('cron', day_of_week='mon-sun', hour=10, minute=12)
        def poloniex_daily_update():
            message = 'Scheduler:: Triggering:: Poloniex all markets Daily Update at 10:12am'
            print(message)
            send_message(message)

        sched.print_jobs()
        sched.start()
        print("SCHEDULER END OF START FUNCTION\n\n")

    def receiveMessage(self, message_received):
        """Gets the mssage from the bus and routes internally"""
        # Route to appropriate service
        message_type = message_received.getMessageType()
        if message_type == SkyzeMessageType.SCHEDULER_RUN:
            self.start()
        elif message_type == SkyzeMessageType.SCHEDULER_TEST:
            self.test()
        else:
            self._unknownMessageTypeError(message_received)
