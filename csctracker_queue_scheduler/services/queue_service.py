import logging
import os
import queue
import threading
import time
from queue import Queue

from csctracker_queue_scheduler.models.generic_data_dto import GenericDataDTO
from csctracker_queue_scheduler.utils import Utils


class QueueService:
    def __init__(self, threads: int = None):
        self.logger = logging.getLogger()
        if threads is None:
            threads = int(os.getenv("NUM_THREADS", 10))
        self.logger.debug(f"NUM_THREADS={threads}")
        self.normal_queue = Queue()
        self.priority_queue = Queue()
        self.init_threads(threads)

    def init_threads(self, num_threads):
        for i in range(num_threads):
            self.logger.debug(f"Starting thread {i}/{num_threads}")
            t = threading.Thread(target=self.__worker)
            t.daemon = True
            t.start()

    def __worker(self):
        while True:
            try:
                self.__run_job(self.priority_queue, "priority")
            except queue.Empty:
                try:
                    self.__run_job(self.normal_queue, "normal")
                except queue.Empty:
                    time.sleep(5)
                except Exception as e:
                    self.logger.error(f"Error in normal queue: {e}")
            except Exception as e:
                self.logger.error(f"Error in priority queue: {e}")

    def __run_job(self, queue, type):
        func_, args_ = queue.get_nowait()
        if func_ is not None:
            if not args_:
                args_ = None
            self.logger.info(
                f"Executing in {type} queue {Utils.get_friendly_method_name(func_)}({args_ if args_ else ''})")
            if args_ is not None:
                self.logger.info(
                    f"Return of {Utils.get_friendly_method_name(func_)}({args_ if args_ else ''}) -> {func_(**args_)}")
            else:
                self.logger.info(
                    f"Return of {Utils.get_friendly_method_name(func_)}({args_ if args_ else ''}) -> {func_()}")
            queue.task_done()
            self.logger.info(
                f"Executed in {type} queue {Utils.get_friendly_method_name(func_)}({args_ if args_ else ''})")

    def clean_queue(self) -> GenericDataDTO:
        while not self.normal_queue.empty():
            try:
                self.normal_queue.get(block=False)
            except queue.Empty:
                continue
            self.normal_queue.task_done()

        while not self.priority_queue.empty():
            try:
                self.priority_queue.get(block=False)
            except queue.Empty:
                continue
            self.priority_queue.task_done()

        return GenericDataDTO(msg="Queues clean")

    def get_queue_size(self) -> list[GenericDataDTO]:

        return [GenericDataDTO(msg=f"Normal queues: {self.normal_queue.qsize()}"),
                GenericDataDTO(msg=f"Priority queues: {self.priority_queue.qsize()}")]

    def put(self, func, priority=False, **args):
        if priority:
            self.priority_queue.put((func, args))
        else:
            self.normal_queue.put((func, args))
