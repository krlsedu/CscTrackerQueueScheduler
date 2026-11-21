import threading
import unittest
import uuid
from unittest.mock import patch

import csctracker_queue_scheduler.services.queue_service as queue_service_mod
from csctracker_queue_scheduler.services.queue_service import QueueService
from csctracker_queue_scheduler.services.scheduler_service import SchedulerService


class TestQueueScheduler(unittest.TestCase):
    def test_priority_executes_before_normal_and_clears_unfinished_tasks(self):
        qs = QueueService(threads=1, poll_interval=0.02)
        started = threading.Event()
        gate = threading.Event()
        done_normal = threading.Event()
        execution_order = []

        def blocker():
            started.set()
            gate.wait(timeout=2)

        def normal_job():
            execution_order.append("normal")
            done_normal.set()

        def priority_job():
            execution_order.append("priority")

        qs.put(blocker)
        self.assertTrue(started.wait(timeout=2))

        qs.put(normal_job, priority=False)
        qs.put(priority_job, priority=True)
        gate.set()

        self.assertTrue(done_normal.wait(timeout=2))
        qs.priority_queue.join()
        qs.normal_queue.join()

        self.assertEqual(execution_order, ["priority", "normal"])
        self.assertEqual(qs.priority_queue.unfinished_tasks, 0)
        self.assertEqual(qs.normal_queue.unfinished_tasks, 0)

    def test_task_done_called_even_when_job_raises(self):
        qs = QueueService(threads=1, poll_interval=0.02)
        ran_after = threading.Event()

        def failing_job():
            raise RuntimeError("simulated job failure")

        def ok_job():
            ran_after.set()

        qs.put(failing_job, priority=False)
        qs.put(failing_job, priority=True)
        qs.put(ok_job, priority=False)

        self.assertTrue(ran_after.wait(timeout=2))

        join_thread = threading.Thread(
            target=lambda: (qs.priority_queue.join(), qs.normal_queue.join()),
            daemon=True,
        )
        join_thread.start()
        join_thread.join(timeout=2)

        self.assertFalse(join_thread.is_alive())
        self.assertEqual(qs.priority_queue.unfinished_tasks, 0)
        self.assertEqual(qs.normal_queue.unfinished_tasks, 0)

    def test_put_works_without_flask_and_generates_uuid_correlation_id(self):
        qs = QueueService(threads=1, poll_interval=0.02)
        captured = []
        done = threading.Event()

        def capture_job():
            captured.append(getattr(threading.current_thread(), "correlation_id", None))
            done.set()

        with patch.object(queue_service_mod, "g", None):
            qs.put(capture_job)

        self.assertTrue(done.wait(timeout=2))
        qs.normal_queue.join()
        self.assertEqual(len(captured), 1)
        uuid.UUID(captured[0])

    def test_scheduler_init_starts_single_daemon_worker_and_avoids_mutable_default(self):
        SchedulerService.init(threads=1)
        first_services = SchedulerService._SchedulerService__services
        self.assertEqual(len(first_services), 1)

        SchedulerService.init(threads=1)
        second_services = SchedulerService._SchedulerService__services
        self.assertEqual(len(second_services), 1)
        self.assertIsNot(first_services, second_services)

        worker_threads = [
            t
            for t in threading.enumerate()
            if getattr(t, "_target", None) == SchedulerService._SchedulerService__worker
        ]
        self.assertEqual(len(worker_threads), 1)
        self.assertTrue(worker_threads[0].daemon)

    def test_scheduler_put_in_queue_with_none_args(self):
        with patch(
            "csctracker_queue_scheduler.services.scheduler_service.QueueService",
            side_effect=lambda threads=None: QueueService(
                threads=threads, poll_interval=0.02
            ),
        ):
            SchedulerService.init(threads=1)
        done = threading.Event()

        SchedulerService.put_in_queue(lambda: done.set())
        self.assertTrue(done.wait(timeout=2))

    def test_clean_queue_and_get_queue_size(self):
        qs = QueueService(threads=0, poll_interval=0.02)
        qs.put(lambda: None, priority=False)
        qs.put(lambda: None, priority=True)

        sizes = [dto.msg for dto in qs.get_queue_size()]
        self.assertEqual(sizes, ["Normal queues: 1", "Priority queues: 1"])

        res = qs.clean_queue()
        self.assertEqual(res.msg, "Queues clean")
        self.assertTrue(qs.normal_queue.empty())
        self.assertTrue(qs.priority_queue.empty())
        self.assertEqual(qs.normal_queue.unfinished_tasks, 0)
        self.assertEqual(qs.priority_queue.unfinished_tasks, 0)


if __name__ == "__main__":
    unittest.main()
