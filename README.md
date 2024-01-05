# CscTrackerQueueScheduler

This project is a Python job scheduling and queuing library. It allows jobs to be scheduled to run at specific periods
and queues these jobs for execution.

## Key Features

- **Job Scheduling**: The Scheduler service (`SchedulerService`) allows jobs to be scheduled for execution at specified
  intervals. It supports intervals in seconds, minutes, hours, days, and weeks, as well as daily scheduling at a
  specific time.

- **Queue Service**: Scheduled tasks are put in a queue (`QueueService`) for execution. Tasks can be queued with or
  without priority, which determines their order of execution.

## Installing

Install and update using pip:

```
pip install csctracker-queue-scheduler
```

## Documentation and Examples

COMING SOON

## Simple Example

```python 
from csctracker_queue_scheduler.models.enums.time_unit import TimeUnit
from csctracker_queue_scheduler.services.scheduler_service import SchedulerService


def my_function(): print("Hello, world!")


SchedulerService.start_scheduled_job(
  function=my_function, period=5, time_unit=TimeUnit.SECONDS)
```

In the above example, `my_function` would be scheduled to run every 5 minutes.

## Testing

Currently, this project does not have automated tests. They may be added in the future as needed.

## Contributing

If you would like to contribute to this project, feel free to fork the repository, make your changes, and propose a pull
request.

## License

This project is under the MIT license. Please refer to the `LICENSE` file for more details.