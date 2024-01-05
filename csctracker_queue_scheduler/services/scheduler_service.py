import logging
import threading
import time

import schedule

from csctracker_queue_scheduler.models.generic_data_dto import GenericDataDTO
from csctracker_queue_scheduler.services.queue_service import QueueService
from csctracker_queue_scheduler.utils.utils import Utils


class SchedulerService:
    def __init__(self, queue_service: QueueService, services: list):
        self.logger = logging.getLogger()
        self.queue_service = queue_service
        self.services = services
        self.services.append(self.queue_service)
        threading.Thread(target=self.worker).start()

    def worker(self):
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                self.logger.error(e)
                pass
        pass

    def start_scheduled_job(self, function, args=None, period=5, time_hh_mm="04:00", trigger='minutes'):
        thread = threading.Thread(target=self.start_scheduler,
                                  args=(function, args, period, time_hh_mm, trigger))
        thread.start()

    def start_scheduler(self, function, args=None, period=5, time_hh_mm=None, trigger='minutes'):
        if args is None:
            args = {}
        if trigger == 'seconds':
            schedule.every(period).seconds.do(self.put_in_queue, function, args, True)
        elif trigger == 'minutes':
            schedule.every(period).minutes.do(self.put_in_queue, function, args, True)
        elif trigger == 'hours':
            schedule.every(period).hours.do(self.put_in_queue, function, args, True)
        elif trigger == 'days':
            schedule.every(period).days.do(self.put_in_queue, function, args, True)
        elif trigger == 'weeks':
            schedule.every(period).weeks.do(self.put_in_queue, function, args, True)
        elif trigger == 'daily':
            schedule.every().day.at(time_hh_mm).do(self.put_in_queue, function, args, True)
        if trigger != 'daily':
            self.logger.info(
                f"Job {Utils.get_friendly_method_name(function)}({args if args else ''}) scheduled to run every {period} {trigger}")
        else:
            self.logger.info(
                f"Job {Utils.get_friendly_method_name(function)}({args if args else ''}) scheduled to run at {time_hh_mm}")

    def init_job(self, function, args=None, priority_job=False, class_name=None, async_job=True) -> GenericDataDTO:
        executed = False
        if args is None:
            args = {}
        if 'priority_job' in args:
            priority_job = args['priority_job'] == 'true'
            del args['priority_job']
        if 'async_job' in args:
            async_job = args['async_job'] == 'true'
            del args['async_job']
        if '.' in function:
            classe, method = function.split('.')
            instance = self.get_instance_by_class_name(classe)
            if instance is not None:
                call_method = SchedulerService.call_method(instance, method)
                if async_job:
                    self.queue_service.put(call_method, priority_job, **args)
                else:
                    ret_ = call_method(**args)
                    return GenericDataDTO(msg=ret_)
                executed = True
        else:
            if class_name is not None:
                instance = self.get_instance_by_class_name(class_name)
                if instance is not None:
                    service_call_method = SchedulerService.call_method(instance, function)
                    if async_job:
                        self.queue_service.put(service_call_method, priority_job, **args)
                    else:
                        ret_ = service_call_method(**args)
                        return GenericDataDTO(msg=ret_)
                    executed = True

        if not executed:
            return GenericDataDTO(msg=f'Job {function} not found')
        schedule_type = 'priority' if priority_job else 'normal'
        return GenericDataDTO(msg=f'Job {function} scheduled for execution {schedule_type}')

    @staticmethod
    def call_method(instance, method_name):
        method = getattr(instance, method_name)
        return method

    def put_in_queue(self, function, args=None, priority=False):
        self.queue_service.put(function, priority, **args)

    def get_instance_by_class_name(self, class_name):
        class_name = Utils.snake_to_camel(class_name)
        for instance in self.services:
            if type(instance).__name__ == class_name:
                return instance
        return None
