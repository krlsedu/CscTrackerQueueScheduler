import logging
import threading
import time

import schedule

from csctracker_queue_scheduler.models.enums.time_unit import TimeUnit
from csctracker_queue_scheduler.models.generic_data_dto import GenericDataDTO
from csctracker_queue_scheduler.services.queue_service import QueueService
from csctracker_queue_scheduler.utils.utils import Utils


class SchedulerService:
    __queue_service = None
    __logger = logging.getLogger()
    __services = []

    @staticmethod
    def init(threads: int = None, services: list = []):
        SchedulerService.__queue_service = QueueService(threads=threads)
        SchedulerService.__services = services
        SchedulerService.__services.append(SchedulerService.__queue_service)
        threading.Thread(target=SchedulerService.__worker).start()

    @staticmethod
    def get_queue_service():
        return SchedulerService.__queue_service

    @staticmethod
    def add_services(services: list):
        SchedulerService.__services.append(services)

    @staticmethod
    def __worker():
        while True:
            try:
                schedule.run_pending()
                time.sleep(1)
            except Exception as e:
                SchedulerService.__logger.error(e)
                pass
        pass

    @staticmethod
    def start_scheduled_job(function,
                            args=None,
                            period=5,
                            time_hh_mm=None,
                            time_unit: TimeUnit = TimeUnit.MINUTES):
        if SchedulerService.__queue_service is None:
            SchedulerService.init()
        thread = threading.Thread(target=SchedulerService.__start_scheduler,
                                  args=(function, args, period, time_hh_mm, time_unit))
        thread.start()

    @staticmethod
    def __start_scheduler(function, args=None, period=5, time_hh_mm=None,
                          time_unit: TimeUnit = TimeUnit.MINUTES):
        if args is None:
            args = {}
        if time_unit == TimeUnit.SECONDS:
            schedule.every(period).seconds.do(SchedulerService.put_in_queue, function, args, True)
        elif time_unit == TimeUnit.MINUTES:
            schedule.every(period).minutes.do(SchedulerService.put_in_queue, function, args, True)
        elif time_unit == TimeUnit.HOURS:
            schedule.every(period).hours.do(SchedulerService.put_in_queue, function, args, True)
        elif time_unit == TimeUnit.DAYS:
            schedule.every(period).days.do(SchedulerService.put_in_queue, function, args, True)
        elif time_unit == TimeUnit.WEEKS:
            schedule.every(period).weeks.do(SchedulerService.put_in_queue, function, args, True)
        elif time_unit == TimeUnit.DAILY:
            if time_hh_mm is None:
                time_hh_mm = period
            schedule.every().day.at(time_hh_mm).do(SchedulerService.put_in_queue, function, args, True)
        else:
            raise Exception(f"Inválid time unit -> {time_unit}")
        if time_unit != TimeUnit.DAILY:
            SchedulerService.__logger.info(
                f"Job {Utils.get_friendly_method_name(function)}({args if args else ''}) scheduled to run every {period} {time_unit.value}")
        else:
            SchedulerService.__logger.info(
                f"Job {Utils.get_friendly_method_name(function)}({args if args else ''}) scheduled to run at {time_hh_mm}")

    @staticmethod
    def init_job(function, args=None, priority_job=False, class_name=None, async_job=True) -> GenericDataDTO:
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
            instance = SchedulerService.get_instance_by_class_name(classe)
            if instance is not None:
                call_method = SchedulerService.call_method(instance, method)
                if async_job:
                    SchedulerService.__queue_service.put(call_method, priority_job, **args)
                else:
                    ret_ = call_method(**args)
                    return GenericDataDTO(msg=ret_)
                executed = True
        else:
            if class_name is not None:
                instance = SchedulerService.get_instance_by_class_name(class_name)
                if instance is not None:
                    service_call_method = SchedulerService.call_method(instance, function)
                    if async_job:
                        SchedulerService.__queue_service.put(service_call_method, priority_job, **args)
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

    @staticmethod
    def put_in_queue(function, args=None, priority=False):
        SchedulerService.__queue_service.put(function, priority, **args)

    @staticmethod
    def get_instance_by_class_name(class_name):
        class_name = Utils.snake_to_camel(class_name)
        for instance in SchedulerService.__services:
            if type(instance).__name__ == class_name:
                return instance
        return None


def scheduled_job(args=None,
                  period=5,
                  time_hh_mm="04:00",
                  time_unit: TimeUnit = TimeUnit.MINUTES):
    def decorator(func):
        SchedulerService.start_scheduled_job(func, args, period, time_hh_mm, time_unit)
        return func

    return decorator
